from sqlalchemy.orm import Session
import os
from database import models
from AI.train import trainAI
from AI.search import search

def train_for_AI(db: Session, imgPath: str, imgName: str):
    vector = trainAI(imgPath)
    db_info = models.Vector(name = imgName, path=imgPath, vector = vector)
    db.add(db_info)
    db.commit()
    db.refresh(db_info)
    return "The information is saved"

def search_image(db: Session, imgPath: str):
    arrayVector = db.query(models.Vector).all()
    return search( arrayVectors = arrayVector, image_path = imgPath)

def get_all_image_and_name(db: Session, skip: int = 0, limit: int = 16):
    return db.query(models.Vector).offset(skip).limit(limit).all()

def update_name_image(db: Session, id: int, newName: str):
    db.query(models.Vector).filter_by(id=id).update({models.Vector.name: newName}) 
    db.commit()
    return f"Update susscess for id={id}"

def delete_info(db: Session, id: int):
    data = db.query(models.Vector).filter(models.Vector.id==id).first()
    if data:
        db.delete(data)
        db.commit()
        os.remove(data.path)
        return f"Delete susscess for {id} with name=\"{data.name}\""
    return f"Not found id={id}, so can not delete \"{data.name}\""