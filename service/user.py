import hmac
import jwt
import calendar
import datetime
from dao.user import UserDAO
import hashlib
import base64
from constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS, SECRET, ALGO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_all(self):
        return self.dao.get_all()

    def get_one(self, uid):
        return self.dao.get_one(uid)

    def get_by_username(self, username):
        return self.dao.get_by_username(username)

    def create(self, data):
        return self.dao.create(data)

    def update(self, data):
        return self.dao.update(data)

    def delete(self, uid):
        return self.dao.delete(uid)

    def generate_password(self, password):
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return base64.b64encode(hash_digest)

    def compare_passwords(self, other_password, another_password) -> bool:
        hashik = self.generate_password(other_password)
        return hmac.compare_digest(hashik, another_password)

    def generate_tokens(self, data):
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

    def check_token(self, token):
        try:
            jwt.decode(token, SECRET, algorithms=[ALGO])
            return True
        except Exception:
            return False
