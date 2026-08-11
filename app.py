from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3, os
from datetime import datetime

app=Flask(__name__)
app.secret_key=os.getenv("SECRET_KEY","dev-change-me")
DB="giveaway.db"
ADMIN_PASSWORD=os.getenv("ADMIN_PASSWORD","change-me")

PETS=["Черепашка","Неон Кенгуру","Неон Фрост","Мега Единорог","Золотая Черепашка","Неоновая Пчела","Неоновый Дракон","Мега Кот","Мега Собака","Неоновый Единорог"]

def conn():
    c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; return c

def init():
    c=conn()
    c.execute("""CREATE TABLE IF NOT EXISTS claims(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT NOT NULL, pet TEXT NOT NULL,
      status TEXT NOT NULL DEFAULT 'pending',
      created_at TEXT NOT NULL)""")
    c.commit(); c.close()

@app.route("/")
def index(): return render_template("index.html",pets=PETS)

@app.post("/claim")
def claim():
    username=request.form.get("username","").strip()
    pet=request.form.get("pet","")
    if not username or len(username)>30 or pet not in PETS:
        flash("Проверь ник и выбранного питомца.")
        return redirect(url_for("index"))
    c=conn()
    cur=c.execute("INSERT INTO claims(username,pet,created_at) VALUES(?,?,?)",
                  (username,pet,datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    cid=cur.lastrowid; c.commit(); c.close()
    return render_template("success.html",username=username,pet=pet,claim_id=cid)

@app.route("/admin",methods=["GET","POST"])
def admin():
    if request.method=="POST" and request.form.get("password")==ADMIN_PASSWORD:
        session["admin"]=True
    if not session.get("admin"): return render_template("admin_login.html")
    c=conn(); rows=c.execute("SELECT * FROM claims ORDER BY id DESC").fetchall(); c.close()
    return render_template("admin.html",claims=rows)

@app.post("/admin/status/<int:cid>")
def set_status(cid):
    if not session.get("admin"): return redirect(url_for("admin"))
    s=request.form.get("status")
    if s in {"pending","processing","completed","rejected"}:
        c=conn(); c.execute("UPDATE claims SET status=? WHERE id=?",(s,cid)); c.commit(); c.close()
    return redirect(url_for("admin"))

@app.get("/admin/logout")
def logout(): session.clear(); return redirect(url_for("admin"))

init()
if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.getenv("PORT","5000")))
