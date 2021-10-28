from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)

CORS(app)


class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, name, price):
        self.name = name
        self.price = price

class PackageSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "price")

package_schema = PackageSchema()
packages_schema = PackageSchema(many=True)


@app.route("/package/add", methods=["POST"])
def add_package():
    name = request.json.get("name")
    price = request.json.get("price")

    record = Package(name, price)
    db.session.add(record)
    db.session.commit()

    return jsonify(item_schema.dump(record))

@app.route("/item/get", methods=["GET"])
def get_all_packages():
    all_packages = Package.query.all()
    return jsonify(packages_schema.dump(all_packages))


if __name__ == "__main__":
    app.run(debug=True)