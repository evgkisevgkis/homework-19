import calendar
import datetime

import jwt

from constants import ALGO, SECRET
from service.user import UserService
from flask import abort


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_tokens(self, username, password, is_refresh=False):
        user = self.user_service.get_by_username(username)

        if user is None:
            return abort(404)

        if not is_refresh:
            if not self.user_service.compare_passwords(user.password, password):
                return abort(404)

        data = {
            'username': user.username,
            'role': user.role
        }

        min30 = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=30)
        data['exp'] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, SECRET, algorithm=ALGO)

        day130 = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=130)
        data['exp'] = calendar.timegm(day130.timetuple())
        refresh_token = jwt.encode(data, SECRET, algorithm=ALGO)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    def refresh_tokens(self, refresh_token):
        data = jwt.decode(refresh_token, SECRET, [ALGO])
        username = data.get('username')
        return self.generate_tokens(username, None, is_refresh=True)
