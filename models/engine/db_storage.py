#!/usr/bin/python3
"""New engine DBStorage class"""
from models.base_model import BaseModel, Base
from models.city import City
from models.state import State
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from sqlalchemy import (create_engine)
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
import os


class DBStorage:
    """This class manages MySQL database for AirBnB"""
    __engine = None
    __session = None

    def __init__(self):
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            os.getenv("HBNB_MYSQL_USER"), os.getenv("HBNB_MYSQL_PWD"),
            os.getenv("HBNB_MYSQL_HOST"), os.getenv("HBNB_MYSQL_DB"),
            pool_pre_ping=True))
        if os.getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        """returns a dictionary
        Return:
            returns a dictionary of objects
        """
        obj_dict = {}
        if cls is None:
            for obj in self.__session.query(City, State, User, Place,
                                            Review, Amenity).all():
                key = "{}.{}".format(type(obj).__name__, obj.id)
                obj_dict[key] = obj
        else:
            for obj in self.__session.query(cls).all():
                key = "{}.{}".format(cls.__name__, obj.id)
                obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """add the object to the current database session
        Args:
            obj: given object
        """
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """delete the object from the current database session
        Args:
            obj: given object
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """create all tables in the database and the current database session
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """closes the current session to force reload
        """
        self.__session.close()
