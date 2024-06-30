from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

comments = []


class Comment(BaseModel):
    text: str
    category: str


for i in range(1, 36):
    comment = Comment(text=f"Test comment {i}", category="positive" if i % 2 == 0 else "negative")
    comments.insert(0, comment)

templates = Jinja2Templates(directory="templates")


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/comments")
def read_comments(request: Request, page: int = 1, limit: int = 10):
    start = (page - 1) * limit
    end = start + limit
    pagination = comments[start:end]
    return templates.TemplateResponse("comments.html", {
        "request": request,
        "comments": pagination,
        "page": page,
        "limit": limit
    })


@app.post("/comments")
def post_comment(page: int = 1, limit: int = 10, text: str = Form(...), category: str = Form(...)):
    if category not in ["positive", "negative"]:
        raise HTTPException(status_code=400, detail="Category must be 'positive' or 'negative'")
    comment = Comment(text=text, category=category)
    comments.insert(0, comment)
    return RedirectResponse(url=f"/comments?page={page}&limit={limit}", status_code=303)
