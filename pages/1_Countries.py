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

with st.container():
    col1, col2 = st.columns(2)
    with col1:                    
        image_path2 = 'th.jpeg'
        image2 = Image.open(image_path2)
        st.image( image2, width=125 )
    with col2:
        st.header('Visão Países')
    
with st.container():
    st.header('Quantidade de Restaurantes Registrados por País')
    restaurant_for_country = (df.loc[:, ['Restaurant Name', 'Country Code']].groupby('Country Code')
                                .nunique()
                                .reset_index()
                                .sort_values(by='Restaurant Name', ascending=False))

        
    fig = px.bar(restaurant_for_country, x='Country Code', y='Restaurant Name')
        
    st.plotly_chart( fig, use_container_width=True )
        
    
with st.container():
    st.header('Quantidade de Cidades Registradas por País')
    city_countries = df.loc[:,['Country Code','City']].groupby('Country Code').nunique().reset_index().sort_values(by='City',ascending=False)

        
    fig = px.bar(city_countries, x='Country Code', y='City')
        
    st.plotly_chart( fig, use_container_width=True )
        
        
    
with st.container():
    col1, col2 = st.columns(2)
        
    with col1:
        st.markdown('Média de Avaliações feitas por País')
        rating_country_mean = df.loc[:, ['Country Code','Votes']].groupby('Country Code').mean().reset_index().sort_values(by='Votes', ascending=False)
            
                
        fig = px.bar(rating_country_mean, x='Country Code', y='Votes')
            
        st.plotly_chart( fig, use_container_width=True )
            
    with col2:
        st.markdown('Média de Preço de um prato para duas pessoas por País')
        avarage_country = df.loc[:,['Country Code','Average Cost for two']].groupby('Country Code').mean().reset_index().sort_values(by= 'Average Cost for two', ascending=False)
            
            
        fig = px.bar( avarage_country , x='Country Code', y='Average Cost for two' )
            
        st.plotly_chart( fig, use_container_width=True )
            