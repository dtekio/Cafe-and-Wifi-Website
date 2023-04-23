from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from sqlalchemy_serializer import SerializerMixin

app = Flask(__name__)
Bootstrap(app)


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///cafes.db"
db = SQLAlchemy(app)



class Cafe(db.Model, SerializerMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)


@app.route("/add", methods=["POST"])
def post_new_cafe():
    new_cafe = Cafe(
        name=request.form.get('name', type=str),
        map_url=request.form.get('map_url', type=str),
        img_url=request.form.get('img_url', type=str),
        location=request.form.get('location', type=str),
        seats=request.form.get('seats', type=str),
        has_toilet=request.form.get('has_toilet', type=bool),
        has_wifi=request.form.get('has_wifi', type=bool),
        has_sockets=request.form.get('has_sockets', type=bool),
        can_take_calls=request.form.get('can_take_calls', type=bool),
        coffee_price=request.form.get('coffee_price', type=str),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/')
def home():
    all_cafes = db.session.query(Cafe).all()
    cafes = [cafe.to_dict() for cafe in all_cafes]
    return render_template("index.html", cafes=cafes)


@app.route('/delete/<cafe_id>')
def delete_cafe(cafe_id):
    cafe_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
