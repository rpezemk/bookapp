from fastapi import Depends, FastAPI, HTTPException, status, Depends, Query
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import json, secrets
from jsonschema import validate
from fastapi.responses import HTMLResponse
from urllib.request import urlopen
from typing import Optional
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_items():
    return """
    <html>
        <head>
            <title>Hello, dear STX TEAM! <3</title>
        </head>
        <body>
            <h1>Welcome to my bookstore,  v=1/n, n-> inf</h1>
            <h2>it's done with FASTapi, it's so great!</h>
        </body>
    </html>
    """

@app.get("/update")
async def update():
    json_url = urlopen('https://www.googleapis.com/books/v1/volumes?q=Tolkien')
    data = json.loads(json_url.read())
    with open('data.json', 'w+') as outfile:
        outfile.truncate()
        json.dump(data, outfile)
        outfile.close()
    return{'msg':'updated'}


#example: /books?author=Tolkien&publisheddate="2012-10-02"&sortkey=id
@app.get('/books', tags=['hash'])
async def get_books(author:str = "", publisheddate:str = "", sortkey:str = "") -> list:
    data = open("data.json", 'r', encoding='utf-8')
    jsData = json.load(data)
    books = jsData['items']
    booksFiltered = [book for book in books if (author in book["volumeInfo"]["authors"] )]
    if sortkey in set().union(*(d.keys() for d in books)):
        booksFiltered = sorted(books, key=lambda k: k[sortkey] )
    return booksFiltered
    #return list(filter(lambda x: ( author in authorq for authors in x["volumeInfo"]["authors"] ) , books))

@app.get('/books/{id}')
async def get_book_by_ID(id: str):
    data = open("data.json", 'r', encoding='utf-8')
    try:
        jsData = json.load(data)
        books = jsData['items']
        return [book for book in books if id == book["id"]]
    except:
        return  {"msg":"error occured!"}


#Post -- post in form of {"key":"anyWord"}
@app.post("/hash", tags=["hash"])
async def put_hash(key:dict) -> dict:   
    data = open("data.json", encoding='utf-8')
    hashes = json.load(data)
    simple = [{"key":"abc"}, {"key":"def"}, {"key":"ghi"}]
    if list(filter(lambda x: x["key"] == key["key"], hashes)) != []:
        return {"msg":"key already exists!"}
    else:
        hashes.append({"id":7, "key":key["key"], "hash":encode(key["key"])})
    with open('data.json', 'w') as outfile:
        print(hashes)
        json.dump(hashes, outfile)
    return {"msg":"key added"}


def encode(key:str) -> str:
    return key.swapcase()

def decode(hash:str) -> str:
    key = hash.swapcase()

hashes = []

