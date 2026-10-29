import os
import uuid
from datetime import datetime
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl

from database import get_url_item, put_url_item

app = FastAPI(title="AWS Link Shortener API", version="1.0.0")

# Configuración de CORS para permitir solicitudes desde S3 u otros orígenes
origins = ["*"]  # En producción, reemplaza "*" por el dominio o bucket URL de S3

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLRequest(BaseModel):
    original_url: HttpUrl

@app.post("/shorten", status_code=status.HTTP_201_CREATED)
def create_short_url(payload: URLRequest, request: FastAPI):
    short_code = str(uuid.uuid4())
    created_at = datetime.utcnow().isoformat()
    original_url_str = str(payload.original_url)

    item = {
        "short_code": short_code,
        "original_url": original_url_str,
        "created_at": created_at
    }

    success = put_url_item(item)
    if not success:
        raise HTTPException(status_code=500, detail="No se pudo guardar el enlace en la base de datos.")

    # Construir la URL corta utilizando la IP/host de la solicitud o configuración
    base_url = str(request.base_url).rstrip("/")
    short_url = f"{base_url}/{short_code}"

    return {
        "short_code": short_code,
        "original_url": original_url_str,
        "short_url": short_url
    }

@app.get("/{short_code}")
def redirect_to_original(short_code: str):
    item = get_url_item(short_code)
    if not item:
        raise HTTPException(status_code=404, detail="Enlace no encontrado")
    
    original_url = item["original_url"]
    # Redirección HTTP 307 Temporary Redirect
    return RedirectResponse(url=original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)

@app.get("/urls/{short_code}")
def get_url_info(short_code: str):
    item = get_url_item(short_code)
    if not item:
        raise HTTPException(status_code=404, detail="Enlace no encontrado")
    return item