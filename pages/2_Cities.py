# Libraries

from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import folium

# Bibliotecas necessárias
import streamlit as st
import pandas as pd
from PIL import Image
from streamlit_folium import folium_static
from datetime import datetime

# import dataset

df = pd.read_csv('zomato.csv')

# Funções

#Tamanho da página
st.set_page_config(layout="wide")


#Preenchimento dos nomes dos países
COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}

def country_name(country_id):
    return COUNTRIES[country_id]

#Criação do Tipo de Categoaria de Comida

def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

# Criação do nome das cores
COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
}

def color_name(color_code):
    return COLORS[color_code]


#Remover as linhas duplicadas
df = df.drop_duplicates().reset_index(drop=True)

#Remover na
df = df.dropna()


# Incluindo coluna de nome de país
df['Country Code'] = df['Country Code'].map(COUNTRIES)

# CATEGORIZAR
df['Cuisines'] = df.loc[:, 'Cuisines'].apply(lambda x: x.split(',')[0])

# =============================================
# Barra lateral
# =============================================



st.sidebar.markdown("""___""")


image_path = 'logo.png'
image = Image.open(image_path)
st.sidebar.image( image, width=60 )
st.sidebar.title('Fome Zero')

#================= Filtros utilizando o Country Code ========
st.sidebar.title('Filtros')
country_options = st.sidebar.multiselect('Escolha os países abaixo', ['India','United States of America','England','South Africa','United Arab Emirates','New Zeland','Brazil','Australia', 'Canada','Turkey','Sri Lanka','Qatar','Philippines','Indonesia'], default='Brazil')
                                                                                      

#Filtro de Códigos dos países
linhas_selecionadas = df['Country Code'].isin( country_options )
df = df.loc[linhas_selecionadas, :]

#st.dataframe( df )

#cópia do dataframe
df1 = df.copy()


# =============================================
# Layout no streamlit
# =============================================

    
image_path3 = 'city.png'
image3 = Image.open(image_path3)
st.image( image3, width=60 )
st.title('Visão Cidades')
    
with st.container():
    st.markdown('Top 10 Cidades com mais Restaurantes na Base de Dados')
        
    restaurant_city = df.loc[:,['Restaurant ID','City']].groupby('City').nunique().reset_index().sort_values(by='Restaurant ID',ascending=False)
    r_city = restaurant_city.head(10)
     
        
    fig = px.bar( r_city , x='City', y='Restaurant ID' )
        
    st.plotly_chart( fig, use_container_width=True )

    
with st.container():
    col1, col2 = st.columns(2)
    with col1: 
        st.markdown('Top 7 Cidades com Restaurantes com média de avaliação acima de 4')
            
        acima4 = df['Aggregate rating'] >= 4
        df1 = df.loc[acima4, :]
        acima4_city = df1.loc[:,['City','Aggregate rating','Restaurant ID']].groupby('City').nunique().reset_index().sort_values(by='Aggregate rating',ascending=False)
            
        acima4_c = acima4_city.head(7)
         
            
        fig = px.bar( acima4_c , x='City', y='Restaurant ID' )
            
        st.plotly_chart( fig, use_container_width=True )
            
    with col2:
        st.markdown('Top 7 Cidades com Restaurantes com média de avalização abaixo de 2,5' )
            
        abaixo_2_5 = df['Aggregate rating'] <= 2.5

        df2 = df.loc[abaixo_2_5, :]

        abaixo_2_5_city = df2.loc[:,['City','Aggregate rating','Restaurant ID']].groupby('City').nunique().reset_index().sort_values(by='Aggregate rating',ascending=False)
            
        
        abaixo2_5city = abaixo_2_5_city.head(7)
            
            
        fig = px.bar( abaixo2_5city , x='City', y='Restaurant ID' )
            
        st.plotly_chart( fig, use_container_width=True )
            
            
with st.container():
    st.markdown('Top 10 Cidades com mais restaurantes com tipo culinários distintos')
    culinaria_city = df.loc[:, ['Cuisines','City']].groupby('City').nunique().reset_index().sort_values(by='Cuisines',ascending=False)
        
    top10_culinaria_city = culinaria_city.head(10)
        
    fig = px.bar( top10_culinaria_city, x='City', y='Cuisines' )
        
    st.plotly_chart( fig, use_container_width=True )
