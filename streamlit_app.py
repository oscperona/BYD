import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from assets import BYD_LOGO_SVG

# Configuración de página
st.set_page_config(
    page_title="BYD Seal U DM-i Calculator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado para diseño elegante
st.markdown("""
    <style>
    /* Estilos generales */
    * {
        font-family: 'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    
    /* Logo SVG */
    svg {
        max-width: 100%;
        height: auto;
    }
    
    /* Contenedor principal con fondo profesional */
    .main {
        background: linear-gradient(135deg, #F5F2ED 0%, #E8DFD3 25%, #f0eae0 50%, #e8dfd3 75%, #F5F2ED 100%);
        background-attachment: fixed;
        position: relative;
    }
    
    .main::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(160, 147, 124, 0.03) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(139, 115, 85, 0.02) 0%, transparent 50%);
        pointer-events: none;
        z-index: -1;
    }
    
    /* Watermark SVG sutil */
    .stMainBlockContainer {
        position: relative;
    }
    
    body::before {
        content: '';
        position: fixed;
        bottom: -10%;
        right: -5%;
        width: 600px;
        height: 600px;
        background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 100"><path d="M20 50 Q50 20, 80 20 L120 20 Q150 20, 170 50 L170 70 Q170 85, 150 85 L50 85 Q30 85, 30 70 Z" fill="none" stroke="%23A0937C" stroke-width="1" opacity="0.08"/><circle cx="50" cy="75" r="3" fill="%23A0937C" opacity="0.08"/><circle cx="150" cy="75" r="3" fill="%23A0937C" opacity="0.08"/></svg>');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        pointer-events: none;
        z-index: 0;
    }
    
    /* Títulos */
    h1 {
        color: #5C4A3F;
        font-weight: 700;
        text-align: center;
        margin-bottom: 8px;
        padding-top: 20px;
        font-size: 2.5em;
        letter-spacing: -0.5px;
    }
    
    h2 {
        color: #8B6F47;
        font-weight: 600;
        border-bottom: 2px solid #A0937C;
        padding-bottom: 12px;
        margin-top: 30px;
        font-size: 1.4em;
    }
    
    h3 {
        color: #6B5344;
        font-weight: 600;
    }
    
    /* Divisores */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(to right, transparent, #A0937C, transparent);
        margin: 20px 0;
    }
    
    /* Tarjetas de métrica */
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.08);
        border-left: 4px solid #A0937C;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        backdrop-filter: blur(10px);
    }
    
    .metric-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 16px 32px rgba(0, 0, 0, 0.12);
    }
    
    /* Botón principal */
    .stButton > button {
        background: linear-gradient(135deg, #A0937C 0%, #8B7355 50%, #7A6245 100%);
        color: white;
        font-weight: 600;
        padding: 14px 45px;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 6px 20px rgba(160, 147, 124, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-size: 0.9em;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 28px rgba(160, 147, 124, 0.5);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    /* Inputs y selectores */
    .stNumberInput > div > div > input,
    .stSlider > div > div > input {
        border-radius: 8px;
        border: 2px solid #E8E1D8;
        padding: 12px;
        transition: all 0.3s ease;
        background-color: #FAFAF9;
    }
    
    .stNumberInput > div > div > input:focus,
    .stSlider > div > div > input:focus {
        border-color: #A0937C;
        box-shadow: 0 0 12px rgba(160, 147, 124, 0.2);
        background-color: white;
    }
    
    .stSlider > div > div > div {
        background-color: #A0937C !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #F5F2ED 0%, #E8DFD3 100%);
    }
    
    /* Subtítulos */
    .subtitle {
        text-align: center;
        color: #8B7968;
        font-size: 18px;
        margin-bottom: 25px;
        font-weight: 300;
        letter-spacing: 0.3px;
    }
    
    /* Contenedor de resultados */
    [data-testid="stVerticalBlock"] > div > div {
        background-color: transparent !important;
    }
    
    /* Métricas Streamlit */
    [data-testid="metric-container"] {
    
    /* Contenedor del logo */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 10px;
    }
    class="logo-container
    /* Contenedor del coche de fondo */
    .car-background {
        position: relative;
        width: 100%;
        opacity: 0.08;
        margin: -50px auto;
        z-index: 0;
    }
        background-color: rgba(255, 255, 255, 0.9);
        border-radius: 12px;
        padding: 16px;
        border-left: 4px solid #A0937C;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
    }
    </style>
""", unsafe_allow_html=True)

# HEADER
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.html(BYD_LOGO_SVG)

with col2:
    st.markdown("<h1>⚡ CALCULADORA BYD SEAL U DM-i</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Análisis inteligente de consumo y eficiencia energética</p>", unsafe_allow_html=True)

with col3:
    st.markdown("")

st.markdown("---")

# SIDEBAR - Configuración del vehículo
st.sidebar.markdown("### ⚙️ CONFIGURACIÓN DEL VEHÍCULO")
st.sidebar.markdown("---")

cap_bateria = st.sidebar.slider("Capacidad Útil Batería (kWh)", 20.0, 35.0, 26.6, step=0.1)
cap_deposito = st.sidebar.slider("Capacidad Depósito (L)", 40.0, 80.0, 60.0, step=1.0)

st.sidebar.markdown("### 💰 PRECIOS DE COMBUSTIBLE")
st.sidebar.markdown("---")

precio_gasolina = st.sidebar.number_input("Precio Gasolina (€/L)", min_value=0.0, value=1.73, step=0.01, format="%.2f")
precio_luz = st.sidebar.number_input("Precio Luz (€/kWh)", min_value=0.0, value=0.07, step=0.001, format="%.3f")

# SECCIÓN PRINCIPAL
st.markdown("### 📍 DATOS DE TU VIAJE")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**🛣️ DISTANCIA Y BATERÍA**")
    distancia = st.number_input("Distancia recorrida (km)", value=254.0, min_value=1.0, step=0.1)
    st.markdown("<small style='color: #8B7968;'>Porcentaje de batería al inicio y final del viaje</small>", unsafe_allow_html=True)
    bat_inicial = st.slider("Batería Inicial (%)", 0, 100, 100)
    bat_final = st.slider("Batería Final (%)", 0, 100, 20)

with col2:
    st.markdown("**⛽ GASOLINA**")
    st.markdown("<small style='color: #8B7968;'>Nivel de combustible al inicio y final</small>", unsafe_allow_html=True)
    gas_inicial = st.slider("Gasolina Inicial (%)", 0, 100, 100, key="gas_ini")
    gas_final = st.slider("Gasolina Final (%)", 0, 100, 85, key="gas_fin")

st.markdown("---")

# BOTÓN DE CÁLCULO
st.markdown("")
col_button = st.columns([0.3, 0.4, 0.3])
with col_button[1]:
    calcular = st.button("🧮  CALCULAR  ANÁLISIS", use_container_width=True, key="calc_button")

# RESULTADOS
if calcular:
    # Mostrar imagen real del coche de fondo
    col_car = st.columns([1, 2, 1])
    with col_car[1]:
        st.image("https://www.grupogamboa.com/img/gama/byd/seal-u-dm-i/93e4d09e-a3d3-4783-ae41-614515da8be3.png", use_container_width=True)
    
    # Cálculos
    kwh_gastados = ((bat_inicial - bat_final) / 100) * cap_bateria
    litros_gastados = ((gas_inicial - gas_final) / 100) * cap_deposito
    
    kwh_100km = (kwh_gastados / distancia) * 100
    litros_100km = (litros_gastados / distancia) * 100
    
    litros_equiv_luz = kwh_gastados / 8.9
    litros_totales_equiv = litros_gastados + litros_equiv_luz
    combinado_100km = (litros_totales_equiv / distancia) * 100
    
    coste_gasolina = litros_gastados * precio_gasolina
    coste_luz = kwh_gastados * precio_luz
    coste_total = coste_gasolina + coste_luz
    coste_100km = (coste_total / distancia) * 100
    
    # Mostrar resultados
    st.markdown("")
    st.markdown("### 📊 RESULTADOS DEL ANÁLISIS")
    st.markdown("---")
    
    # Resultados de consumo
    st.markdown("#### 📈 CONSUMO DETALLADO")
    col_res1, col_res2, col_res3, col_res4 = st.columns(4)
    
    with col_res1:
        st.metric(
            label="Gasolina",
            value=f"{litros_100km:.2f}",
            delta="L/100km"
        )
    
    with col_res2:
        st.metric(
            label="Electricidad",
            value=f"{kwh_100km:.2f}",
            delta="kWh/100km"
        )
    
    with col_res3:
        st.metric(
            label="Consumo Combinado",
            value=f"{combinado_100km:.2f}",
            delta="L/100km eq."
        )
    
    with col_res4:
        porcentaje_electrico = (kwh_100km / (combinado_100km * 8.9)) * 100
        st.metric(
            label="Energía Eléctrica",
            value=f"{porcentaje_electrico:.1f}%",
            delta="del total"
        )
    
    st.markdown("---")
    
    # Resultados de costes
    st.markdown("#### 💳 ANÁLISIS DE COSTES")
    col_cost1, col_cost2, col_cost3, col_cost4 = st.columns(4)
    
    with col_cost1:
        porcentaje_gas = (coste_gasolina/coste_total*100)
        st.metric(
            label="Coste Gasolina",
            value=f"{coste_gasolina:.2f}€",
            delta=f"{porcentaje_gas:.0f}% del total"
        )
    
    with col_cost2:
        porcentaje_luz = (coste_luz/coste_total*100)
        st.metric(
            label="Coste Electricidad",
            value=f"{coste_luz:.2f}€",
            delta=f"{porcentaje_luz:.0f}% del total"
        )
    
    with col_cost3:
        st.metric(
            label="Coste Total",
            value=f"{coste_total:.2f}€",
            delta=f"en {distancia:.0f} km"
        )
    
    with col_cost4:
        st.metric(
            label="Coste Normalizado",
            value=f"{coste_100km:.2f}€",
            delta="por cada 100 km"
        )
    
    st.markdown("---")
    
    # Gráficos
    st.markdown("#### 📉 VISUALIZACIONES")
    
    col_graph1, col_graph2 = st.columns(2)
    
    with col_graph1:
        # Gráfico de consumo
        fig_consumo = go.Figure(data=[
            go.Bar(name='Gasolina (L/100km)', x=['Consumo'], y=[litros_100km], marker_color='#A0937C'),
            go.Bar(name='Eléctrico (eq. L/100km)', x=['Consumo'], y=[litros_equiv_luz / distancia * 100], marker_color='#DDB892')
        ])
        fig_consumo.update_layout(
            title="Desglose de Consumo",
            barmode='stack',
            height=400,
            hovermode='x unified',
            template='plotly_white',
            font=dict(family="Segoe UI, sans-serif", size=11, color="#6B5344"),
            paper_bgcolor='rgba(255,255,255,0.95)',
            plot_bgcolor='rgba(245,242,237,0.5)',
            title_font=dict(size=14, color="#6B5344")
        )
        st.plotly_chart(fig_consumo, use_container_width=True)
    
    with col_graph2:
        # Gráfico de costes
        colores = ['#A0937C', '#DDB892']
        fig_costes = go.Figure(data=[go.Pie(
            labels=['Gasolina', 'Electricidad'],
            values=[coste_gasolina, coste_luz],
            marker=dict(colors=colores, line=dict(color='white', width=2)),
            hovertemplate='<b>%{label}</b><br>€%{value:.2f}<br>%{percent}<extra></extra>'
        )])
        fig_costes.update_layout(
            title="Distribución de Costes",
            height=400,
            template='plotly_white',
            font=dict(family="Segoe UI, sans-serif", size=11, color="#6B5344"),
            paper_bgcolor='rgba(255,255,255,0.95)',
            title_font=dict(size=14, color="#6B5344")
        )
        st.plotly_chart(fig_costes, use_container_width=True)
    
    st.markdown("---")
    
    # Tabla resumen
    st.markdown("#### 📋 TABLA RESUMEN COMPLETA")
    datos_resumen = {
        'Métrica': [
            'Distancia',
            'Batería Gastada',
            'Gasolina Gastada',
            'Consumo Gasolina',
            'Consumo Eléctrico',
            'Consumo Combinado',
            'Coste Gasolina',
            'Coste Electricidad',
            'Coste Total',
            'Coste por 100 km'
        ],
        'Valor': [
            f'{distancia:.1f} km',
            f'{kwh_gastados:.2f} kWh',
            f'{litros_gastados:.2f} L',
            f'{litros_100km:.2f} L/100km',
            f'{kwh_100km:.2f} kWh/100km',
            f'{combinado_100km:.2f} L/100km',
            f'{coste_gasolina:.2f} €',
            f'{coste_luz:.2f} €',
            f'{coste_total:.2f} €',
            f'{coste_100km:.2f} €/100km'
        ]
    }
    
    df_resumen = pd.DataFrame(datos_resumen)
    st.dataframe(df_resumen, use_container_width=True, hide_index=True)
