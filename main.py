from fastapi import FastAPI
from typing import Union
import pandas as pd


app = FastAPI(title="Mi API de películas y series",
    version="1.0",
    description="Esta API permite buscar información sobre películas y series, hecha por Alejandro Gonzalez PIMLOps_01",
    docs_url="/docs",
)

@app.get("/Pelicula con mayor duración")

def get_max_duration(year:int=None, platform:str=None, duration_type:str=None):

       
    # Cargar el  dataframe que elavoramos con sus respectivas trasformaciones finales.
    df = pd.read_csv('./plataformascore.csv')
    
    # Retorna la película con mayor duración, filtrada por año, plataforma y tipo de duración.
    # Utilizando las funciones query() y idxmax() de Pandas para simplificar el código y mejorar la eficiencia.

    df_filtrado = df.copy()
    
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

@app.get("/Pelicula con mayor puntaje (numeros con decimal y rango de 3.34 min a 3.72 max)")

def get_score_count(platform:str,scored:float,year:int):
    
    df = pd.read_csv('./plataformascore.csv')
    # Cargar el dataframe de películas.
    movies_df = df

    # Filtrar las películas que pertenecen a la plataforma y al año especificados
    filtered_df = movies_df[(movies_df["platform"] == platform) & (movies_df["release_year"] == year)]

    # Verificar si la plataforma y el año existen en el DataFrame
    if filtered_df.empty:
        return {"message": "No se encontraron datos para la plataforma y/o año especificados."}

    # Contar la cantidad de películas con puntaje mayor al valor especificado
    count = filtered_df[filtered_df["score_mean"] > scored].shape[0]

    return int(count)

@app.get('/Cantidad de peliculas por plataforma')


def get_count_platform(platform:str):
    
      
    # Cargar el dataframe de películas.
    df = pd.read_csv('./plataformascore.csv')
    movies_df = df

    # Filtrar las películas que pertenecen a la plataforma especificada
    filtered_df = movies_df[movies_df["platform"] == platform]
 
    # Contar la cantidad de películas por plataforma
    count_by_platform = filtered_df["platform"].value_counts()

    return int(count_by_platform[platform])




@app.get('/Actor que mas se repite segun/{platform}/{year}')

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
