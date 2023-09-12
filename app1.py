import pandas as pd
import streamlit as st
import altair as alt
import datetime as dt
from PIL import Image


# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
page_title='DASHBOARD DE QUEIXAS DE SANEAMENTO DA MARÉ',
page_icon= '',
layout='wide',
initial_sidebar_state='expanded',
)
#with open ("style.css") as f:
    #st.markdown("<style>{f.read}</style>",unsafe_allow_html=True)
    
logo = Image.open('MENU.png')
st.image(logo)

###Criando o dataframe###
df = pd.read_csv('QueixasDash.csv', on_bad_lines='skip',usecols=['ano','Mes','Localidade','Categoria','Subcategoria'])
Categorias = pd.read_csv('CategoriasLocalidade.csv')
Subcategorias = pd.read_csv('Queixas_Localidade.csv')
Localidades = pd.DataFrame(df.groupby('Localidade')['Categoria'].count().reset_index()) 
Meses = pd.DataFrame(df.groupby('Mes')['ano'].count().reset_index()) 
###Criando o sidebar###

with st.sidebar:
    anos = list(df['ano'].unique())
    opcoes = anos[:]
    opcoes.append('Todos')
    fAno = st.selectbox('Selecione o ano:',opcoes)
    if fAno == 'Todos':
       fAno = df['ano']

           
        
            
fMes = df['Mes']      
              
fCategoria = df['Categoria']
    
fSubCategoria = df['Subcategoria']
     
fLocalidade = df['Localidade']
    

##### PADRÕES #########
cor_grafico = '#6A2691'

###Criando as tabelas####
tabAno = df.loc[(df['Mes'] == fMes) & 
                (df['ano'] == fAno)]
tabAno = tabAno.reset_index().sort_index()

tabCat = df.loc[(df['Categoria'] == fCategoria) & 
                (df['ano'] == fAno)]
tabCat = tabCat.reset_index().sort_index()

tabSub = df.loc[(df['Subcategoria'] == fSubCategoria)
                & (df['ano'] == fAno)]
tabSub = tabSub.reset_index().sort_index()

tabLoc = df.loc[(df['Localidade'] == fLocalidade) &
                (df['ano'] == fAno)]
tabLoc = tabLoc.reset_index().sort_index()


#--Criar os gráficos
#GRÁFICO 1. Queixas por mês-----
graf1_Ano = alt.Chart(tabAno).mark_bar(
        color = cor_grafico,
        cornerRadiusTopLeft= 3,
        cornerRadiusTopRight= 3
    ).encode(
    x = alt.X('Mes:O',title = 'Meses',
        sort =['janeiro','fevereiro','março','abril','maio','junho','julho','agosto','setembro','outubro','novembro','dezembro'],
        axis = alt.Axis(labelAngle= 45, labelColor= 'black',labelFontSize= 14)),     
    y = alt.Y('count():Q',title = 'Queixas'), 
    tooltip = ['Mes:O','count():Q']
    )
rotulo1 = graf1_Ano.mark_text(
        dy = -10,
        size = 14,
        color = "black"
    ).encode(
        text = 'count(Mes)'
    ).properties(height= 400,width= 200) 


#GRÁFICO 2. Queixas por favela-----

graf2_Localidade = alt.Chart(tabLoc).mark_bar(
    color = cor_grafico,
    cornerRadiusTopLeft= 3,
    cornerRadiusTopRight= 3
).encode(
    x = alt.X('count(Localidade)',title = 'Queixas',
              axis = alt.Axis(labelColor= 'black',labelFontSize= 14)),     
    y = alt.Y('Localidade',title ='Favela',sort = '-x',
            axis = alt.Axis(labelAngle= 0, labelColor= 'black',labelFontSize= 9)),
    tooltip= ['count(Localidade)','Localidade']
    )
   

rotulo2 = graf2_Localidade.mark_text(
    dx = 2,
    size = 14,
    align = 'left'
).encode(
    text = 'count(Localidade)'
).properties(height= 500,width= 200)

#GRÁFICO 3. Queixas por localidade e categoria-----

graf3_Categoria = alt.Chart(tabCat).mark_bar(
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

rotulo3 = alt.Chart(tabSub).mark_text(dx= -7, dy= 3,size =13,align = 'center',color='black').encode(
        x=alt.X('count(Categoria)', stack='normalize'),
        y=alt.Y('Localidade'),
        detail='Categoria',
        text= alt.Text('count(Categoria)', format='.0f')
)


#--Grafico 4.Queixas por localidade e subcategoria---
graf4_Subcategoria = alt.Chart(tabSub).mark_bar(
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
rotulo4 = alt.Chart(tabSub).mark_text(dx= -7, dy= 3,size= 13,align = 'center',color='black').encode(
        x=alt.X('count(Subcategoria)', stack='normalize'),
        y=alt.Y('Localidade'),
        detail='Subcategoria',
        text= alt.Text('count(Subcategoria)', format='.0f')
)
#--Criar as abas

tab1,tab2,tab3,tab4 = st.tabs(['Geral','Favela','Categoria','Subcategoria'])

with tab1:
    st.header('Queixas por mês')  
    st.altair_chart(graf1_Ano + rotulo1, use_container_width=True)

with tab2:
    st.header('Queixas por favela')
    st.altair_chart(graf2_Localidade + rotulo2, use_container_width=True)
with tab3:
    st.subheader('Queixas por Categoria')
    st.altair_chart(graf3_Categoria + rotulo3 ,use_container_width=True)
    st.write(Categorias,use_container_width = True)
with tab4:
    st.subheader('Queixas por Subcategoria')
    st.altair_chart(graf4_Subcategoria + rotulo4 ,use_container_width=True)
    st.write(Subcategorias,use_container_width = True)
