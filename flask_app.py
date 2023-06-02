from flask import Flask, render_template, request, redirect, url_for
import os
import codecs


app = Flask(__name__)


def listuj_pliki(szukane, katalog):
    lista = {}
    for i in os.listdir(katalog):
        if szukane == "" or szukane == None or szukane in i:
            with codecs.open(f"{katalog}/{i}", "r", "utf-8") as f:
                a = f.read()
                lista[i[: len(i) - 4]] = a[0:200] + "..."
    dane = "<ul>"
    for i in lista:
        dane = dane + f"<li><a href='/notes/{i}'>{i}</a><span>{lista[i]}</span></li>"
    dane = dane + "</ul>"
    return dane


@app.route("/")
def index():
    searched = request.args.get("search")
    print(request.args.get("search"))
    dane = listuj_pliki(searched, "./notes")
    return render_template("index.html", dane=dane)


@app.route("/notes/<path:path>")
def subpage(path):
    exact_path = f"notes/{path}.txt"
    with codecs.open(exact_path, "r", "utf-8") as f:
        dane = f"<h2>{path}</h2><pre><span>{f.read()}</span></pre>"
    return render_template("index.html", dane=dane)



@app.route("/add")
def adder():
    dane = """    <form action="/INSERTOR" method="post" id="myForm">
    <input type="text" name="nazwa" class="input-field">
    <textarea name="notatka" id="" cols="30" rows="10" class="textarea-field"></textarea>
    <button type="submit" class="submit-button">Stwórz</button>
</form>
"""
    return render_template("index.html", dane=dane)


@app.route('/INSERTOR',methods = ['POST'])
def dodaj():
    data = request.form
    print(data)
    name = data['nazwa']
    conetnts = data['notatka']
    with open(f"./notes/{name}.txt","w")as f:
        f.write(conetnts)
    return redirect(url_for('index'))



















