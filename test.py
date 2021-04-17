import json

author = "tolkien"
publisheddate = "2012"

data = open("data.json", 'r', encoding='utf-8')

jsData = json.load(data)
books = jsData['items']


for book in books:
    for key in book:
        print(key)
        print(book[key])
        for k in book[key]:
            print(k['authors'])
    #print (book['volumeInfo'].keys())

    booksFiltered = list(filter(
        lambda x: (author == "" or any(author.lower() in string.lower() for string in x["volumeInfo"]["authors"]))
        and  (publisheddate in x["volumeInfo"]["publishedDate"]   or  publisheddate == "")
        , books ))


            #booksFiltered = [book for book in books if (author in book["volumeInfo"]["authors"] )]
    booksFiltered = list(filter(lambda x: ( author in author for authors in x["volumeInfo"]["authors"] ) , books))