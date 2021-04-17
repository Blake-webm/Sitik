from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from cloudipsp import Api, Checkout


# базовый дизайн был взят из Boodstrap
obb = Flask(__name__)
# Создаем настройку Sql
obb.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///BigShop.db"
obb.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(obb)
db_user = SQLAlchemy(obb)
# создание db


class Item_user(db.Model):
    id = db_user.Column(db.Integer, primary_key=True)
    name = db_user.Column(db.String(10), nullable=False)
    posward = db_user.Column(db.String(16), nullable=False)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    Text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return self.title


# делаем возможным отслеживание странички
@obb.route("/")
def home_index():
    items = Item.query.order_by(Item.title).all()
    return render_template("main_title.html", data=items)


# страничка о нас
@obb.route("/about")
def about_us():
    return render_template("aboutOfUs.html")


# страничка оплаты
@obb.route("/buy/<int:id>")
def buy(id):
    item = Item.query.get(id)

    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {
        "currency": "RUB",
        "amount": str(item.price) + "00"
    }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)


# ошибка удоления
@obb.route("/error_dalate")
def error_dalate():
    return render_template("error_dalate.html")


# удоление
@obb.route("/<int:id>/del")
def staf_del(id):
    item = Item.query.get_or_404(id)
    try:
        db.session.delete(item)
        db.session.commit()
        return redirect("/")
    except:
        return redirect("/error_dalate")


# ошибка создания
@obb.route("/error_craete")
def error_craete():
    return render_template("error_craete.html")


# страничка создания
@obb.route("/create", methods=['POST', "GET"])
def create():
    if request.method == "POST":
        title = request.form["title"]
        if int(request.form["price"]) > 0:
            price = request.form["price"]
        else:
            return redirect("/error_craete")
        Text = request.form["Text"]
        item = Item(title=title, price=price, Text=Text)
        try:
            db.session.add(item)
            db.session.commit()
            return redirect("/")
        except:
            return redirect("/create")
    else:
        return render_template("create.html")
# проверяем какой файл запускаеться


@obb.route("/<int:id>/update", methods=['POST', "GET"])
def post_update(id):
    arct = Item.query.get(id)
    if request.method == "POST":
        arct.title = request.form["title"]
        arct.price = request.form["price"]
        arct.Text = request.form["Text"]
        try:
            db.session.commit()
            return redirect("/")
        except:
            return redirect("При изменение пприкола произошла ошибка")
    else:
        return render_template("update.html", db=arct)

if __name__ == "__main__":
    obb.run(debug=True)