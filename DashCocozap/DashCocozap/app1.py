import pandas as pd
import streamlit as st
import altair as alt
import datetime as dt
from PIL import Image


# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
page_title='DASHBOARD DE QUEIXAS DO COCOZAP',
page_icon= '',
layout='wide',
initial_sidebar_state='expanded',
)
#with open ("style.css") as f:
#st.markdown("<style>{f.read}</style>",unsafe_allow_html=True)
logo = Image.open('MENU.png')

st.image(logo)

#col1,col2,col3 = st.columns(3)

#with col1:
#st.metric('Queixas',322)
#with col2:
#st.metric('Favelas',16)
#with col3:
#st.metric('Categorias',6)


# --- Criar o dataframe
df = pd.read_csv('QueixasDash.csv', on_bad_lines='skip',usecols=['ano','Mes','Localidade','Categoria','Subcategoria'])
Categorias = pd.read_csv('CategoriasLocalidade.csv')
Subcategorias = pd.read_csv('Queixas_Localidade.csv')
Localidades = df.groupby('Localidade')['Categoria'].count().reset_index() 

##### PADRÕES #########
cor_grafico = '#6A2691'
#cor_grafico ='#9A7100'

#--Criar os gráficos

#GRÁFICO 1. Queixas por mês-----

graf1_Ano = alt.Chart(df).mark_bar(
    color = cor_grafico,
    cornerRadiusTopLeft= 3,
    cornerRadiusTopRight= 3
).encode(
    x = alt.X('Mes:O',title = 'Meses', sort =['janeiro','fevereiro','março','abril','maio',
            'junho','julho','agosto','setembro','outubro','novembro','dezembro'],
            axis = alt.Axis(labelAngle= 0, labelColor= 'black',grid= False,labelFontSize= 14)),
    y = alt.Y('count():Q',title = 'Queixas')
) 
rotulo1 = graf1_Ano.mark_text(
    dy = -10,
    size = 14,
    align = 'center'
).encode(
    text = 'count(Mes)'
).properties(height= 400,width= 200)

#GRÁFICO 2. Queixas por favela-----

graf2_Localidade = alt.Chart(df).mark_bar(
    color = cor_grafico,
    cornerRadiusTopLeft= 3,
    cornerRadiusTopRight= 3
).encode(
    x = alt.X('count()',title = 'Queixas'), 
    y = alt.Y('Localidade', title = 'Favelas',sort = '-x',  
            axis = alt.Axis(labelAngle= 0, labelColor= 'black',grid= False,labelFontSize= 11))
    )

rotulo4 = graf2_Localidade.mark_text(
    dx = 2,
    size = 14,
    align = 'left'
).encode(
    text = 'count(Localidade)'
).properties(height= 500,width= 200)

#GRÁFICO 3. Queixas por localidade e categoria-----

graf3_Categoria = alt.Chart(df).mark_bar(
    cornerRadiusTopLeft= 3,
    cornerRadiusTopRight= 3
).encode(
        x= alt.X('count(Categoria)',title = '%Queixas',stack = 'normalize', axis = alt.Axis(labelAngle= 0, labelColor= 'black',grid= False,labelFontSize= 11),
                sort =['Baixa do Sapateiro','Bento Ribeiro Dantas','Conjunto Esperança','Conjunto Pinheiros', 
                'Marcílio Dias','Morro do Timbau','Nova Holanda','Nova Maré','Parque Maré','Parque Rubens Vaz',
                'Parque União','Praia de Ramos','Roquete Pinto','Salsa e Merengue','Vila do João','Vila dos Pinheiros']),
        y= alt.Y('Localidade',title = 'Favelas', axis = alt.Axis(labelAngle= 0, labelColor= 'black',grid= False,labelFontSize= 11)),
color='Categoria'
).properties(height= 500,width= 200)


#--Grafico 4.Queixas por localidade e subcategoria---
graf4_Subcategoria = alt.Chart(df).mark_bar(
    cornerRadiusTopLeft= 3,
    cornerRadiusTopRight= 3
).encode(
    x= alt.X('count(Subcategoria)',title = '%Queixas',stack = 'normalize', axis = alt.Axis(labelAngle= 0, labelColor= 'black',grid= False,labelFontSize= 11),
             sort =['Baixa do Sapateiro','Bento Ribeiro Dantas','Conjunto Esperança','Conjunto Pinheiros',
            'Marcílio Dias','Morro do Timbau','Nova Holanda','Nova Maré','Parque Maré','Parque Rubens Vaz',
            'Parque União','Praia de Ramos','Roquete Pinto','Salsa e Merengue','Vila do João','Vila dos Pinheiros']),
    y= alt.Y('Localidade',title ='Favela', axis = alt.Axis(labelAngle= 0, labelColor= 'black',grid= False,labelFontSize= 11)),
    color ='Subcategoria' 
).properties(height= 500,width= 200
)

#--Criar as abas

tab1,tab2,tab3,tab4 = st.tabs(['Geral','Favela','Categoria','Subcategoria'])

with tab1:
    st.header('Queixas por mês')
    st.altair_chart(graf1_Ano + rotulo1, use_container_width=True)
with tab2:
    st.header('Queixas por favela')
    st.altair_chart(graf2_Localidade + rotulo4, use_container_width=True)
with tab3:
    st.subheader('Queixas por Categoria')
    st.altair_chart(graf3_Categoria,use_container_width=True)
    st.write(Categorias,use_container_width = True)
with tab4:
    st.subheader('Queixas por Subcategoria')
    st.altair_chart(graf4_Subcategoria,use_container_width=True)
    st.write(Subcategorias,use_container_width = True)
