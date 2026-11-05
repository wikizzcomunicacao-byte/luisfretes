import streamlit as st
import pandas as pd
import plotly.express as px

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
    
    # Tratamento de colunas numéricas de cliques e impressões
    for col in ['Cliques', 'Impressões']:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace('.', '', regex=False).str.replace(',', '.', regex=False), 
                errors='coerce'
            ).fillna(0)

    # Tratamento seguro da coluna de Custo
    if 'Custo' in df.columns:
        custo_limpo = (
            df['Custo'].astype(str)
            .str.replace('R$', '', regex=False)
            .str.replace('\xa0', '', regex=False)
            .str.replace('.', '', regex=False)
            .str.replace(',', '.', regex=False)
            .str.strip()
        )
        df['Custo_Num'] = pd.to_numeric(custo_limpo, errors='coerce').fillna(0)
    else:
        df['Custo_Num'] = 0.0

    # Adicionar uma coluna de data real para ordenar cronologicamente se necessário
    # Como as datas estão em formato descritivo, vamos manter a ordem original ou ordenar pelo índice correto
    # Vamos garantir que o eixo X exibe os dados de forma limpa

    # Cartões de Métricas (KPIs) no topo
    st.markdown("### 🚀 Visão Geral")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_cliques = int(df['Cliques'].sum())
        st.metric(label="Total de Cliques", value=f"{total_cliques:,}")

    with col2:
        total_impressoes = int(df['Impressões'].sum())
        st.metric(label="Total de Impressões", value=f"{total_impressoes:,}")

    with col3:
        total_custo = df['Custo_Num'].sum()
        st.metric(label="Investimento Total", value=f"R$ {total_custo:,.2f}")

    with col4:
        cpc_medio = (total_custo / total_cliques) if total_cliques > 0 else 0.0
        st.metric(label="CPC Médio", value=f"R$ {cpc_medio:,.2f}")

    st.divider()

    # Gráficos Profissionais com Plotly
    st.markdown("### 📈 Evolução Temporal")
    col_graf1, col_graf2 = st.columns(2)
    
    data_col = [c for c in df.columns if 'Data' in c or 'dia' in c.lower()]
    
    if data_col and 'Cliques' in df.columns:
        with col_graf1:
            # Gráfico de Linha Moderno (Plotly)
            fig_cliques = px.line(
                df, 
                x=data_col[0], 
                y='Cliques', 
                title="Evolução de Cliques por Dia",
                markers=True,
                template="plotly_white"
            )
            fig_cliques.update_traces(line_color='#2563eb', line_width=3, marker_size=8)
            fig_cliques.update_layout(xaxis_title="", yaxis_title="Cliques", margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_cliques, use_container_width=True)
            
    if data_col and 'Impressões' in df.columns:
        with col_graf2:
            # Gráfico de Barras Moderno (Plotly)
            fig_impr = px.bar(
                df, 
                x=data_col[0], 
                y='Impressões', 
                title="Evolução de Impressões por Dia",
                template="plotly_white"
            )
            fig_impr.update_traces(marker_color='#0284c7')
            fig_impr.update_layout(xaxis_title="", yaxis_title="Impressões", margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_impr, use_container_width=True)

    st.divider()

    # Tabela Detalhada
    st.markdown("### 📋 Dados Detalhados")
    st.dataframe(df.drop(columns=['Custo_Num'], errors='ignore'), use_container_width=True)

else:
    st.warning("⚠️ O ficheiro `dados.csv` não foi encontrado no repositório do GitHub.")
    st.info("Certifique-se de que o ficheiro se chama exatamente `dados.csv` e está na raiz do repositório.")
