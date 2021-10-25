from flask import Blueprint, jsonify, request, make_response
from app import db
from app.models.book import Book

# class Book:
#     def __init__(self, id, title, description):
#         self.id = id
#         self.title = title
#         self.description = description

# books = [
#     Book(1, "Pride and Prejudice", "placeholder description"),
#     Book(2, "Sense and Sensibility", "placeholder description"),
#     Book(3, "Persuasion", "placeholder description")
# ]

books_bp = Blueprint("books", __name__, url_prefix="/books")

@books_bp.route("", methods = ["GET", "POST"])
def list_books():
    if request.method == "POST":
        request_body = request.get_json()
        new_book = Book(title = request_body["title"],
                        description = request_body["description"])
        db.session.add(new_book)
        db.session.commit()

        return make_response(f"Book {new_book.title} successfully created", 201)
        
    elif request.method == "GET":
        books = Book.query.all()
        books_response = []
        for book in books:
            books_response.append(
                {
                    "id": book.id,
                    "title": book.title,
                    "description": book.description
                }
            )
        
        return jsonify(books_response)

@books_bp.route("/<book_id>", methods = ["GET", "PUT", "DELETE", "PATCH"])
def show_book(book_id):
    # book = Book.query.get(book_id)
    
    if request.method == "GET":
        book_id = int(book_id)
        book = Book.query.get(book_id)
        if book is not None:
            return {
                    "id": book.id,
                    "title": book.title,
                    "description": book.description
                    }
        else:
            return make_response("error: book not found", 404)

    elif request.method == "PUT":
        request_body = request.get_json()
        book_id = int(book_id)
        book = Book.query.get(book_id)

        if book is not None:
            book.title = request_body["title"]
            book.description = request_body["description"]

            db.session.commit()

            return make_response(f"Book #{book.id} successfully updated")

        else:
            return make_response("error: book not found", 404)
    
    elif request.method == "DELETE":
        book_id = int(book_id)
        book = Book.query.get(book_id)
        if book is not None:
            db.session.delete(book)
            db.session.commit()

            return make_response(f"Book #{book.id} successfully deleted")
        else:
            return make_response("error: book not found", 404)

    elif request.method == "PATCH":
        request_body = request.get_json()
        book_id = int(book_id)
        book = Book.query.get(book_id)
        if book is not None:
            if "title" in request_body:
                book.title = request_body["title"]
                db.session.commit()
            if "description" in request_body:
                book.description = request_body["description"]
                db.session.commit()

            return make_response(f"Book #{book.id} successfully updated")

        else:
            return make_response("error: book not found", 404)