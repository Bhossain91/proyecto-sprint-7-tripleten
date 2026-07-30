import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ======================================================
# CONFIGURACIÓN DE LA PÁGINA
# ======================================================

st.set_page_config(
    page_title="Dashboard Vehiculos del Mercado",
    page_icon="🚗",
    layout="wide"
)

# ======================================================
# CARGAR DATOS
# ======================================================

@st.cache_data
def load_data():
    df = pd.read_csv("vehicles_us.csv")
    df["manufacturer"] = df["model"].str.split().str[0]
    return df

df = load_data()

# ======================================================
# TÍTULO
# ======================================================

st.title("🚗 Dashboard Vehiculos del Mercado")

st.markdown("""
Exploración interactiva del conjunto de datos **Vehicles US** utilizando
**Pandas**, **Plotly Graph Objects** y **Streamlit**.
""")

st.divider()

# ======================================================
# SIDEBAR
# ======================================================

st.sidebar.header("Filtros")

manufacturer = st.sidebar.selectbox(
    "Fabricante",
    ["Todos"] + sorted(df["manufacturer"].unique().tolist())
)

vehicle_type = st.sidebar.selectbox(
    "Tipo de vehículo",
    ["Todos"] + sorted(df["type"].dropna().unique().tolist())
)

condition = st.sidebar.selectbox(
    "Condición",
    ["Todas"] + sorted(df["condition"].dropna().unique().tolist())
)

# ======================================================
# FILTROS
# ======================================================

filtered = df.copy()

if manufacturer != "Todos":
    filtered = filtered[
        filtered["manufacturer"] == manufacturer
    ]

if vehicle_type != "Todos":
    filtered = filtered[
        filtered["type"] == vehicle_type
    ]

if condition != "Todas":
    filtered = filtered[
        filtered["condition"] == condition
    ]

# ======================================================
# DATA VIEWER
# ======================================================

st.header("📋 Data Viewer")

if st.checkbox("Mostrar datos filtrados"):

    st.dataframe(
        filtered,
        use_container_width=True
    )

st.divider()

# ======================================================
# BARRAS
# ======================================================

st.header("📊 Tipo de Vehículo por Fabricante")

if st.checkbox("Construir gráfico de barras"):

    vehicle_count = (
        filtered.groupby("type")
        .size()
        .reset_index(name="count")
    )

    fig = go.Figure()

    fig.add_trace(

        go.Bar(

            x=vehicle_count["type"],
            y=vehicle_count["count"],
            text=vehicle_count["count"],
            textposition="outside"

        )
    )

    fig.update_layout(

        title="Cantidad de vehículos por tipo",
        xaxis_title="Tipo",
        yaxis_title="Cantidad",
        template="plotly_white"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ======================================================
# HISTOGRAMA CONDICIÓN
# ======================================================

st.header("🚙 Condición vs Año Modelo")

if st.checkbox("Construir histograma condición"):

    fig = go.Figure()

    for cond in filtered["condition"].dropna().unique():

        temp = filtered[
            filtered["condition"] == cond
        ]

        fig.add_trace(

            go.Histogram(

                x=temp["model_year"],
                name=cond,
                opacity=0.75

            )
        )

    fig.update_layout(

        title="Condición del vehículo por año modelo",
        xaxis_title="Año Modelo",
        yaxis_title="Cantidad",
        barmode="overlay",
        template="plotly_white"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ======================================================
# DISPERSIÓN
# ======================================================

st.header("💲 Precio vs Odómetro")

if st.checkbox("Construir gráfico de dispersión"):

    fig = go.Figure()

    fig.add_trace(

        go.Scatter(

            x=filtered["odometer"],
            y=filtered["price"],
            mode="markers",

            marker=dict(
                size=6,
                color=filtered["price"],
                colorscale="Viridis",
                showscale=True
            ),

            text=filtered["manufacturer"]

        )
    )

    fig.update_layout(

        title="Precio vs Odómetro",
        xaxis_title="Odómetro",
        yaxis_title="Precio",
        template="plotly_white"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ======================================================
# COMPARACIÓN DE FABRICANTES
# ======================================================

st.header("📉 Comparación de Precios")

manufacturer1 = st.selectbox(
    "Fabricante 1",
    sorted(df["manufacturer"].unique()),
    key="m1"
)

manufacturer2 = st.selectbox(
    "Fabricante 2",
    sorted(df["manufacturer"].unique()),
    key="m2"
)

if st.checkbox("Comparar fabricantes"):

    compare = df[
        df["manufacturer"].isin(
            [manufacturer1, manufacturer2]
        )
    ]

    fig = go.Figure()

    for brand in [manufacturer1, manufacturer2]:

        temp = compare[
            compare["manufacturer"] == brand
        ]

        fig.add_trace(

            go.Histogram(

                x=temp["price"],
                histnorm="percent",
                name=brand,
                opacity=0.75

            )
        )

    fig.update_layout(

        title="Distribución porcentual de precios",
        xaxis_title="Precio",
        yaxis_title="Porcentaje",
        barmode="overlay",
        template="plotly_white"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )