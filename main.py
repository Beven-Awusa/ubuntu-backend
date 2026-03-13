from typing import Union
import logging
import os

from fastapi import FastAPI #, Request, Depends
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
# from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from redis_om import get_redis_connection
import uvicorn

#from app.api.api_v1.routes.routes import router
#from app.db.database import engine #async_engines
#from app.model import model as models


app = FastAPI(title="UBUNTU-CROWDFUNDING WEB API", reload=True)

redis = get_redis_connection(
    host=os.getenv('REDIS_URL', 'redis'),
    port=6379,
    password=None,
    decode_responses=True
)

# Configure logging
logging.basicConfig(
    filename='v1.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app.mount('/staticfolder', StaticFiles(directory='staticfolder'), name='staticfolder')
templates = Jinja2Templates(directory="templates")

origins = [
  'http://localhost:3000',
  'http://localhost:3001',
  'http://localhost:5173',
  'http://localhost:5174'
]

app.add_middleware(
  CORSMiddleware,
  # SessionMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  
  allow_methods=['*'],
  allow_headers=['*'],
  # secret_key="my_secret_key_from_env"
)

@app.get("/")
async def read_root():
    logger.info("Root endpoint was called")
    return {"Hello": "World"}


@app.get("/items/{item_id}") 
async def read_item(item_id: int, q: Union[str, None] = None):
    logger.info(f"Item endpoint was called with item_id={item_id}")
    return {"item_id": item_id, "q": q}

#models.Base.metadata.create_all(engine)
#app.include_router(router)

if __name__ == "__main__":
    # uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug", reload=True) ## interchange when need be.
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="debug", reload=True)
