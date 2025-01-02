import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración de la página
st.set_page_config(
    page_title="Calculadora de Interés Compuesto de Gume",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Estilo personalizado con CSS
st.markdown(
    """ 
    <style>
    /* Estilo general */
    body {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: white;
        font-family: 'Arial', sans-serif;
        margin: 0;
    }
    .main {
        padding: 3rem;
        background-color: rgba(0, 0, 0, 0.7);
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    h1 {
        font-size: 3rem;
        text-align: center;
    }
    h1 span.title-text {
        background: -webkit-linear-gradient(135deg, #1e90ff, #00bfff, #87cefa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    h2, h3, label {
        color: #87cefa;
    }
    .stButton>button {
        background: linear-gradient(135deg, #1e90ff, #00bfff);
        color: white;
        border: none;
        padding: 0.7rem 1.5rem;
        border-radius: 10px;
        font-size: 1rem;
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #00bfff, #1e90ff);
        box-shadow: 0px 6px 8px rgba(0, 0, 0, 0.3);
    }
    .stDataFrame, .stTable {
        background-color: rgba(0, 0, 0, 0.5);
        color: white;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Título de la página con HTML personalizado
st.markdown("<h1><span class='title-text'>Calculadora de Interés Compuesto de Gume</span> 🏆</h1>", unsafe_allow_html=True)
st.markdown("### Visualiza cómo tu inversión crece con el tiempo gracias al poder del interés compuesto.")

# Inputs del usuario
with st.container():
    st.subheader("Introduce los valores de tu inversión:")
    col1, col2, col3 = st.columns(3)
    with col1:
        deposito_inicial = st.number_input("Depósito Inicial ($):", min_value=0, value=600000, step=1000)
    with col2:
        aporte = st.number_input("Aportación ($):", min_value=0, value=65000, step=1000)
    with col3:
        incremento_aporte = st.number_input("Incremento % Anual en la Aportación:", min_value=0.0, value=0.0, step=0.1)

    col4, col5, col6 = st.columns(3)
    with col4:
        años_aporte = st.number_input("Número de Años con Aportaciones:", min_value=0, value=15, step=1)
    with col5:
        años_totales = st.number_input("Número Total de Años de Inversión:", min_value=años_aporte, value=40, step=1)
    with col6:
        frecuencia = st.radio("Frecuencia de Aportaciones:", ["Anual", "Mensual"], horizontal=True)

    rendimiento_anual = st.number_input("Rendimiento % Anual Promedio:", min_value=0.0, value=7.0, step=0.1)

# Función de cálculo
def calcular_interes_compuesto_detallado(deposito_inicial, aporte, incremento_aporte, años_aporte, años_totales, rendimiento_anual, frecuencia):
    monto = deposito_inicial
    deposito_acumulado = deposito_inicial
    aportaciones_acumuladas = 0
    historial = []
    
    # Ajuste según frecuencia (Mensual o Anual)
    factor_frecuencia = 12 if frecuencia == "Mensual" else 1
    aporte_total_anual = aporte * factor_frecuencia  # Convertir a aportación anual si es mensual

    for año in range(1, años_totales + 1):
        saldo_inicial = monto  # Saldo inicial es el monto acumulado al inicio del año
        if año <= años_aporte:
            aporte_actual = aporte_total_anual * ((1 + incremento_aporte / 100) ** (año - 1))
            monto += aporte_actual
            aportaciones_acumuladas += aporte_actual
        monto *= (1 + rendimiento_anual / 100)
        interes_ganado_anual = monto - saldo_inicial  # Diferencia entre saldo inicial y saldo después de intereses
        interes_acumulado = monto - deposito_acumulado - aportaciones_acumuladas
        historial.append({
            "Año": año,
            "Saldo Inicial": saldo_inicial,
            "Interés Ganado Año": interes_ganado_anual,
            "Aportaciones Acumuladas": aportaciones_acumuladas,
            "Interés Acumulado": interes_acumulado,
            "Monto Total": monto
        })
    
    return pd.DataFrame(historial)

# Botón para calcular
if st.button("Calcular"):
    resultados = calcular_interes_compuesto_detallado(
        deposito_inicial, aporte, incremento_aporte, años_aporte, años_totales, rendimiento_anual, frecuencia
    )

    # Mostrar los resultados
    total_aportaciones = resultados["Aportaciones Acumuladas"].iloc[-1]
    total_intereses = resultados["Interés Acumulado"].iloc[-1]
    monto_final = resultados["Monto Total"].iloc[-1]

    st.markdown("### Resultados Resumen:")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Depósito Inicial", f"${deposito_inicial:,.2f}")
    col2.metric("Aportaciones Acumuladas", f"${total_aportaciones:,.2f}")
    col3.metric("Interés Acumulado", f"${total_intereses:,.2f}")
    col4.metric("Total Final", f"${monto_final:,.2f}")

    # Crear gráfico de barras apiladas con Plotly
    fig = px.bar(
        resultados,
        x="Año",
        y=["Aportaciones Acumuladas", "Interés Acumulado"],
        title="Evolución del Valor de la Inversión",
        labels={"value": "Monto ($)", "variable": "Componentes"},
        color_discrete_map={
            "Aportaciones Acumuladas": "#87ceeb",
            "Interés Acumulado": "#1e90ff"
        },
        barmode="stack",
    )
    fig.update_layout(xaxis_title="Años", yaxis_title="Monto ($)", legend_title="Componentes")
    
    # Mostrar gráfico
    st.plotly_chart(fig, use_container_width=True)

    # Mostrar tabla de resultados a pantalla completa
    st.markdown("### Resultados por Año:")
    st.table(resultados[["Año", "Saldo Inicial", "Interés Ganado Año", "Aportaciones Acumuladas", "Interés Acumulado", "Monto Total"]].style.format({
        "Saldo Inicial": "${:,.2f}",
        "Interés Ganado Año": "${:,.2f}",
        "Aportaciones Acumuladas": "${:,.2f}",
        "Interés Acumulado": "${:,.2f}",
        "Monto Total": "${:,.2f}"
    }))
