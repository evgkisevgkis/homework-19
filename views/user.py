from flask import request
from flask_restx import Resource, Namespace
from implemented import user_service

user_ns = Namespace('users')


@user_ns.route('/')
class UserView(Resource):
    def post(self):
        data = request.json
        new_user = user_service.create(data)
        return 'Created', 201
