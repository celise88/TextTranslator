from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from transformers import pipeline
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/", StaticFiles(directory="static", html=True), name="static")
templates = Jinja2Templates(directory="templates/")

pipe_flan = pipeline("text2text-generation", model="google/flan-t5-small")

@app.get("/", response_class=HTMLResponse)
def index_get(request: Request):
    inputLang = ["English", "French", "German", "Italian", "Spanish"]
    outputLang = ["English", "French", "German", "Italian", "Spanish"]
    return templates.TemplateResponse('index.html', context={'request': request, 'inputLang': inputLang, 'outputLang': outputLang})

@app.post("/", response_class=HTMLResponse)
async def index_post(request: Request, inputLang: str = Form(...), text: str = Form(...), outputLang: str = Form(...)):
    text = inputLang + ": Translate" + text + " " + outputLang + ": "
    result = await pipe_flan(text)
    return templates.TemplateResponse('index.html', context={'request': request, 'text': result})