import requests
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

logging.basicConfig(level=logging.INFO)


NOMINATIM_URL = os.environ.get("NOMINATIM_URL", "https://nominatim.openstreetmap.org")


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/v1/search")
def search(text: str):
    return read_item(text)

@app.get("/v1/autocomplete")
def autocomplete(text: str):
    return read_item(text)

def read_item(text: str):
    r= requests.get(
        f'{NOMINATIM_URL}/search', params={'q': text, 'format': 'geocodejson', 'addressdetails':1, 'limit':20, 'extratags':1}
    )
    if r.status_code!=200:
        logging.info(f'Status code from nominatim: {r.status_code}')
        return
    obj =r.json()
    for feature in obj['features']:
        feature['properties'] = feature['properties']['geocoding']
        properties=feature['properties']
        properties['label']=properties['name']
        properties['sub_label']=properties.get('city') or properties.get('county') or properties.get('state')
    return obj
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
