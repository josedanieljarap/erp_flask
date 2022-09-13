import datetime
import time
from cs50 import SQL
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

db = SQL("sqlite:///ventas.db")

@app.route('/', methods=["POST", "GET"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        bodega = float(request.form.get("bodega", 0))
        panaderia = float(request.form.get("panaderia", 0))
        total = round(bodega + panaderia, 2)
        current_time = datetime.datetime.now()
        dia = current_time.day
        mes = current_time.month
        año = current_time.year
        hora = time.strftime("%H:%M:%S", time.localtime())
        db.execute("INSERT INTO historial (bodega, panaderia, total, dia, mes, año, hora)\
             VALUES(?,?,?,?,?,?,?)", bodega, panaderia, total, dia, mes, año, hora)
        return redirect("/")

@app.route('/history', methods=["GET"])
def history():
    full_table = db.execute("SELECT * FROM historial")
    return render_template("history.html", full_table=full_table)

@app.route('/delete', methods=["POST"])
def delete():
    id = request.form.get("id")
    if id :
        db.execute("DELETE FROM historial WHERE id = ?", id)
    return redirect("/history")
    