import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, distinct
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBsession = sessionmaker(bind = engine)
session = DBsession()

'''
#Print restaurants in alpha order
restaurants = session.query(Restaurant).order_by(Restaurant.name)
for restaurant in restaurants:
    print restaurant.name
'''

#only show menu items less than a certain price
#this doesn't really work because price is a string
items = session.query(MenuItem).filter(MenuItem.price < '$8').order_by(MenuItem.price)
for item in items:
    print item.name,"-",item.price,"-",item.restaurant.name


'''
#only print certain type of menu item
veg = session.query(MenuItem).filter_by(name = 'Veggie Burger')
for item in veg:
    print item.id
    print item.price
    print item.restaurant.name
    print item.description
'''
'''
#print all names of menu items
items = session.query(MenuItem).all()
for item in items:
    print item.name
    print item.price
'''
