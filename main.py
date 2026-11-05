import streamlit as st
import pandas as pd

st.set_page_config(page_title="Painel de Métricas", layout="wide")

st.title("📊 Painel de Métricas - Google Ads")

# Função para carregar o CSV diretamente do repositório
@st.cache_data
def carregar_dados():
    nome_ficheiro = "dados.csv"
    try:
        # Lê o ficheiro CSV (com codificação UTF-8 ou ISO-8859-1 para aceitar acentos)
        df = pd.read_csv(nome_ficheiro, encoding='utf-8')
        return df
    except UnicodeDecodeError:
        try:
            df = pd.read_csv(nome_ficheiro, encoding='ISO-8859-1')
            return df
        except Exception as e:
            return None
    except FileNotFoundError:
        return None

df = carregar_dados()

if df is not None:
    st.success("Planilha CSV carregada com sucesso a partir do GitHub!")
    
    # Exibe a tabela detalhada com todos os dados
    st.subheader("Dados Detalhados das Campanhas")
    st.dataframe(df, use_container_width=True)

else:
    st.warning("⚠️ O ficheiro `dados.csv` ainda não foi encontrado no repositório.")
    st.info("Para resolver: adicione o seu ficheiro CSV com o nome exato `dados.csv` na pasta raiz do seu projeto no GitHub.")
