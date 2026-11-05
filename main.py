import streamlit as st
import pandas as pd

# Configuração da página para ocupar a largura total e dar um aspeto profissional
st.set_page_config(page_title="Painel de Métricas - Google Ads", page_icon="📊", layout="wide")

# Estilo visual moderno com CSS personalizado
st.markdown("""
    <style>
        .main { background-color: #f8f9fa; }
        .metric-card {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Painel de Métricas - Google Ads")
st.markdown("Acompanhamento de desempenho das campanhas em tempo real.")

# Função para carregar o CSV do GitHub com segurança de codificação
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
    # Limpeza básica dos nomes das colunas (reirar espaços extras se houver)
    df.columns = df.columns.str.strip()
    
    # Exemplo de conversão de colunas monetárias ou numéricas se necessário
    # Garantir que colunas numéricas estão no formato correto
    for col in ['Cliques', 'Impressões']:
        if col in df.columns and df[col].dtype == object:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace('.', '').str.replace(',', '.'), errors='coerce')

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
        # Tenta calcular o custo total se existir coluna de custo
        custo_col = [c for c in df.columns if 'Custo' in c or 'Valor' in c]
        if custo_col:
            # Limpa formatação de moeda R$ se vier como string
            custo_serie = df[custo_col[0]]
            if custo_serie.dtype == object:
                custo_val = custo_serie.astype(str).str.replace('R$', '', regex=False).str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float).sum()
            else:
                custo_val = custo_serie.sum()
            st.metric(label="Investimento Total", value=f"R$ {custo_val:,.2f}")
        else:
            st.metric(label="Investimento Total", value="R$ 0,00")

    with col4:
        cpc_col = [c for c in df.columns if 'CPC' in c]
        if cpc_col:
            cpc_medio = df[cpc_col[0]]
            if cpc_medio.dtype == object:
                cpc_val = cpc_medio.astype(str).str.replace('R$', '', regex=False).str.replace(',', '.', regex=False).astype(float).mean()
            else:
                cpc_val = cpc_medio.mean()
            st.metric(label="CPC Médio", value=f"R$ {cpc_val:,.2f}")
        else:
            st.metric(label="CPC Médio", value="R$ 0,00")

    st.divider()

    # Gráficos Visuais Modernos
    st.markdown("### 📈 Evolução Temporal")
    
    col_graf1, col_graf2 = st.columns(2)
    
    data_col = [c for c in df.columns if 'Data' in c or 'dia' in c.lower()]
    if data_col and 'Cliques' in df.columns:
        # Gráfico de Linha para Cliques ao longo do tempo
        with col_graf1:
            st.subheader("Cliques por Dia")
            st.line_chart(df.set_index(data_col[0])['Cliques'])
            
    if data_col and 'Impressões' in df.columns:
        # Gráfico de Barras para Impressões ao longo do tempo
        with col_graf2:
            st.subheader("Impressões por Dia")
            st.bar_chart(df.set_index(data_col[0])['Impressões'])

    st.divider()

    # Tabela Detalhada com aspeto limpo
    st.markdown("### 📋 Dados Detalhados")
    st.dataframe(df, use_container_width=True)

else:
    st.warning("⚠️ O ficheiro `dados.csv` não foi encontrado no repositório do GitHub.")
    st.info("Certifique-se de que o ficheiro se chama exatamente `dados.csv` e está na raiz do repositório.")
