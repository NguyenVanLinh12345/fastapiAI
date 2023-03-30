from typing import List
import os as _os
import fastapi as _fastapi
import time as _time

def select_image(directory_name: str, value: str) -> str:
   path = f"{directory_name}/{value}"
   return path

def _is_image(filename: str) -> bool:
   valid_extensions = (".png", ".jpg", ".jpeg", ".gif")
   return filename.endswith(valid_extensions)

def upload_image(directory_name: str, image: _fastapi.UploadFile):
   if _is_image(image.filename):
      timestr = _time.strftime("%Y%m%d-%H%M%S")
      image_name = timestr + image.filename.replace(" ", "-")
      with open(f"{directory_name}/{image_name}", "wb+") as image_file_upload:
         image_file_upload.write(image.file.read())

      return f"{directory_name}/{image_name}"
   
   return None