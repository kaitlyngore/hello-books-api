from flask import Blueprint, jsonify

class Book:
    def __init__(self, id, title, description):
        self.id = id
        self.title = title
        self.description = description

books = [
    Book(1, "Pride and Prejudice", "placeholder description"),
    Book(2, "Sense and Sensibility", "placeholder description"),
    Book(3, "Persuasion", "placeholder description")
]

books_bp = Blueprint("books", __name__, url_prefix="/books")

@books_bp.route("", methods = ["GET"])
def list_books():
    books_list = []
    for book in books:
        books_list.append({
            "id": book.id,
            "title": book.title,
            "description": book.description
        })
    return jsonify(books_list)

@books_bp.route("/<book_id>", methods = ["GET"])
def show_book(book_id):
    book_id = int(book_id)
    for book in books:
        if book_id == book.id:
            return {
                "id": book.id,
                "title": book.title,
                "description": book.description
                }
        else:
            return{
                "error": "book not found"
            }
