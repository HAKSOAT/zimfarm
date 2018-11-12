from bson import ObjectId
from flask import Blueprint, request, jsonify, Response
from jsonschema import validate, ValidationError
from celery.app.control import Inspect

from app import celery
from utils.mongo import Schedules
from . import authenticate, bson_object_id, errors


blueprint = Blueprint('workers', __name__, url_prefix='/api/workers')


@blueprint.route("/", methods=["GET"])
@authenticate
def list_workers(user: dict):
    inspect: Inspect = celery.control.inspect()
    return jsonify(inspect.ping())