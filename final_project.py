from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, distinct
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBsession = sessionmaker(bind = engine)
session = DBsession()

@app.route('/')
@app.route('/restaurants/')
def restaurants():
    restaurantList = session.query(Restaurant).all()
    return render_template('restaurantList.html',restaurantList=restaurantList)

@app.route('/restaurant/new/', methods=['GET', 'POST'])
def createRestaurant():
    if request.method == 'POST':
        newrestaurant = Restaurant(name = request.form['name'])
        session.add(newrestaurant)
        session.commit()
        return redirect(url_for('restaurants'))
    else:
        return render_template('createRestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET','POST'])
def editRestaurant(restaurant_id):
    if request.method == 'POST':
        editrestaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
        editname = request.form['name']
        editrestaurant.name = editname
        session.add(editrestaurant)
        session.commit()
        return redirect(url_for('restaurants'))
    else:
        restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
        return render_template('editrestaurant.html', restaurant=restaurant)



@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
    return render_template('menu.html',restaurant=restaurant, items=items)
    
# Task 1: Create route for newMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET','POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(
            name=request.form['name'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash("New Menu Item Created!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)




# Task 2: Create route for editMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET','POST'])
def editMenuItem(restaurant_id, menu_id):
    if request.method =='POST':
        renameItem = session.query(MenuItem).filter_by(id=menu_id).one()
        if request.form['name']:
            renameName = request.form['name']
            renameItem.name = renameName
            session.add(renameItem)
            session.commit()
            flash("Menu Item Updated!")
            return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
        else:
            return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    else:
        restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
        item = session.query(MenuItem).filter_by(id=menu_id).one()
        return render_template('editmenuitem.html',restaurant=restaurant,chgItem=item)

# Task 3: Create a route for deleteMenuItem function here
@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        delItem = session.query(MenuItem).filter_by(id=menu_id).one()
        session.delete(delItem)
        session.commit()
        flash("Menu Item Deleted!")
        return redirect(url_for('restaurantMenu',restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html',restaurant_id=restaurant_id,item=item)

@app.route('/restaurants/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def menuItemJSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=item.serialize)



if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port= 5000)