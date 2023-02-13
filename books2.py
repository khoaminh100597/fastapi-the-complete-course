from fastapi import FastAPI, HTTPException, Request, status, Form, Header
from typing import Union, Optional
from pydantic import BaseModel, Field
from uuid import UUID
from starlette.responses import JSONResponse

app = FastAPI()

class NegativeNumberException(Exception):
    def __init__(self, books_to_return):
        self.books_to_return = books_to_return

class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: Union[str, None] = Field(title='Description of the book', max_length=100, min_length=1)
    rating: int = Field(gt=-1, lt=101)

    class Config:
        schema_extra = {
            'example': {
                'id': 'fa44562b-f066-4f3c-a100-2e198ddc0f24',
                'title': 'Computer Science Pro',
                'author': 'Codingwithroby',
                'description': 'A very nice description of the book',
                'rating': 75
            }
        }

class BookNoRating(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: Union[str, None] = Field(default=None, title='Description of the book', max_length=100, min_length=1
    )

BOOKS = []

@app.exception_handler(NegativeNumberException)
async def negative_number_exception(request: Request, exception: NegativeNumberException):
    return JSONResponse(status_code=418, content={'message': f'Hey, why do you want {exception.books_to_return} '
                                                             f'books? You need to read more!'}
    )

@app.post('/books/login')
async def book_login(book_index: int, username: Union[str, None] = Form(), password: Union[str, None] = Form()):
    if username == 'FastAPIUser' and password == 'test1234!':
        return BOOKS[book_index]
    return 'Invalid user'

@app.get('/header')
async def read_header(random_header: Union[str, None] = Header(None)):
    return {'Random-Header': random_header}    

@app.get('/')
async def read_all_books(books_to_return: Optional[int] = None):
    if books_to_return and books_to_return < 0:
        raise NegativeNumberException(books_to_return=books_to_return)

    if len(BOOKS) < 1:
        create_book_no_api()
    
    if books_to_return and len(BOOKS) >= books_to_return > 0:
        i = 1
        new_books = []
        while i<= books_to_return:
            new_books.append(BOOKS[i - 1])
            i += 1
        return new_books
    return BOOKS

@app.get('/book/{book_id}')
async def read_book(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise raise_item_cannot_be_found_exception()

@app.get('/book/rating/{book_id}', response_model=BookNoRating)
async def read_book_no_rating(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise raise_item_cannot_be_found_exception()

@app.post('/', status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):
    BOOKS.append(book)
    return book

@app.put('/{book_id}')
async def update_book(book_id: UUID, book: Book):
    counter = 0

    for x in BOOKS:
        counter += 1 
        if x.id == book_id:
            BOOKS[counter - 1] = book
            return BOOKS[counter - 1]

@app.delete('/{book_id}')
async def delete_book(book_id: UUID):
    counter = 0 

    for x in BOOKS:
        counter +=1
        if x.id == book_id:
            del BOOKS[counter - 1]
            return f'{book_id} deleted'
    raise raise_item_cannot_be_found_exception()

def create_book_no_api():
    book_1 = Book(
        id='e130c2ec-8d3e-448e-a070-d637a3914bfc',
        title='Title 1',
        author='Author 1',
        description='Description 1',
        rating=60
    )
    book_2 = Book(
        id='fa44562b-f066-4f3c-a100-2e198ddc0f24',
        title='Title 2',
        author='Author 2',
        description='Description 2',
        rating=60
    )
    book_3 = Book(
        id='9e9c4aab-b64a-42b8-b4e8-5708d2be518b',
        title='Title 3',
        author='Author 3',
        description='Description 3',
        rating=60
    )
    book_4 = Book(
        id='71b550b0-a941-4df0-9c8a-c0e335af0e4a',
        title='Title 4',
        author='Author 4',
        description='Description 4',
        rating=60
    )
    BOOKS.extend([book_1, book_2, book_3, book_4])

def raise_item_cannot_be_found_exception():
    return HTTPException(status_code=404,
                         detail='Book not found',
                         headers={'X-Header_Error': 'Nothing to be seen at the UUID'})
    