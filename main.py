from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
# базовый дизайн был взят из Boodstrap
obb = Flask(__name__)
# Создаем настройку Sql
obb.config['SQLALCHEMY DATABASE_URI'] = "sqlite:///BigShop.db"
db = SQLAlchemy(obb)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    isActive = db.Column(db.Boolean, default=True)

# делаем возможным отслеживание странички
@obb.route("/")
def home_index():
    return render_template("main_title.html")
# страничка о нас
@obb.route("/about")
def aboun_us():
    return render_template("aboutOfUs.html")
# проверяем какой файл запускаеться
if __name__ == "__main__":
    obb.run(debug=True)