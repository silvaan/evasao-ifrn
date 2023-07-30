import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title='Evasão IFRN - Dashboard',
    page_icon='✅',
    # layout='wide',
)

@st.cache_data 
def load_data() -> pd.DataFrame:
    return pd.read_csv('clean_data.csv')

df = load_data()

st.title('Evasão IFRN')


with st.form(key='filter_form'):
    st.subheader('Filtrar')
    col1, col2 = st.columns(2)
    with col1:
        campus = st.checkbox('Campus', key='campus')
        curso = st.checkbox('Curso', key='curso')
    with col2:
        periodo_atual = st.checkbox('Período Atual', key='periodo_atual')
        ano = st.checkbox('Ano de Ingresso', key='ano')

    col1, col2 = st.columns(2)
    with col1:
        situacao = st.selectbox('Situação', options=['Evasão', 'Retenção'], key='situacao')
    with col2:
        valores = st.selectbox('Valores', options=['Absolutos', 'Porcentagens'], key='valores')

    submit_button = st.form_submit_button(label='Aplicar')

if submit_button:
    selections = {'Campus': campus, 'Código Curso': curso, 'Período Atual': periodo_atual, 'Ano de Ingresso': ano}
    selected_variables = [key for key, value in selections.items() if value]

    if len(selected_variables) > 2:
        st.warning('Selecione apenas duas variáveis.')
        selected_variables = selected_variables[:2]

    df_situacao = df[df[situacao] == True]
    grouped_df = df_situacao.groupby(selected_variables).size().reset_index(name='Quantidade')

    if len(selected_variables) == 1:
        fig = px.bar(
            grouped_df, 
            x=selected_variables[0], 
            y='Quantidade', 
            title=f'Quantidade de {situacao} por {selected_variables[0]}',
            barmode='group'
        )
    else:
        fig = px.bar(
            grouped_df, 
            x=selected_variables[0], 
            y='Quantidade', 
            color=selected_variables[1],
            title=f'Quantidade de {situacao} por {selected_variables[0]} e {selected_variables[1]}',
            barmode='group'
        )
    
    st.plotly_chart(fig)
