from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from typing import List

app = FastAPI()

# Base de datos simulada
movies = [
    {
        "id": "7a1f3c55-01aa-4ec7-8cd3-b9a6f3e6d111",
        "title": "Inception",
        "duration": "148 min",
        "classification": "PG-13",
        "genre": "Ciencia ficcion",
        "imageName": "1.jpg",
        "showtimes": ["13:00", "16:30", "20:00"]
    },
    {
        "id": "56de9b49-bc08-4c17-9d3d-8d7d4d52c222",
        "title": "Interstellar",
        "duration": "169 min",
        "classification": "PG-13",
        "genre": "Drama espacial",
        "imageName": "2.jpg",
        "showtimes": ["12:15", "17:00", "21:10"]
    },
    {
        "id": "90a71d9e-d1f0-4df6-80f7-7a24f08bb333",
        "title": "The Dark Knight",
        "duration": "152 min",
        "classification": "PG-13",
        "genre": "Accion",
        "imageName": "3.jpg",
        "showtimes": ["14:00", "18:00", "22:00"]
    },
    {
        "id": "3d6d3c9e-7ad1-44d9-98bb-0bc465f4c444",
        "title": "Coco",
        "duration": "105 min",
        "classification": "A",
        "genre": "Animacion",
        "imageName": "4.jpg",
        "showtimes": ["11:00", "13:30", "16:00"]
    }
]

# Montar la carpeta estática para las imágenes
app.mount("/portadas", StaticFiles(directory="portadas"), name="portadas")

# Función para serializar y construir la URL completa de la imagen
def serialize_movie(request: Request, movie: dict):
    movie_copy = movie.copy()
    # request.base_url obtiene automáticamente el protocolo (http/https) y el dominio
    movie_copy["imageName"] = f"{request.base_url}portadas/{movie['imageName']}"
    return movie_copy

@app.get("/movies")
def get_movies(request: Request):
    return [serialize_movie(request, m) for m in movies]

@app.get("/movies/{movie_id}")
def get_movie(movie_id: str, request: Request):
    for movie in movies:
        if movie["id"] == movie_id:
            return serialize_movie(request, movie)

    # Retornar 404 si no se encuentra
    raise HTTPException(status_code=404, detail="Pelicula no encontrada")