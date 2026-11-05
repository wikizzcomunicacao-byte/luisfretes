import streamlit as st
import pandas as pd

st.set_page_config(page_title="Painel de Métricas", layout="wide")

st.title("📊 Painel de Métricas - Google Ads / Desempenho")

# Função para carregar a planilha diretamente do repositório
@st.cache_data
def carregar_dados():
    # Substitua "dados.xlsx" pelo nome exato do ficheiro que colocar no GitHub
    nome_ficheiro = "dados.xlsx" 
    try:
        if nome_ficheiro.endswith('.csv'):
            df = pd.read_csv(nome_ficheiro)
        else:
            df = pd.read_excel(nome_ficheiro)
        return df
    except FileNotFoundError:
        return None

df = carregar_dados()

if df is not None:
    st.success("Planilha carregada com sucesso a partir do GitHub!")
    
    # Exemplo de Métricas (Substitua pelos nomes reais das colunas da sua planilha)
    st.subheader("Resumo Geral")
    
    # Crie colunas para métricas (exemplo: Custo, Cliques, Impressões)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if 'Cliques' in df.columns:
            total_cliques = df['Cliques'].sum()
            st.metric("Total de Cliques", f"{total_cliques:,}")
    with col2:
        if 'Custo' in df.columns:
            total_custo = df['Custo'].sum()
            st.metric("Investimento Total", f"R$ {total_custo:,.2f}")
    with col3:
        if 'Conversões' in df.columns:
            total_conversoes = df['Conversões'].sum()
            st.metric("Total de Conversões", f"{total_conversoes:,}")

    # Tabela detalhada
    st.subheader("Dados Detalhados das Campanhas")
    st.dataframe(df, use_container_width=True)

else:
    st.warning("⚠️ O ficheiro da planilha ainda não foi encontrado no repositório.")
    st.info("Para resolver: adicione a sua planilha (`dados.xlsx` ou `dados.csv`) na mesma pasta raiz do seu projeto no GitHub.")
