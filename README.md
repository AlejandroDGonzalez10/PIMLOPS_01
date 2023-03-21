# PIMLOPS_01


## <h1 align=center> **PROYECTO INDIVIDUAL Nº1 DE HENRY LABS** </h1>

# <h1 align=center>"Sistema de recomendación de servicios de streaming" </h1>

## Contexto
La Empresa provee servicios de agregación de plataformas de streaming y necesita un sistema de recomendación para mejorar la experiencia del usuario. 

## Propuesta de trabajo
El proyecto sigue un enfoque iterativo basado en el ciclo de vida de los proyectos de **Machine Learning**. El objetivo es proporcionar un **MVP** en una semana. Para ello, se plantea la siguiente propuesta de trabajo:

## Arquitectura del proyecto
Realizamos el ETL, luego el EDA analizando lo que vimos relevante, procedimos a filtrar datos para el ML para posterior Deploy con su funcionamiento de consultas, lo realizamos en fastapi con render.

## Transformaciones de datos
El proceso completo de **ETL** se realizo en el archivo **ETL.ipynb**, la informacion procesada se guardo en la carpeta **processed_data**.
Se realizaron las siguientes transformaciones de datos segun se indica en 0-Consignas.md : 

+ Generar campo **`id`**: Cada id se compondrá de la primera letra del nombre de la plataforma, seguido del show_id ya presente en los datasets (ejemplo para títulos de Amazon = **`as123`**)

+ Los valores nulos del campo rating deberán reemplazarse por el string “**`G`**” (corresponde al maturity rating: “general for all audiences”

+ De haber fechas, deberán tener el formato **`AAAA-mm-dd`**

+ Los campos de texto deberán estar en **minúsculas**, sin excepciones

+ El campo ***duration*** debe convertirse en dos campos: **`duration_int`** y **`duration_type`**. El primero será un integer y el segundo un string indicando la unidad de medición de duración: min (minutos) o season (temporadas)

## Desarrollo de la API:  
 
Se utilizo el framework FastAPI para disponibilizar los datos de la empresa. Se han definido las siguientes consultas:  

+ Título con mayor duración con filtros opcionales de AÑO, PLATAFORMA Y TIPO DE DURACIÓN. (función get_max_duration(year, platform, duration_type)).  
+ Cantidad de títulos por plataforma con un puntaje mayor a XX en determinado año (la función get_score_count(platform, scored, year))
+ Cantidad de títulos por plataforma con filtro de PLATAFORMA. (La función get_count_platform(platform)).  
+ Actor que más se repite según plataforma y año. (La función get_actor(platform, year)).  

## Análisis exploratorio de datos:   
En el archivo **3-EDA.ipynb** se realizo el **EDA**, en la carpeta EDA se almacenaron las imagenes de este analisis, y un archivo EDA.pdf  
Se realizo un análisis exploratorio de datos para investigar las relaciones entre las variables de los datasets, detectar outliers o anomalías y explorar patrones interesantes. 

## Sistema de recomendación: 
En el archivo **Modelo.ipynb** se desarrollo el modelo de **Machine Learning**, 
Una vez finalizado el **ETL** y el **EDA**, se debe entreno un modelo de ML para armar un sistema de recomendación de películas para usuarios. El modelo es capaz de recomendar películas a un usuario dado su ID y una película. 

