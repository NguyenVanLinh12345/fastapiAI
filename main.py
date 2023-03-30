import fastapi as _fastapi
from fastapi import Depends
from fastapi.middleware.cors import CORSMiddleware
import fastapi.responses as _response
from sqlalchemy.orm import Session

import services as _services
from database.database import SessionLocal, engine
from database import models
from database import schemas
from crud import train_for_AI, search_image, get_all_image_and_name, update_name_image, delete_info

#--------------------
# e:
# cd Pictures\FastAPI_AI
# .\env\scripts\activate
# uvicorn main:app --reload

models.Base.metadata.create_all(bind=engine)

app = _fastapi.FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


origins = ["http://127.0.0.1:5500"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)  

@app.get('/imageStore/{value}')
def getProductImg(value: str):
  image_path = _services.select_image('imageStore', value)
  return _response.FileResponse(image_path)

@app.post('/trainAI')
async def TrainByImage(image: _fastapi.UploadFile = _fastapi.File(...), text: str = _fastapi.Form(...), db: Session = Depends(get_db)):
  path_location = _services.upload_image("imageStore", image)
  if path_location is None:
    return _fastapi.HTTPExceopton(status_code=409, detail ="incorrect file type")
   
  message = train_for_AI( db, imgPath = path_location, imgName = text )
  return {"message": message}

@app.post('/searchImage')
async def SearchByImage(image: _fastapi.UploadFile = _fastapi.File(...), db: Session = Depends(get_db)):
  path_location = f"temp/imageSearch.jpg"
  with open(path_location, 'wb') as file_object:
    file_object.write(image.file.read())
  message = search_image(db, path_location)

  return {"message": message}

@app.get('/getImage/skip={skip}&limit={limit}', response_model= list[schemas.Info])
def getImage(skip: int = 0, limit: int = 16, db: Session = Depends(get_db),):
  return get_all_image_and_name(db, skip=skip, limit=limit)

@app.put('/update/id={id}')
def updateName(id: int, newName: str, db: Session = Depends(get_db)):
   message = update_name_image(db, id=id, newName=newName)
   return {"message": message}

@app.delete('/delete/id={id}')
def delete(id: int, db: Session = Depends(get_db)):
  message = delete_info(db, id=id)
  return {"message": message}