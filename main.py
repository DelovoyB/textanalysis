from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from collections import Counter
from textblob import TextBlob
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

class TextInput(BaseModel):
    text: str

@app.get("/", response_class=HTMLResponse)
def read_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/analyze/")
async def analyze_text(request: Request, text: str = Form(None), form: bool = True):
    if text is None:
        try:
            data = await request.json()
            text = data.get("text")
            form = False
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid input format")

    if not text:
        raise HTTPException(status_code=400, detail="Text is required")

    word_count = len(text.split())
    char_count = len(text)

    print(f'{form=}')

    words = text.split()
    frequency = Counter(words).most_common(5)

    blob = TextBlob(text)
    sentiment = blob.sentiment

    result = {
        "word_count": word_count,
        "char_count": char_count,
        "frequency": dict(frequency),
        "polarity": "positive" if sentiment.polarity > 0.25 else "negative" if sentiment.polarity < -0.25 else "neutral",
        "subjectivity": "subjective" if sentiment.subjectivity > 0.5 else "objective",
    }

    if not form:
        return JSONResponse(result)
    else:
        return templates.TemplateResponse("result.html", {"request": request, "result": result})
