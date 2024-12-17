import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# Configuração da página
st.set_page_config(page_title="Sistema de Análise de Tendências", layout="wide")

# Título principal
st.title("Sistema de Análise de Tendências para Diagnóstico Organizacional em Cooperativas")

# Função para carregar dados
@st.cache_data
def load_data(uploaded_file):
      if uploaded_file is not None:
        try:
            # Obtém a extensão do arquivo
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            # Lê o arquivo baseado na extensão
            if file_extension == 'csv':
                data = pd.read_csv(uploaded_file)
            elif file_extension in ['xls', 'xlsx']:
                data = pd.read_excel(uploaded_file, engine='openpyxl')
            else:
                st.error(f"Formato de arquivo não suportado: {file_extension}")
                return None
            
            return data
        except Exception as e:
            st.error(f"Erro ao carregar o arquivo: {str(e)}")
            return None
    return None
        
        return data
    return None

# Upload de arquivo
uploaded_file = st.file_uploader("Escolha um arquivo", type=['csv', 'xlsx', 'xls'])
data = load_data(uploaded_file)

if data is not None:
    # Sidebar para navegação
    st.sidebar.title("Menu")
    page = st.sidebar.radio("Selecione uma página:", ["Visão Geral", "Análise por Ramo", "Tendências Anuais"])

    # Página de Visão Geral
    if page == "Visão Geral":
        st.header("Visão Geral dos Dados")
        st.write(data)

        st.subheader("Estatísticas Gerais")
        st.write(data.describe())

    # Página de Análise por Ramo
    elif page == "Análise por Ramo":
        st.header("Análise por Ramo")
        
        # Assumindo que existe uma coluna 'Ramo' no seu DataFrame
        if 'Ramo' in data.columns:
            ramo_selecionado = st.selectbox("Selecione um Ramo:", data["Ramo"].unique())
            ramo_data = data[data["Ramo"] == ramo_selecionado]
            
            st.subheader(f"Dados do Ramo: {ramo_selecionado}")
            st.write(ramo_data)
            
            # Aqui você pode adicionar visualizações específicas para o ramo selecionado
            # Por exemplo, um gráfico de linha mostrando tendências ao longo do tempo
            if 'Ano do Diagnóstico' in ramo_data.columns:
                fig, ax = plt.subplots()
                numeric_columns = ramo_data.select_dtypes(include=[np.number]).columns
                for col in numeric_columns:
                    if col != 'Ano do Diagnóstico':
                        ax.plot(ramo_data['Ano do Diagnóstico'], ramo_data[col], label=col)
                plt.title(f"Tendências para {ramo_selecionado}")
                plt.legend()
                st.pyplot(fig)
        else:
            st.error("Coluna 'Ramo' não encontrada nos dados.")

    # Página de Tendências Anuais
    elif page == "Tendências Anuais":
        st.header("Tendências Anuais")
        
        if 'Ano do Diagnóstico' in data.columns and 'Ramo' in data.columns:
            fig, ax = plt.subplots(figsize=(10, 6))
            for ramo in data["Ramo"].unique():
                ramo_data = data[data["Ramo"] == ramo]
                ax.plot(ramo_data["Ano do Diagnóstico"], ramo_data.select_dtypes(include=[np.number]).mean(axis=1), label=ramo)
            
            plt.title("Tendências Anuais por Ramo")
            plt.xlabel("Ano")
            plt.ylabel("Média dos Índices")
            plt.legend(title="Ramo", bbox_to_anchor=(1.05, 1), loc='upper left')
            plt.tight_layout()
            st.pyplot(fig)

            st.subheader("Análise de Crescimento")
            for ramo in data["Ramo"].unique():
                ramo_data = data[data["Ramo"] == ramo].sort_values("Ano do Diagnóstico")
                if len(ramo_data) > 1:
                    primeiro_ano = ramo_data.iloc[0]
                    ultimo_ano = ramo_data.iloc[-1]
                    crescimento = (ultimo_ano.select_dtypes(include=[np.number]).mean() - primeiro_ano.select_dtypes(include=[np.number]).mean()) / primeiro_ano.select_dtypes(include=[np.number]).mean() * 100
                    st.write(f"{ramo}: Crescimento médio de {crescimento:.2f}% nos índices")
        else:
            st.error("Colunas necessárias não encontradas nos dados.")

    # Rodapé
    st.sidebar.text("Desenvolvido com Streamlit")
else:
    st.info("Por favor, faça o upload de um arquivo para começar a análise.")
