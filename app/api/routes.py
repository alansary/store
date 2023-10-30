from app.api import bp
from app.extensions import db
from flask_restful import Api
from flask_restful import Resource
from flask_restful import reqparse
from werkzeug.exceptions import BadRequest
from flask import make_response, jsonify
import datetime
import json
from bson import json_util


# Create the API
api = Api(bp)


# Create the products resource
class Products(Resource):
    def post(self):
        products_post_args = reqparse.RequestParser()
        products_post_args.add_argument(
            "title", type=str, required=True, help="Product title is required"
        )
        products_post_args.add_argument("description", type=str, required=False)
        products_post_args.add_argument("sku", type=str, required=True)
        products_post_args.add_argument(
            "images", type=str, required=False, action="append"
        )
        products_post_args.add_argument("video_link", type=str, required=False)
        products_post_args.add_argument("price", type=float, required=True)
        products_post_args.add_argument("quantity", type=int, required=False)

        try:
            args = products_post_args.parse_args()
            try:
                product = {
                    "title": args["title"],
                    "description": args["description"],
                    "sku": args["sku"],
                    "images": args["images"],
                    "video_link": args["video_link"],
                    "price": args["price"],
                    "quantity": args["quantity"],
                    "created_at": datetime.datetime.now(),
                }
                db.products.insert_one(product)

                # Get the record data
                record = json.loads(json_util.dumps(db.products.find(product).limit(1)))[0]

                return make_response(jsonify(record), 201)
            except Exception as e:
                return make_response(
                    jsonify({"error": f"An error occurred: {e._message}"}), 500
                )
        except BadRequest as e:
            return make_response(jsonify({"error": e.description}), e.code)

    def get(self):
        records = json.loads(json_util.dumps(db.products.find({})))
        return make_response(jsonify(records), 200)


api.add_resource(Products, "/products")
