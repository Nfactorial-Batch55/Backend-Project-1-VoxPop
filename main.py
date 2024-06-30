from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI()

comments = []


class Comment(BaseModel):
    text: str
    category: str


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
def post_comment(comment: Comment):
    if comment not in ["positive", "negative"]:
        raise HTTPException(status_code=400, detail="Comment must be either positive or negative")
    comments.append(comment)
    return comment
