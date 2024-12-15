def process_isbn(isbn):
    return isbn.replace('-', '').replace(' ', '')

def validate_isbn(isbn):
    isbn = process_isbn(isbn)
    return (len(isbn) == 13 or len(isbn == 10)) and isbn.isdigit()

def get_book_by_isbn(isbn, books):
    for id, book_details in books.items():
        if book_details['isbn'] == isbn:
            return id, book_details
   
    return None, None