from fastapi import FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import json, secrets
#from jsonschema import validate
from fastapi.responses import HTMLResponse
from urllib.request import urlopen
from typing import Optional
app = FastAPI()

@app.get("/", response_class=HTMLResponse, tags=['root'])
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

@app.get("/update", tags=['update'])
async def basic_update():
    update_db()
    return{'msg':'updated'}


#example: /books?author=Tolkien&publisheddate="2012-10-02"&sortkey=id
@app.get('/books', tags=['books'])
async def get_books(author:str = "", publisheddate:str = "", sortkey:str = "") -> list:

    booksFiltered = list(filter(
        lambda x: (author == "" or any(author.lower() in string.lower() for string in x["volumeInfo"]["authors"]))
        and  (publisheddate in x["volumeInfo"]["publishedDate"]   or  publisheddate == "")
        , get_all_local_books() ))

    reversedSorting = False
    if sortkey != '':
        if sortkey[0] == '-':
            sortkey = sortkey[1:]
            reversedSorting = True

    if sortkey in set().union(*(d.keys() for d in booksFiltered)):
        print(sortkey)
        booksFiltered = sorted(booksFiltered, key=lambda k: k[sortkey], reverse= reversedSorting )
    return booksFiltered
    #return list(filter(lambda x: ( author in authorq for authors in x["volumeInfo"]["authors"] ) , books))




@app.get('/books/{id}', tags=['books by ID'])
async def get_book_by_ID(id: str):
    data = open("data.json", 'r', encoding='utf-8')
    try:
        jsData = json.load(data)
        books = jsData['items']
        return [book for book in books if id == book["id"]]
    except:
        return  {"msg":"error occured!"}


@app.post('/db', tags=['post books'])
async def post_db(query: dict):
    #return list(query)[0]
    if type(query) != dict:
        return {"msg":"wrong argument"}
    if type(query[list(query)[0]]) != str:
        return {"msg":"error parsing"}
    
    booksFromNet = get_books_from_url(list(query)[0], query[list(query)[0]])
    localBooks = get_all_local_books()

    for book in booksFromNet:
        if any( book["id"] == localBook["id"] for localBook in localBooks ):
            print(book["id"] + ' is in database already')
        else:
            localBooks.append(book)
    
    save_books(localBooks)


def get_all_local_books():
    data = open("data.json", 'r', encoding='utf-8')
    try:
        jsData = json.load(data)
        books = jsData['items']
        return books
    except:
        return  {"msg":"error occured!"}



def update_db():
    json_url = urlopen('https://www.googleapis.com/books/v1/volumes?q=a')
    data = json.loads(json_url.read())
    save_books(data['items'])
    return{'msg':'updated'}


def get_books_from_url(param: str, value: object):
    url = 'https://www.googleapis.com/books/v1/volumes?' + param + "=" + value
    json_url = urlopen(url)
    data = json.loads(json_url.read())
    #missing key problem appeared, so it's manually fixed here:
    booksFromNet = data['items']
    for book in booksFromNet:
        if not "authors"  in book['volumeInfo'].keys():
            booksFromNet.remove(book)    
    return booksFromNet       


def save_books(books: list):
    #we don't want books with no authors at all!
    for book in books:
        if not "authors"  in book['volumeInfo'].keys():
            #print('key missing')
            books.remove(book)   
    data = {"items":books}  
    with open('data.json', 'w+') as outfile:
        outfile.truncate()
        json.dump(data, outfile)
        outfile.close()


