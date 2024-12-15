# Library Management API

RESTfull API for library management. The API manages a collection of books, and allows basic CRUD operations related to books and authors.

## Features

- Add a new book
- Retrieve a list of all books.
- Delete books by their ISBN.
- Update book details using the ISBN.
- Interactive API documentation using Swagger UI.

## Prerequisites

- Python 3.10 or higher.
- Docker.
- virtualenv.

## Getting Started
### Building and running the docker container
1. Clone the repository.

```bash
git clone https://github.com/maysam-asser/library-management-api
cd library-management-api
```

2. Buid docker container.

```bash
docker build -t library-management-api .
```

3. Run the container.

```bash
docker run -p 5000:5000 library-management-api
```

4. The API is now running on `http://localhost:5000`.

### Accessing the Swagger API documentation

After running the container, you can access the Swagger UI documentation by navigating to `http://localhost:5000/api-docs`.

---

## API Endpoints

| Endpoint        | Method | Description                                 |
| ---------------- | -------- | -------------------------------------------- |
| `/books/add`    | POST   | Add a new book to the collection.           |
| `/books/index`  | GET    | List all books in the collection.           |
| `/books/filter` | GET    | Search for books by author, year, or genre. |
| `/books/delete` | DELETE | Delete a book using its ISBN.               |
| `/books/update` | PUT    | Update a book's details using its ISBN.     |
| `/api-docs`     | GET    | Access the Swagger API documentation. 