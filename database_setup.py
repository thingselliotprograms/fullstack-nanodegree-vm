import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurant'
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)



class MenuItem(Base):
    __tablename__ = 'menu_item'
    name = Column(String(80),nullable = False)
    id = Column(Integer, primary_key=True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer,ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'course': self.course,
        }






engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)


Base = declarative_base()

class Employee(Base):
    __tablename__ = 'employee'
    name = Column(String(250), nullable=False)
    id = Column(Integer, primary_key=True)

class Address(Base):
    __tablename__ = 'address'
    street = Column(String(80), nullable=False)
    zip = Column(String(5), nullable=False)
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer,ForeignKey('employee.id'))
    employee = relationship(Employee)

engine = create_engine('sqlite:///employeeData.db')
Base.metadata.create_all(engine)