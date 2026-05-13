import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------
# CONFIGURAÇÃO DA PÁGINA
# -----------------------------------
st.set_page_config(
    page_title="Dashboard Financeiro",
    layout="wide"
)

st.title("Dashboard Financeiro")

# -----------------------------------
# LINK GOOGLE PLANILHAS CSV
# -----------------------------------
# EXEMPLO:
# https://docs.google.com/spreadsheets/d/ID/export?format=csv

url = "https://docs.google.com/spreadsheets/d/1zLlMxT9vKT5oJv8mWVPr0x3vq3EBsJR4E-SwY26r1Hk/edit?usp=sharing"

# -----------------------------------
# LEITURA DA PLANILHA
# -----------------------------------
df = pd.read_csv(
    "CLIENTESSTREAMLIT - Financeiro.csv",
    sep=","
)
# LIMPAR COLUNAS
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
)

# MOSTRAR COLUNAS
st.write(df.columns)

# CONVERTER VALOR PARA NÚMERO
df["valor"] = (
    df["valor"]
    .astype(str)
    .str.replace(",", ".")
    .astype(float)
)

st.sidebar.header("Filtros")

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

col1.metric("Clientes", total_clientes)

col2.metric("Pagantes", clientes_pagantes)

col3.metric("Inadimplentes", clientes_inadimplentes)

col4.metric(
    "Faturamento",
    f"R$ {faturamento:,.2f}"
)

col5.metric(
    "Ticket Médio",
    f"R$ {ticket_medio:,.2f}"
)

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
    title="Clientes Pagantes x Inadimplentes"
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

st.plotly_chart(
    fig_linha,
    use_container_width=True
)

# -----------------------------------
# ANÁLISES AUTOMÁTICAS
# -----------------------------------
st.subheader("Análises")

maior_empresa = empresa_total.loc[
    empresa_total["valor"].idxmax()
]

st.success(
    f"Empresa com maior faturamento: "
    f"{maior_empresa['empresa']} "
    f"- R$ {maior_empresa['valor']:,.2f}"
)

percentual_inad = (
    clientes_inadimplentes / total_clientes
) * 100

st.warning(
    f"Taxa de inadimplência: "
    f"{percentual_inad:.1f}%"
)

# -----------------------------------
# TABELA
# -----------------------------------
st.subheader("📋 Dados Financeiros")

st.dataframe(
    df_filtrado,
    use_container_width=True
)