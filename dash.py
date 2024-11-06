import streamlit as st
import pandas as pd
import plotly.express as px
from ajuda import abr_mes


st.set_page_config(
    page_title="Aula de monitoria",
    page_icon=":popcorn:",
    layout="wide",
    initial_sidebar_state="auto",
)

with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


#Função para carregar os dados
@st.cache_data
def carregar_dados():
    df = pd.read_csv('publico.csv')
    df['DATA_EXIBICAO'] = pd.to_datetime(df['DATA_EXIBICAO'])
    return df


df = carregar_dados()


#Sidebar
st.sidebar.title("Filtros")
st.sidebar.markdown('---')

#Filtro de data
ano = df['DATA_EXIBICAO'].dt.year.unique()
ano = sorted(ano)

anos_select = st.sidebar.multiselect('Selecione os anos:', ano,ano,placeholder="Selecione o ano")


df_filtrado = df[df['DATA_EXIBICAO'].dt.year.isin(anos_select)]

#Main
st.title('Dashboard de Filmes no Brasil')
st.divider()

col1, col2, col3 = st.columns([1,1,1])

publico_total = df_filtrado['PUBLICO'].sum()
filmes_mais_assistidos = df_filtrado.groupby('TITULO_BRASIL')['PUBLICO'].sum()
filmes_mais_assistidos = filmes_mais_assistidos.sort_values(ascending=False)
filme_mais_assistido = filmes_mais_assistidos.head(1)
agrupar_por_estado= df_filtrado.groupby('UF_SALA_COMPLEXO')['PUBLICO'].sum()


with col1:
    st.markdown("### Público Total")
    st.markdown(f'## {publico_total:,.0f}')

with col2:
    try:
        st.markdown("### Filme mais assistido")
        st.markdown(f'## {filme_mais_assistido.index[0]}')
        st.markdown(f'###### Público: {filme_mais_assistido[0]:,.0f}')
    except:
        st.markdown(f'###### Não há dados para o ano selecionado')
with col3:
    try:
        st.markdown("### Estado com maior público")
        estado_maior_publico = agrupar_por_estado.idxmax()
        publico_estado_maior = agrupar_por_estado.max()
        st.markdown(f'## {estado_maior_publico}')
        st.markdown(f'###### Público: {publico_estado_maior:,.0f}')
    except:
        st.markdown(f'###### Não há dados para o ano selecionado')

st.divider()

graf1, tab1 = st.columns([2,1])

with graf1:
    dados = df_filtrado
    dados['DATA_EXIBICAO'] = dados['DATA_EXIBICAO'].dt.month
    dados = dados.groupby('DATA_EXIBICAO')['PUBLICO'].sum().reset_index()
    dados['DATA_EXIBICAO'] = dados['DATA_EXIBICAO'].apply(abr_mes)
    fig = px.bar(dados,x='DATA_EXIBICAO',y='PUBLICO',labels={'DATA_EXIBICAO':'Mês de exibição','PUBLICO':'Público'},title='Público por mês')
    graf1.plotly_chart(fig,theme=None)

with tab1:
    tab1.markdown('### 10 Filmes mais assistidos')
    top10 = filmes_mais_assistidos.head(10).reset_index()
    top10.index += 1
    top10.columns = ['Filme','Público']
    tab1.write(top10)

st.divider()

col4, col5 = st.columns([1,2])

with col4:
   buscar_filme= col4.text_input('Busca por filme:',placeholder='Digite o nome do filme')
   dados = df_filtrado[df_filtrado['TITULO_BRASIL'].str.contains(buscar_filme,case=False)]
   dados = dados.groupby(['TITULO_BRASIL'])['PUBLICO'].sum().reset_index()
   if len(dados)>0:
       col5.dataframe(dados,hide_index=True,use_container_width=True)
   else:
       col5.write('Nenhum filme encontrado')


