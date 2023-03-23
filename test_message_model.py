"""Message model tests."""

from app import app
import os
from unittest import TestCase
from sqlalchemy.exc import IntegrityError

from models import db, User, Message, Follows

os.environ['DATABASE_URL'] = "postgresql:///warbler_test"

db.drop_all()
db.create_all()


class MessageModelTestCase(TestCase):
    def setUp(self):
        Message.query.delete()
        User.query.delete()

        u1 = User.signup("u1", "u1@email.com", "password", None)
        u2 = User.signup("u2", "u2@email.com", "password", None)

        m1 = Message(
            text="This is a sample message",
            user_id=u1.id
        )

        m2 = Message(
            text="This is another sample message",
            user_id=u2.id
        )

        db.session.commit()
        self.u1_id = u1.id
        self.u2_id = u2.id
        self.m1_id = m1.id
        self.m2_id = m2.id

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    # Things to test:
        # - Creating a new message
        # - Timestamp is populated upon message creation
        # - New message can't be created without a user foreign key
        # - Message.user returns user object