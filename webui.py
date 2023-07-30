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

# dashboard title
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

    # st.subheader('Selecionar situação')
    # situacao = st.selectbox('Situação', options=['Evasão', 'Retenção'], key='situacao')

    # st.subheader('Selecionar valores')
    # valores = st.selectbox('Valores', options=['Absolutos', 'Porcentagens'], key='valores')

    submit_button = st.form_submit_button(label='Aplicar')

if submit_button:
    selections = {'Campus': campus, 'Código Curso': curso, 'Período Atual': periodo_atual, 'Ano de Ingresso': ano}
    selected_variables = [key for key, value in selections.items() if value]

    if len(selected_variables) > 2:
        st.warning('Selecione apenas duas variáveis.')
        selected_variables = selected_variables[:2]

    # This is just a placeholder for further processing based on 'situacao' and 'valores'
    # You should implement the actual processing according to your specific requirements
    # st.write(f"Selected variables: {selected_variables}")
    # st.write(f"Selected situation: {situacao}")
    # st.write(f"Selected values: {valores}")

    df_situacao = df[df[situacao] == True]
    grouped_df = df_situacao.groupby(selected_variables).size().reset_index(name='Quantidade')

    # Create the plot
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
    
    # Show the plot
    st.plotly_chart(fig)



# with st.form(key='filter_form'):
#     col1, col2, col3 = st.columns(3)

#     with col1:
#         campus = st.checkbox('Campus', key='campus')
#     with col2:
#         curso = st.checkbox('Código Curso', key='curso')
#     with col3:
#         periodo_atual = st.checkbox('Período Atual', key='periodo_atual')

#     submit_button = st.form_submit_button(label='Aplicar')
    

# col1, col2 = st.columns(2)

# with col1:
#     show_percentage = st.checkbox('Mostrar porcentagem', key='show_percentage')
# with col2:
#     curso_ = st.checkbox('Código Curso', key='curso_')



# if submit_button:
#     selected_variables = []
#     if campus:
#         selected_variables.append('Campus')
#     if curso:
#         selected_variables.append('Código Curso')
#     if periodo_atual:
#         selected_variables.append('Período Atual')

#     if len(selected_variables) > 0:
#         df_melted = df.melt(id_vars=selected_variables, value_vars='Evasão')
#         fig = px.bar(df_melted, x='variable', y='value', color=selected_variables[0], barmode='group')
#         st.plotly_chart(fig)
#     else:
#         st.write("Please select at least one variable.")

# with st.form(key='filter_form'):
#     col1, col2, col3 = st.columns(3)

#     with col1:
#         campus = st.selectbox('Campus', options=['None'] + list(df['Campus'].unique()), key='campus')
#     with col2:
#         curso = st.selectbox('Curso', options=['None'] + list(df['Código Curso'].unique()), key='curso')
#     with col3:
#         periodo_atual = st.selectbox('Período Atual', options=['None'] + list(df['Período Atual'].unique()), key='periodo_atual')

#     submit_button = st.form_submit_button(label='Filter')

# if submit_button:
#     if campus != 'None':
#         df = df[df['Campus'] == campus]
#     if curso != 'None':
#         df = df[df['Código Curso'] == curso]
#     if periodo_atual != 'None':
#         df = df[df['Período Atual'] == periodo_atual]

# df = df[df['Evasão'] == True]
# fig = px.histogram(df, x='Campus')
# st.plotly_chart(fig)


# plt.figure(figsize=(10, 6))
# sns.countplot(x='Evasão', data=df)
# plt.title('Count Plot')
# st.pyplot(plt)

# df_count = df['Evasão'].value_counts().reset_index()
# df_count.columns = ['Evasão', 'Count']  # rename the columns
# fig = px.bar(df_count, x='Evasão', y='Count')
# st.plotly_chart(fig)

# fig = px.scatter(df, x='Campus', y='Ano de Ingresso', color='Sexo')
# st.plotly_chart(fig)

# df_evasao = df[df['Evasão'] == True]
# fig = px.histogram(df_evasao, x='Campus')
# st.plotly_chart(fig)


# top-level filters
# sex_filter = st.selectbox('Select the Job', pd.unique(df['Sexo']))

# # creating a single-element container
# placeholder = st.empty()

# # dataframe filter
# df = df[df['Sexo'] == sex_filter]

# st.markdown('### Detailed Data View')
# st.dataframe(df)