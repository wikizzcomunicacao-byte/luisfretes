import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Painel de Métricas - Google Ads", page_icon="📊", layout="wide")

st.title("📊 Painel de Métricas - Google Ads")
st.markdown("Acompanhamento de desempenho das campanhas em tempo real.")

# Função para carregar o CSV do GitHub com segurança
@st.cache_data
def carregar_dados():
    nome_ficheiro = "dados.csv"
    for enc in ['utf-8', 'ISO-8859-1', 'cp1252']:
        try:
            df = pd.read_csv(nome_ficheiro, encoding=enc)
            return df
        except Exception:
            continue
    return None

df = carregar_dados()

if df is not None:
    # Limpeza básica dos nomes das colunas
    df.columns = df.columns.str.strip()
    
    # Conversão segura de colunas numéricas principais
    for col in ['Cliques', 'Impressões']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False), errors='coerce').fillna(0)

    # Cartões de Métricas (KPIs) no topo
    st.markdown("### 🚀 Visão Geral")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_cliques = df['Cliques'].sum() if 'Cliques' in df.columns else 0
        st.metric(label="Total de Cliques", value=f"{int(total_cliques):,}")

    with col2:
        total_impressoes = df['Impressões'].sum() if 'Impressões' in df.columns else 0
        st.metric(label="Total de Impressões", value=f"{int(total_impressoes):,}")

    with col3:
        custo_col = [c for c in df.columns if 'Custo' in c or 'Valor' in c or 'Investimento' in c]
        custo_val = 0.0
        if custo_col:
            try:
                serie = df[custo_col[0]].astype(str).str.replace('R$', '', regex=False).str.replace('.', '', regex=False).str.replace(',', '.', regex=False)
                custo_val = pd.to_numeric(serie, errors='coerce').sum()
            except Exception:
                custo_val = 0.0
        st.metric(label="Investimento Total", value=f"R$ {custo_val:,.2f}")

    with col4:
        cpc_col = [c for c in df.columns if 'CPC' in c]
        cpc_val = 0.0
        if cpc_col:
            try:
                serie_cpc = df[cpc_col[0]].astype(str).str.replace('R$', '', regex=False).str.replace(',', '.', regex=False)
                cpc_val = pd.to_numeric(serie_cpc, errors='coerce').mean()
            except Exception:
                cpc_val = 0.0
        st.metric(label="CPC Médio", value=f"R$ {cpc_val:,.2f}")

    st.divider()

    # Gráficos Visuais Modernos
    st.markdown("### 📈 Evolução Temporal")
    col_graf1, col_graf2 = st.columns(2)
    
    data_col = [c for c in df.columns if 'Data' in c or 'dia' in c.lower()]
    if data_col and 'Cliques' in df.columns:
        with col_graf1:
            st.subheader("Cliques por Dia")
            st.line_chart(df.set_index(data_col[0])['Cliques'])
            
    if data_col and 'Impressões' in df.columns:
        with col_graf2:
            st.subheader("Impressões por Dia")
            st.bar_chart(df.set_index(data_col[0])['Impressões'])

    st.divider()

    # Tabela Detalhada
    st.markdown("### 📋 Dados Detalhados")
    st.dataframe(df, use_container_width=True)

else:
    st.warning("⚠️ O ficheiro `dados.csv` não foi encontrado no repositório do GitHub.")
    st.info("Certifique-se de que o ficheiro se chama exatamente `dados.csv` e está na raiz do repositório.")
