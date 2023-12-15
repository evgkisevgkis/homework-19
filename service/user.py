import hmac
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

    def create(self, user_d):
        user_d["password"] = self.generate_password(user_d.get("password"))
        return self.dao.create(user_d)

    def update(self, data):
        return self.dao.update(data)

    def delete(self, uid):
        return self.dao.delete(uid)

    def generate_password(self, password):
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT.encode('utf-8'),
            PWD_HASH_ITERATIONS
        )

    def compare_passwords(self, other_password, another_password) -> bool:
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            another_password.encode('utf-8'),
            PWD_HASH_SALT.encode('utf-8'),
            PWD_HASH_ITERATIONS
        )
        return hmac.compare_digest(other_password, hash_digest)
