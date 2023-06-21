#!/usr/bin/python3
"""This is the state class"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
import os


class State(BaseModel, Base):
    """This is the class for State
    Attributes:
        name: input name
    """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)

    if os.getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            citylist = []
            city_dict = models.storage.all(models.city.City)
            for key, value in city_dict.items():
                if value.state_id == self.id:
                    citylist.append(value)
            return citylist
    else:
        cities = relationship("City", backref="state",
                              cascade="all, delete-orphan")
