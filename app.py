#!/usr/bin/env python3
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
#mysql
app.config['SQLALCHEMY_DATABASE_URI']="mysql://root:root@127.0.0.1:3306/flask_products"
#mariadb
#app.config['SQLALCHEMY_DATABASE_URI']="mariadb+mariadbconnector://root:root@127.0.0.1:3306/flask_products"
db = SQLAlchemy(app)

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == "POST":
        productName = request.form["name"]
        productPrice = request.form["price"]
        productStock = request.form["quantity_in_stock"]
        db.session.execute("INSERT INTO products(name,price,quantity_in_stock) VALUES(:n,:p ,:s)",
                           {"n":productName,"p":productPrice,"s":productStock})
        db.session.commit()
        return redirect("/")
    else:
        products = db.session.execute("SELECT * FROM products")
        return render_template('index.html',products=products)
@app.route("/delete/<int:id>")
def delete(id):
    db.session.execute("DELETE FROM products WHERE id = :id",{"id":id})
    db.session.commit()
    return redirect("/")
@app.route("/update/<int:id>", methods=["GET","POST"])
def update(id):
    if request.method == "POST":
        productName = request.form["name"]
        productPrice = request.form["price"]
        productStock = request.form["quantity_in_stock"]
        db.session.execute("UPDATE products SET name= :n ,price= :p ,quantity_in_stock= :s WHERE id= :id",
                           {"n":productName,"p":productPrice,"s":productStock,"id":id})
        db.session.commit()
        return redirect("/")
if __name__ == "__main__":
   app.run(debug=True)
