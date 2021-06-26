from flask import Flask, redirect, url_for, render_template, request, session, flash
import requests
from flask_sqlalchemy import SQLAlchemy
import json

a = requests.get('https://api.nytimes.com/svc/books/v3//lists/names.json?&api-key=XsLIhP0Mg2Wr77ol3kIBaD81BdIsx9My')

print(a.status_code)
print(a.headers)
res = a.json()

chungus = []

# for x in range(0, len(res["results"])):
#     susmogus = (res["results"][x]["list_name"])
#     chungus.append(susmogus)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Python'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth.sqlite'
db = SQLAlchemy(app)


class auth(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), nullable=False, unique=True)
    password = db.Column(db.String(15), nullable=False)
    img = db.Column(db.String(100), nullable=True)


db.create_all()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        session['username'] = username

        if db.session.query(auth.id).filter_by(username=username).first() and db.session.query(auth.id).filter_by(
                password=password).first() is not None:
            return redirect(url_for('user'))
        elif username == '' or password == '':
            # return "გთხოვთ შეავსოთ ყველა ველი"
            flash("გთხოვთ შეავსოთ ყველა ველი")
        else:
            # return "უზერნეიმ ან პაროლი არასწორია"
            flash("უზერნეიმ ან პაროლი არასწორია", )

    return render_template('login.html')


@app.route('/Register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == '' or password == '':
            flash("გთხოვთ შეავსოთ ყველა ველი")
        else:
            b1 = auth(username=username, password=password,
                      img='https://i1.wp.com/researchictafrica.net/wp/wp-content/uploads/2016/10/default-profile-pic.jpg?fit=300%2C300&ssl=1')
            db.session.add(b1)
            db.session.commit()

    return render_template('Register.html')


@app.route('/user', methods=['POST', 'GET'])
def user():
    if request.method == 'POST':
        imglink = request.form['imglink']

        db.session.query(auth).filter(auth.username == session['username']).update({'img': imglink})
        db.session.commit()
        return render_template('user.html',img= db.session.query(auth).filter_by(username=session['username']).first().img)
    return render_template('user.html', img=db.session.query(auth).filter_by(username=session['username']).first().img)


@app.route('/<genrename>')
def userage(genrename):
    for x in range(0, len(res["results"])):
        susmogus = (res["results"][x]["list_name"])
        chungus.append(susmogus)

    genrename = genrename.replace(" ", "-")
    b = requests.get(
        f'https://api.nytimes.com/svc/books/v3//lists/current/{genrename}.json?&api-key=XsLIhP0Mg2Wr77ol3kIBaD81BdIsx9My')
    res2 = b.json()
    booklist = []
    bnum = len(res2['results']["books"])
    for y in range(0, len(res2['results']["books"])):
        booklist.append(res2["results"]["books"][y]["title"])

    return render_template("booknames.html", booklist=booklist, bnum=bnum, genrename=genrename)


@app.route('/book_info', methods=['GET', 'POST'])
def book_info():
    if request.method == 'POST':
        book_name = request.form["bookname"]
        c = requests.get(
            f'https://api.nytimes.com/svc/books/v3/reviews.json?title={book_name}&api-key=XsLIhP0Mg2Wr77ol3kIBaD81BdIsx9My')
        res3 = c.json()
        try:
            test = res3['results'][0]['book_title']
            flash("info", "info")
        except:
            flash("error")

        return render_template("Book Info.html", res3=res3)
    return render_template("Book Info.html")


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect("/")


@app.route('/Genre', methods=['GET', 'POST'])
def books():
    if request.method == 'POST':
        genre_name = request.form.to_dict()
        genre_name1 = list(genre_name.keys())[0]
        return redirect(f"/{genre_name1}")

    return render_template('books.html', chungus=chungus, length=len(chungus))


if __name__ == "__main__":
    app.run(debug=True)
