from flask_restx import Resource, Namespace
from decorators import auth_required, admin_required
from dao.model.genre import GenreSchema, Genre
from implemented import genre_service
from flask import request

genre_ns = Namespace('genres')


@genre_ns.route('/')
class GenresView(Resource):
    @auth_required
    def get(self):
        rs = genre_service.get_all()
        res = GenreSchema(many=True).dump(rs)
        return res, 200

    @admin_required
    def post(self):
        data = request.json
        new_genre = genre_service.create(data)
        return 'Created', 201


@genre_ns.route('/<int:gid>')
class GenreView(Resource):
    @auth_required
    def get(self, gid):
        r = genre_service.get_one(gid)
        sm_d = GenreSchema().dump(r)
        return sm_d, 200

    @admin_required
    def put(self, gid):
        data = request.json
        if "id" not in data:
            data["id"] = gid
        genre_service.update(data)
        return 'Updated', 204

    @admin_required
    def delete(self, gid):
        genre_service.delete(gid)
        return 'Deleted', 204
