"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


from app import app, CURR_USER_KEY
import os
from unittest import TestCase
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt

from models import db, User, Message, Follows

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

# Now we can import app


# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.drop_all()
db.create_all()
bcrypt = Bcrypt()

UNAUTHORIZED = 401
REDIRECT = 302
OK = 200


class UserModelTestCase(TestCase):
    def setUp(self):
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        u1.following.append(u2)

        db.session.flush()

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_user_get_routes_unauthorized(self):
        with self.client as c:

            resp = c.get("/users", follow_redirects=True)
            self.assertEqual(resp.request.path, "/")

            resp = c.get("/users/profile", follow_redirects=True)
            self.assertEqual(resp.request.path, "/")

            resp = c.get(f"/users/{self.u1_id}", follow_redirects=True)
            self.assertEqual(resp.request.path, "/")

            resp = c.get(
                f"/users/{self.u1_id}/liked_messages", follow_redirects=True)
            self.assertEqual(resp.request.path, "/")

            resp = c.get(f"/users/{self.u1_id}/followers",
                         follow_redirects=True)
            self.assertEqual(resp.request.path, "/")

            resp = c.get(f"/users/{self.u1_id}/following",
                         follow_redirects=True)
            self.assertEqual(resp.request.path, "/")

    def test_user_get_routes_authorized(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1_id

            resp = c.get("/users")
            self.assertEqual(resp.status_code, OK)

            resp = c.get("/users/profile", follow_redirects=True)
            self.assertEqual(resp.status_code, OK)

            resp = c.get(f"/users/{self.u1_id}", follow_redirects=True)
            self.assertEqual(resp.status_code, OK)

            resp = c.get(
                f"/users/{self.u1_id}/liked_messages", follow_redirects=True)
            self.assertEqual(resp.status_code, OK)

            resp = c.get(f"/users/{self.u1_id}/followers",
                         follow_redirects=True)
            self.assertEqual(resp.status_code, OK)

            resp = c.get(f"/users/{self.u1_id}/following",
                         follow_redirects=True)
            self.assertEqual(resp.status_code, OK)

    def test_user_post_routes_unauthorized(self):
        with self.client as c:

            u1 = User.query.get(self.u1_id)
            follow_id = u1.following[0].id
            resp = c.post(f"/users/follow/{follow_id}", follow_redirects=True)
            self.assertEqual(resp.request.path, "/")

            resp = c.post(
                f"/users/stop-following/{follow_id}", follow_redirects=True)
            self.assertEqual(resp.request.path, "/")

            resp = c.post("/users/profile", follow_redirects=True)
            self.assertEqual(resp.request.path, "/")

            resp = c.post("/users/delete", follow_redirects=True)
            self.assertEqual(resp.request.path, "/")

    def test_user_login_fail(self):
        with self.client as c:

            resp = c.post("/login",
                          data={"username": "u1",
                                "password": "wrong_password"
                                },
                          follow_redirects=True
                          )

            html = resp.get_data(as_text=True)
            self.assertIn("Invalid credentials", html)

    # def test_user_login_success(self):
    # def test_user_signup_fail(self):
    # def test_user_signup_success(self):
