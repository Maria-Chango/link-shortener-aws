import os
import uuid
from datetime import datetime
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl

from database import get_url_item, put_url_item

# 1. PRIMERO SE CREA 'app'
app = FastAPI(title="AWS Link Shortener API", version="1.0.0")

# 2. LUEGO SE CONFIGURA EL CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLRequest(BaseModel):
    original_url: HttpUrl

# 3. Y AL FINAL VAN LAS RUTAS QUE USAN '@app'
@app.post("/shorten", status_code=status.HTTP_201_CREATED)
def create_short_url(payload: URLRequest):
    short_code = str(uuid.uuid4())[:8]
    created_at = datetime.utcnow().isoformat()
    original_url_str = str(payload.original_url)

    # Lógica de guardado...
    put_url_item(short_code, original_url_str)

    return {"short_code": short_code, "original_url": original_url_str}