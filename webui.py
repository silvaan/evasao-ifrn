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
    df = pd.read_csv('clean_data.csv')
    df['Código Curso'] = df['Código Curso'].astype(str)
    df['Ano de Ingresso'] = df['Ano de Ingresso'].astype(str)
    df['Período Atual'] = df['Período Atual'].astype(str)
    return df

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

    situacao_counts = df[df[situacao] == True].groupby(selected_variables).size()
    situacao_df = situacao_counts.reset_index(name='Quantidade')

    if valores == 'Porcentagens':
        total_counts = df.groupby(selected_variables).size()
        situacao_counts = 100 * (situacao_counts / total_counts)
        y_label = 'Porcentagem'
    else:
        y_label = 'Quantidade'

    situacao_df = situacao_counts.reset_index(name=y_label)

    fig = px.bar(
        situacao_df,
        x=selected_variables[0],
        y=y_label,
        color=None if len(selected_variables) == 1 else selected_variables[1],
        title=f'{y_label} de {situacao} por {" e ".join(selected_variables)}',
        barmode='group'
    )
    
    st.plotly_chart(fig)
