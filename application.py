# import modules
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__) #initialize app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' #create sqlite db in current directory
db = SQLAlchemy(app)

#object that handles api
class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    publisher = db.Column(db.String)

    def __repr__(self):
        return f"{self.book_name} - {self.author} - {self.publisher}"
    
    

@app.route('/')
def index():
    return '<h1>Hello!</h1>'

@app.route('/books')
def get_books():
    books = Books.query.all()

    output = []
    for book in books:
        book_data = {'title': book.book_name, 'author': book.author, 'publisher': book.publisher}
    
        output.append(book_data)

    return {"books" : output}

@app.route('./books/<id>')
def get_book(id):
    book = Books.query.get_or_404(id)
    return {"title": book.book_name, 'author': book.author, 'publisher': book.publisher}

@app.route('/books', methods=['POST'])
def add_book():
    book = Books(book_name=request.json['book_name'], author=request.json['author'], publisher=request.json['publisher'])
    db.session.add(book)
    db.session.commit()
    return {'id': book.id}


@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    book = Books.query.get(id)
    if book is None:
        return {"error": "not found"}
    db.session.delete(book)
    db.session.commit()
    return {"message": "yeet!@"}