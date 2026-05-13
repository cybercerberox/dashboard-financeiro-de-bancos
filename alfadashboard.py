import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------
# CONFIGURAÇÃO DA PÁGINA
# -----------------------------------
st.set_page_config(
    page_title="Dashboard Financeiro Neon",
    layout="wide"
)

# -----------------------------------
# CSS PERSONALIZADO
# -----------------------------------
st.markdown("""
<style>

.main {
    background-color: #0f172a;
}

h1, h2, h3, h4 {
    color: #00F5FF;
}

[data-testid="metric-container"] {
    background-color: #111827;
    border: 1px solid #00F5FF;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0px 0px 15px #00F5FF;
}

[data-testid="metric-container"] label {
    color: white !important;
}

[data-testid="metric-container"] div {
    color: #00F5FF !important;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

.stDataFrame {
    border-radius: 15px;
    overflow: hidden;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------
# TÍTULO
# -----------------------------------
st.title("💎 Dashboard Financeiro Neon")

st.markdown("""
### Controle financeiro em tempo real
""")

# -----------------------------------
# LEITURA DA PLANILHA
# -----------------------------------
df = pd.read_csv(
    "CLIENTESSTREAMLIT - Financeiro.csv",
    sep=None,
    engine="python"
)

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
)

st.write(df.columns.tolist())

st.stop()

# -----------------------------------
# CONVERTER VALOR
# -----------------------------------
df["valor"] = (
    df["valor"]
    .astype(str)
    .str.replace(",", ".")
    .astype(float)
)

# -----------------------------------
# FILTROS
# -----------------------------------
st.sidebar.title("📌 Filtros")

status = st.sidebar.multiselect(
    "Status",
    options=df["status"].unique(),
    default=df["status"].unique()
)

empresa = st.sidebar.multiselect(
    "Empresa",
    options=df["empresa"].unique(),
    default=df["empresa"].unique()
)

mes = st.sidebar.multiselect(
    "Mês",
    options=df["mes"].unique(),
    default=df["mes"].unique()
)

valor_min = st.sidebar.slider(
    "Valor mínimo",
    min_value=int(df["valor"].min()),
    max_value=int(df["valor"].max()),
    value=int(df["valor"].min())
)

# -----------------------------------
# FILTRAGEM
# -----------------------------------
df_filtrado = df[
    (df["status"].isin(status)) &
    (df["empresa"].isin(empresa)) &
    (df["mes"].isin(mes)) &
    (df["valor"] >= valor_min)
]

# -----------------------------------
# MÉTRICAS
# -----------------------------------
total_clientes = len(df_filtrado)

clientes_pagantes = len(
    df_filtrado[df_filtrado["status"] == "Pago"]
)

clientes_inadimplentes = len(
    df_filtrado[df_filtrado["status"] == "Inadimplente"]
)

faturamento = df_filtrado["valor"].sum()

ticket_medio = df_filtrado["valor"].mean()

# -----------------------------------
# CARDS
# -----------------------------------
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Clientes",
    total_clientes
)

col2.metric(
    "Pagantes",
    clientes_pagantes
)

col3.metric(
    "Inadimplentes",
    clientes_inadimplentes
)

col4.metric(
    "Faturamento",
    f"R$ {faturamento:,.2f}"
)

col5.metric(
    "Ticket Médio",
    f"R$ {ticket_medio:,.2f}"
)

st.divider()

# -----------------------------------
# GRÁFICO PIZZA
# -----------------------------------
status_count = (
    df_filtrado["status"]
    .value_counts()
    .reset_index()
)

status_count.columns = [
    "status",
    "quantidade"
]

fig_pizza = px.pie(
    status_count,
    names="status",
    values="quantidade",
    title="Clientes Pagantes x Inadimplentes",
    hole=0.5
)

fig_pizza.update_layout(
    paper_bgcolor="#0f172a",
    plot_bgcolor="#0f172a",
    font_color="white"
)

st.plotly_chart(
    fig_pizza,
    use_container_width=True
)

# -----------------------------------
# GRÁFICO BARRAS
# -----------------------------------
empresa_total = (
    df_filtrado
    .groupby("empresa")["valor"]
    .sum()
    .reset_index()
)

fig_barra = px.bar(
    empresa_total,
    x="empresa",
    y="valor",
    title="Faturamento por Empresa"
)

fig_barra.update_layout(
    paper_bgcolor="#0f172a",
    plot_bgcolor="#0f172a",
    font_color="white"
)

st.plotly_chart(
    fig_barra,
    use_container_width=True
)

# -----------------------------------
# GRÁFICO LINHA
# -----------------------------------
mes_total = (
    df_filtrado
    .groupby("mes")["valor"]
    .sum()
    .reset_index()
)

fig_linha = px.line(
    mes_total,
    x="mes",
    y="valor",
    title="Evolução Financeira"
)

fig_linha.update_layout(
    paper_bgcolor="#0f172a",
    plot_bgcolor="#0f172a",
    font_color="white"
)

st.plotly_chart(
    fig_linha,
    use_container_width=True
)

# -----------------------------------
# ANÁLISES
# -----------------------------------
st.subheader("📊 Análises Inteligentes")

maior_empresa = empresa_total.loc[
    empresa_total["valor"].idxmax()
]

st.success(
    f"""
    Empresa com maior faturamento:
    {maior_empresa['empresa']}
    - R$ {maior_empresa['valor']:,.2f}
    """
)

percentual_inad = (
    clientes_inadimplentes / total_clientes
) * 100

st.warning(
    f"""
    Taxa de inadimplência:
    {percentual_inad:.1f}%
    """
)

# -----------------------------------
# TABELA
# -----------------------------------
st.subheader("📋 Dados Financeiros")

st.dataframe(
    df_filtrado,
    use_container_width=True
)