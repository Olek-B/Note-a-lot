from flask import Flask, render_template,redirect,request,url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["DEBUG"] = True

SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="AleBla",
    password="Lama1234",
    hostname="AleBla.mysql.pythonanywhere-services.com",
    databasename="AleBla$default",
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Info(db.Model):

    __tablename__ = "Info"

    id = db.Column(db.Integer, primary_key=True )
    name = db.Column(db.String(20))
    definition = db.Column(db.String(200))
    date = db.Column(db.String(10))

query = db.select([Info])

def get_data(searched=""):
    ret = ""
    for i in Info.query.filter(Info.name.ilike(f"%{searched}%")).all():
        print(i.name)
        ret += f'<div class="row"><h3>{i.name}</h3><h3>{i.date}</h3><span>{i.definition}</span></div>'
    return ret



@app.route("/")
def index():
    search = request.args.get('search')
    a=get_data(search)
    print(a)
    return render_template("index.html", dane=str(a))



@app.route("/add")
def adder():
    dane = """    <form action="/INSERTOR" method="post" id="myForm">
    <input type="text" name="nazwa" class="input-field">
    <input type="text" name="definicja" class="input-field">
    <input type="date" name="data" class="input-field">
    <button type="submit" class="submit-button">Stwórz</button>
</form>
"""
    return render_template("index.html", dane=dane)


@app.route('/INSERTOR',methods = ['POST'])
def dodaj():
    data = request.form
    print(data)
    name = data['nazwa']
    contents = data['definicja']
    date = data['data']
    data = Info(name=name,definition=contents,date=date)
    db.session.add(data)
    db.session.commit()
    return redirect(url_for('index'))




