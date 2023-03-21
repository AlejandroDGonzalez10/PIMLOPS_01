import pandas as pd
import streamlit as st
from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Configuración de título y descripción
st.title("Análisis exploratorio de plataformas de streaming")
st.write("Este proyecto tiene como objetivo realizar un análisis exploratorio de las plataformas de streaming más populares, incluyendo Netflix, Hulu, Amazon y Disney.")

# Descripción de cada plataforma de streaming
st.header("Descripción de las plataformas de streaming")
st.write("A continuación, se describe brevemente cada plataforma de streaming incluida en el análisis:")

st.write("- Netflix: una plataforma de streaming que ofrece una amplia variedad de películas y series de televisión, así como contenido original de Netflix.")
st.write("- Hulu: una plataforma de streaming que se centra en programas de televisión, con una selección de películas y contenido original de Hulu.")
st.write("- Amazon Prime Video: una plataforma de streaming que ofrece una variedad de películas, series de televisión y contenido original de Amazon.")
st.write("- Disney+: una plataforma de streaming que se centra en el contenido de Disney, incluyendo películas de Disney, Pixar, Marvel y Star Wars, así como contenido original de Disney+.")


def get_max_duration(year:int=None, platform:str=None, duration_type:str=None):

       
    # Cargar el  dataframe que elavoramos con sus respectivas trasformaciones finales.
    df = pd.read_csv('./plataformascore.csv')
    
    # Retorna la película con mayor duración, filtrada por año, plataforma y tipo de duración.
    # Utilizando las funciones query() y idxmax() de Pandas para simplificar el código y mejorar la eficiencia.

    df_filtrado = df
    
    if year:
        df_filtrado = df_filtrado.query('release_year == @year')
    if platform:
        df_filtrado = df_filtrado.query('platform == @platform')
    if duration_type:
        df_filtrado = df_filtrado.query('duration_type == @duration_type')

    # Obtenemos la película con la duración máxima
    max_duration_idx = df_filtrado['duration_int'].idxmax()
    titulo = df_filtrado.loc[max_duration_idx, 'title']

    return titulo


def get_score_count(platform:str,scored:float,year:int):
    
    df = pd.read_csv('./plataformascore.csv')
    # Cargar el dataframe de películas.
    movies_df = df

    # Filtrar las películas que pertenecen a la plataforma y al año especificados
    filtered_df = df[(df["platform"] == platform) & (df["release_year"] == year)]

    # Verificar si la plataforma y el año existen en el DataFrame
    if filtered_df.empty:
        return 0

    # Contar la cantidad de películas con puntaje mayor al valor especificado
    count = filtered_df[filtered_df["score_mean"] > scored].shape[0]

    return count



def get_count_platform(platform:str):
    
      
    # Cargar el dataframe de películas.
    df = pd.read_csv('./plataformascore.csv')
    movies_df = df

    # Filtrar las películas que pertenecen a la plataforma especificada
    filtered_df = movies_df[movies_df["platform"] == platform]
 
    # Contar la cantidad de películas por plataforma
    count_by_platform = filtered_df["platform"].value_counts()

    return int(count_by_platform[platform])





def get_actor3(platform: str, year: int):

    df = pd.read_csv('./plataformascore.csv')

    
    # Filtrar el DataFrame según plataforma y año
    df_filtered = df[(df['platform'] == platform) & (df['release_year'] == year)]
    
    # Verificar si el DataFrame filtrado no está vacío
    if len(df_filtered) == 0:
        return f"No se encontraron resultados para la plataforma {platform} en el año {year}"
    
    # Crear un diccionario para contar la cantidad de veces que aparece cada actor
    actor_count = {}
    for row in df_filtered.iterrows():
        cast = row[1]['cast']
        if isinstance(cast, str):
            actors = cast.split(',')
            for actor in actors:
                if actor in actor_count:
                    actor_count[actor] += 1
                else:
                    actor_count[actor] = 1
    
    # Verificar si el diccionario de conteo está vacío
    if len(actor_count) == 0:
        return f"No se encontraron actores para la plataforma {platform} en el año {year}"
    
    # Obtener el actor que más se repite
    max_actor = max(actor_count, key=actor_count.get)
    return max_actor


# Crear un título para la aplicación
st.title('Consultas de películas y series')

st.write('Bienvenido a la aplicación de consultas en el catálogo de servicios de streaming')

st.subheader('Duración máxima por año y plataforma')
year = st.number_input('Año', min_value=2000, max_value=2023, value=2020, step=1)
platform = st.selectbox('Seleccione una plataforma', ['amazon','disney','hulu','netflix'])
duration_type = st.selectbox('Tipo de duración', ['min', 'season'])
if st.button('Consultar 1'):
    result = get_max_duration(year, platform, duration_type)
    if isinstance(result, str):
        st.write(f'La duración máxima en {duration_type.lower()}s en {year} en {platform} es: {result}.')
    else:
        st.write(result)


