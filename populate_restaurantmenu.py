import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBsession = sessionmaker(bind = engine)
session = DBsession()
FirstRestaurant = Restaurant(name = "Pizza Palace")
session.add(FirstRestaurant)
session.commit()
print session.query(Restaurant).all()

cheezepizza = MenuItem(name = "Cheeze Pizza", description = "Made with all natural cheeze", course = "Entree", price = "$5.99", restaurant = FirstRestaurant)
session.add(cheezepizza)
session.commit()
print session.query(MenuItem).all()