from flask import Flask, jsonify, request
from db import Database, generate_id
from utils import process_isbn, validate_isbn, get_book_by_isbn
import datetime
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)
db = Database('db.json')

@app.route('/books/add', methods=['POST'])
def add_book():
    # request data
    book_details = request.json
    title = book_details.get('title')
    author = book_details.get('author')
    year = book_details.get('published')
    isbn = book_details.get('isbn')
    genre = book_details.get('genre')

    # validation
    if not (title and author and isbn):
        return jsonify({'message': f'Book title, author and ISBN are required'}), 400
   
    if not isinstance(year, int) or year <= 0 or year > datetime.datetime.now().year:
        return jsonify({'message': 'Invalid year'}), 400
       
    if not validate_isbn(isbn):
        return jsonify({'message': 'Invalid ISBN'}), 400
   
    isbn = process_isbn(isbn)

    books = db.load()['books']

    if get_book_by_isbn(isbn, books)[0]:
        return jsonify({'message': 'Book already exists'}), 400
   
    id = generate_id()
    books[id] = {
        'title': title,
        'author': author,
        'published': year,
        'isbn': isbn,
        'genre': genre
    }
    db.save({'books': books})
   
    return jsonify({'message': 'Book added successfully'}), 201


@app.route('/books/index', methods=['GET'])
def list_all_bocks():
    books = db.load()['books']
    return jsonify(books)


@app.route('/books/filter', methods=['GET'])
def search_books():
    author = request.args.get('author')
    year = request.args.get('year', type=int)
    genre = request.args.get('genre')

    books = db.load()['books']
   
    filtered_books = [
        book_details for book_details in books.values() if (
            (not author or book_details['author'] == author) and
            (not year or book_details['published'] == year) and
            (not genre or book_details['genre'] == genre)
        )
    ]
    return jsonify(filtered_books)

@app.route('/books/delete', methods=['DELETE'])
def delete_book():
    isbn = request.args.get('isbn')
    if isbn and validate_isbn(isbn):
        isbn = process_isbn(isbn)
    else:
        return jsonify({'message': 'Invalid ISBN'}), 400

    books = db.load()['books']
    id = get_book_by_isbn(isbn, books)[0]

    if not id:
        return jsonify({'message': 'Book not found'}), 404
   
    del books[id]
   
    db.save({'books': books})
    return jsonify({'message': 'Book deleted successfully'}), 200

@app.route('/books/update', methods=['PUT'])
def update_book():
    isbn = request.args.get('isbn')
    if isbn and validate_isbn(isbn):
        isbn = process_isbn(isbn)
    else:
        return jsonify({'message': 'Invalid ISBN'}), 400

    books = db.load()['books']
    id = get_book_by_isbn(isbn, books)[0]
   
    if not id:
        return jsonify({'message': 'Book not found'}), 404

    book_details = request.json
    title = book_details.get('title')
    author = book_details.get('author')
    year = book_details.get('published')
    genre = book_details.get('genre')

    if year and (not isinstance(year, int) or year <= 0 or year > datetime.datetime.now().year):
        return jsonify({'message': 'Invalid year'}), 400

    if title:
        books[id]['title'] = title
    if author:
        books[id]['author'] = author
    if year:
        books[id]['published'] = year
    if genre:
        books[id]['genre'] = genre

    db.save({'books': books})
    return jsonify({'message': 'Book updated successfully'}), 200


SWAGGER_URL = '/api-docs'
API_URL = '/SwaggerDoc.yaml'

@app.route('/SwaggerDoc.yaml')
def swagger_yaml():
    with open('SwaggerDoc.yaml', 'r') as f:
        return f.read()

swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)