st.subheader('Títulos por puntuación')
# Título de la página
st.title('Películas por Puntuación')

# Selección de plataforma, año y puntaje
platform = st.selectbox('Plataforma:', ['amazon', 'disney', 'hulu', 'netflix'])
year = st.number_input('Año:', min_value=2000, max_value=2023, value=2020, step=1)
scored = st.slider('Puntaje mínimo:', min_value=3.34, max_value=3.72, value=3.50, step=0.01)

# Botón de consulta
if st.button('Consulta 2'):
    result = get_score_count(platform, scored, year)
    st.write(f'Hay {result} películas en {platform} con una puntuación mayor a {scored} en {year}.')

st.subheader('Número de títulos en una plataforma dada')
platform = st.selectbox('Seleccione una plataforma' + str(year), ['amazon','disney','hulu','netflix'])
if st.button('Consultas 3'):
    result = get_count_platform(platform)
    st.write(f'Hay {result} títulos en {platform}.')




st.subheader('Actor con más apariciones en una plataforma y año determinados')
platform = st.selectbox(f'Seleccione una plataforma ({year})', ['amazon', 'disney', 'hulu', 'netflix'])
year = st.number_input('Año', min_value=2000, max_value=2022, value=2020, step=1)
if st.button('Consultar 4'):
    result = get_actor3(platform, year)
    if isinstance(result, str):
        st.write(result)
    else:
        st.write(f'El actor con más apariciones en {platform} en {year} es {result["actor"]}, con {result["appearances"]} apariciones.')






# Carga de datos

@st.cache(persist=True)
def load_data(platform):
    df = pd.read_parquet('archivoparquetsinnulos.parquet')
    return df

# Definir el lector de Surprise
reader = Reader(rating_scale=(1, 10))

# Crear el dataset de Surprise
data = Dataset.load_builtin('ml-100k', reader)

# Entrenar modelo KNN con Mean
trainset = data.build_full_trainset()
sim_options = {'name': 'pearson_baseline', 'user_based': False}
algo = KNNWithMeans(sim_options=sim_options)
algo.fit(trainset)

# Función para obtener recomendaciones
def get_recommendations(user_id, platform, n=10):
    # Cargar los datos de la plataforma
    df = load_data(platform)
    # Obtener los títulos de las películas calificadas por el usuario
    rated_titles = list(df[df['user_id'] == user_id]['title'].unique())
    # Obtener las predicciones para los items no calificados del usuario
    unrated_items = df[~df['title'].isin(rated_titles)]
    unrated_items = list(unrated_items['title'].unique())
    predictions = [algo.predict(user_id, item) for item in unrated_items]
    # Ordenar las predicciones por la calificación estimada
    predictions.sort(key=lambda x: x.est, reverse=True)
    # Devolver los títulos de las películas recomendadas
    return [pred.iid for pred in predictions[:n]]

# Interfaz de Streamlit
st.title('Sistema de recomendación de streaming')
st.write('Ingrese su ID de usuario:')
user_id = st.number_input('', value=1, step=1)
platform = st.selectbox('Seleccione la plataforma', ('Netflix', 'Hulu', 'Amazon', 'Disney'))
if st.button('Obtener recomendaciones'):
    recommendations = get_recommendations(user_id, platform.lower())
    st.write('Recomendaciones:')
    for title in recommendations:
        st.write('-', title)



# Carga de datos
streaming_df = pd.read_parquet('new_df2.parquet')


# Definir el lector de Surprise
reader = Reader(rating_scale=(1, 10))

# Crear el dataset de Surprise
data = Dataset.load_from_df(streaming_df[['userId', 'title', 'score']], reader)

# Entrenar modelo SVD
trainset, testset = train_test_split(data, test_size=.25)
algo = SVD()
algo.fit(trainset)

# Función para obtener recomendaciones
def get_recommendations(user_id, n=10):
    # Obtener predicciones para los items no calificados del usuario
    unrated_items = streaming_df[~streaming_df['title'].isin(trainset.ur[user_id])]
    unrated_items = list(unrated_items['title'].unique())
    predictions = [algo.predict(user_id, item) for item in unrated_items]
    # Ordenar las predicciones por la calificación estimada
    predictions.sort(key=lambda x: x.est, reverse=True)
    # Devolver los títulos de las películas recomendadas
    return [pred.id for pred in predictions[:n]]

# Interfaz de Streamlit
st.title('Sistema de recomendación de streaming')
st.write('Ingrese su ID de usuario:')
user_id = st.number_input('', value=1, step=1)
if st.button('Obtener recomendaciones'):
    recommendations = get_recommendations(user_id)
    st.write('Recomendaciones:')
    for title in recommendations:
        st.write('-', title)