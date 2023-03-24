"""Message model tests."""

from app import app
import os
from unittest import TestCase
from sqlalchemy.exc import IntegrityError
from datetime import datetime

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
            text="User 1 sample message",
        )

        m2 = Message(
            text="User 2 sample message",
        )


        # Builds the relationship for User -> Message
        u1.messages.append(m1)
        u2.messages.append(m2)

        db.session.add(m1, m2)
        db.session.commit()

        self.u1_id = u1.id
        self.u2_id = u2.id
        self.m1_id = m1.id
        self.m2_id = m2.id
        

        self.client = app.test_client()

    def tearDown(self):
        db.session.rollback()

    def test_create_new_message_success(self):
        m1 = Message.query.get(self.m1_id)
        self.assertIsInstance(m1, Message)


    def test_message_timestamp_success(self):
        m1 = Message.query.get(self.m1_id)
        self.assertIsInstance(m1.timestamp, datetime)

    def test_return_user_object_success(self):
        m2 = Message.query.get(self.m2_id)
        self.assertIsInstance(m2.user, User)

    