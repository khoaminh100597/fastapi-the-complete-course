from enum import Enum
from typing import Union, Optional
from fastapi import FastAPI

app = FastAPI()

BOOKS = {
    'book_1': {'title': 'Title One', 'author': 'Author One'},
    'book_2': {'title': 'Title Two', 'author': 'Author Two'},
    'book_3': {'title': 'Title Three', 'author': 'Author Three'},
    'book_4': {'title': 'Title Four', 'author': 'Author Four'},
    'book_5': {'title': 'Title Five', 'author': 'Author Five'}
}

class DirectionName(str, Enum):
    north = 'North'
    south = 'South'
    west = 'West'
    east = 'East'

@app.get('/')
async def read_all_books(skip_book: Optional[str] = None):
    new_books = BOOKS.copy()
    if skip_book:
        new_books.pop(skip_book)
    return new_books

@app.get('/directions/{direction_name}')
async def get_direction(direction_name: DirectionName):
    if direction_name is DirectionName.north:
        return {'Direction': direction_name.value, 'sub': 'Up'}
    if direction_name is DirectionName.south:
        return {'Direction': direction_name.value, 'sub': 'Down'}
    if direction_name is DirectionName.east:
        return {'Direction': direction_name.value, 'sub': 'Right'}
    if direction_name is DirectionName.west:
        return {'Direction': direction_name.value, 'sub': 'Left'}

@app.get('/{book_name}')
async def read_book(book_name: str):
    return BOOKS[book_name]

@app.post('/')
async def create_book(book_title, book_author):
    current_book_id = 0

    if len(BOOKS) > 0:
        for book in BOOKS:
            x = int(book.split('_')[-1])
            if x > current_book_id:
                current_book_id = x
    
    BOOKS[f'book_{current_book_id + 1}'] = {'title': book_title, 'author': book_author}
    return BOOKS[f'book_{current_book_id + 1}']

@app.put('/{book_name}/{book_title}/{book_author}')
async def update_book(book_name: str, book_title: str, book_author: str):
    book_information = {'title': book_title, 'author': book_author}
    BOOKS[book_name] = book_information
    return book_information  

@app.delete('/{book_name}')
async def delete_book(book_name):
    del BOOKS[book_name]
    return f'Book_{book_name} deleted.'

@app.get('/query/')
async def read_one_book(book_name: Optional[str] = None):
    if book_name in BOOKS:
        return BOOKS[book_name]
    return None

@app.delete('/query/')
async def delete_one_book(book_name: Optional[str] = None):
    if book_name in BOOKS:
        del BOOKS[book_name]
        return f'Book_{book_name} deleted'
    return None
