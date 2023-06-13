from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
import requests
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from typing import Optional

# Configuración de HubSpot y ClickUp
HUBSPOT_API_KEY = "pat-na1-bfa3f0c0-426b-4f0e-b514-89b20832c96a"
CLICKUP_API_KEY = "pk_3182376_Q233NZDZ8AVULEGGCHLKG2HFXWD6MJLC"
CLICKUP_LIST_ID = "900200532843"

# Configuración de la base de datos PostgreSQL
POSTGRESQL_HOST = "db.g97.io"
POSTGRESQL_PORT = "5432"
POSTGRESQL_DB = "data_analyst"
POSTGRESQL_USER = "developer"
POSTGRESQL_PASSWORD = "qS*7Pjs3v0kw"

# Creación aplicación FastAPI
app = FastAPI()

# Definición del modelo de datos del contacto
class Contact(BaseModel):
    email: str
    firstname: str
    lastname: str
    phone: str
    website: str

# Definición del modelo de datos del registro de llamada
class APICall(BaseModel):
    timestamp: datetime
    endpoint: str
    parameters: Optional[dict]
    result: str

# Tabla en la base de datos
engine = create_engine(f"postgresql://{POSTGRESQL_USER}:{POSTGRESQL_PASSWORD}@{POSTGRESQL_HOST}:{POSTGRESQL_PORT}/{POSTGRESQL_DB}")
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class APICallLog(Base):
    _tablename_ = 'api_calls'

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    endpoint = Column(String)
    parameters = Column(String)
    result = Column(String)

# Definición de las funciones de sincronización con HubSpot y ClickUp
def sync_with_clickup(contact_id):
    
    for contacto in contactos_clickup:
        if contacto["id"] == contact_id and contacto["estado_clickup"]:
            return "Contacto ya sincronizado con ClickUp"
    
    url = f"https://api.clickup.com/api/v2/list/{CLICKUP_LIST_ID}/task"
    payload = {
        "name": f"Synced from HubSpot - Contact ID: {contact_id}"
    }
    headers = {
        "Authorization": CLICKUP_API_KEY
    }
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 201:
        return "Contact synced with ClickUp"
    else:
        return "Failed to sync contact with ClickUp"

def create_hubspot_contact(contact_data):
    url = "https