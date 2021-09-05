import logging
import typing

import requests
from sqlalchemy import Column, ForeignKey, UniqueConstraint, sql
from sqlalchemy import Integer, BigInteger, String, Text, LargeBinary, DateTime, Boolean, DECIMAL, Enum
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils import Timestamp
import enum


# Create a base class to define all the database subclasses
TableDeclarativeBase = declarative_base()

class UserStatus(enum.Enum):
    active = 1
    expired = 2


# Define all the database tables using the sqlalchemy declarative base
class User(TableDeclarativeBase):
    """A Telegram user who used the bot at least once."""

    # Telegram data
    user_id = Column(BigInteger, primary_key=True)
    name = Column(String)
    username = Column(String)
    language = Column(String, nullable=False)

    location_lat = Column(DECIMAL(15,10))
    location_lon = Column(DECIMAL(15,10))

    status = Column(Enum(UserStatus), nullable=False)
    # Current wallet credit
    credit = Column(Integer, nullable=False)

    access_token = Column(String, nullable=False)

    timestamp_created = Column(DateTime(timezone=True), server_default=sql.func.now())

    # Extra table parameters
    __tablename__ = "users"

    def __init__(self, user_id, name, username, language, status, credit, access_token):
        # Initialize the super
        super().__init__()
        # Get the data from telegram
        self.user_id = user_id
        self.name = name
        self.username = username
        self.language = language
        self.status = status
        # The starting wallet value is 0
        self.credit = credit
        self.access_token = access_token





class Admin(TableDeclarativeBase, Timestamp):
    """A greed administrator with his permissions."""

    # The telegram id
    user_id = Column(BigInteger, ForeignKey("users.user_id"), primary_key=True)
    user = relationship("User")
    # Permissions
    edit_products = Column(Boolean, default=False)
    receive_orders = Column(Boolean, default=False)
    create_transactions = Column(Boolean, default=False)
    display_on_help = Column(Boolean, default=False)
    is_owner = Column(Boolean, default=False)
    # Live mode enabled
    live_mode = Column(Boolean, default=False)

    timestamp_created = Column(DateTime(timezone=True), server_default=sql.func.now())

    # Extra table parameters
    __tablename__ = "admins"


