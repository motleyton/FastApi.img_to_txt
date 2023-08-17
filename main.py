import os
from fastapi import FastAPI, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pytesseract
from PIL import Image
import io
import uvicorn


app = FastAPI()

app.mount("/templates", StaticFiles(directory="templates"), name="templates")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/extract_text", response_class=HTMLResponse)
async def extract_text(file: UploadFile):
    image_data = await file.read()
    image = Image.open(io.BytesIO(image_data))
    text = pytesseract.image_to_string(image, lang="rus")
    # Замените \n на HTML тег <br>
    html_text = text.replace("\n", "<br>")
    return html_text

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
