import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Employee, Address

engine = create_engine('sqlite:///employeeData.db')
Base.metadata.bind = engine
DBsession = sessionmaker(bind = engine)
session = DBsession()

newEmployee = Employee(name = "Frant T. Tank")
frankAddress = Address(street = "1000 Verona Rd.", zip = "53703", employee = newEmployee)
session.add(newEmployee)
session.add(frankAddress)
session.commit()

print session.query(Employee).all()
print session.query(Address).all()