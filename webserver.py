import sys
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func, distinct
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBsession = sessionmaker(bind = engine)
session = DBsession()

class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/delete"):
                idstr = self.path.split('/')[2]
                idint = int(idstr)
                delRestaurant = session.query(Restaurant).filter(Restaurant.id == idint).one()
                if delRestaurant != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output =""
                    output += "<html><body>"
                    output += "<h1>Are you sure you want to delete "+delRestaurant.name+"?</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action="+str(self.path)+">"
                    output += "<input name='deleteRestaurant' type='submit' value='Delete'></form>"
                    output += "</body></html>"
                    self.wfile.write(output)
                return

            if self.path.endswith("/edit"):
                idstr = str(str.split(str(self.path),'/')[2])
                idint = int(idstr)
                editrestaurant = session.query(Restaurant).filter(Restaurant.id == idint).one()
                if editrestaurant != []:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output =""
                    output += "<html><body>"
                    output += "<h1>"+editrestaurant.name+"</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action="+str(self.path)+">"
                    output += "<input name='editRestaurantName' type='text' placeholder='%s'>" % editrestaurant.name
                    output += "<input type='submit' value='Rename'></form>"
                    output += "</body></html>"
                    self.wfile.write(output)
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output =""
                output += "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><input name="newRestaurantName" type="text" placeholder="New Restaurant Name" ><input type="submit" value="Create"></form>'''
                output += "</body></html>"
                self.wfile.write(output)
                return
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output =""
                output += "<html><body>"
                output += "<h1>This is a list of restaurants.</h1>"
                output += "<a href='/restaurants/new'>Make a new restaurant</a>"
                items = session.query(Restaurant).all()
                for item in items:
                    output += "<h2>"+item.name+"</h2>"
                    output += "<h3><a href='/restaurants/"+str(item.id)+"/edit'>Edit</a>"
                    output += "<h3><a href='/restaurants/%s/delete'>Delete</a>" % item.id
                    output += "<br><br>"
                    
                output += "</body></html>"
                self.wfile.write(output)
                return
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output=""
                output += "<html><body>"
                output += "<h1>Hey Yah!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"></form>'''
                output += "</body></html>"
                self.wfile.write(output)
                return
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output=""
                output += "<html><body>"
                output += "<h1>Hola!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>Que quiere yo digo?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                return
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)


    def do_POST(self):
        try:
            if self.path.endswith("/delete"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                idstr = self.path.split('/')[2]
                idint = int(idstr)
                delRestaurant = session.query(Restaurant).filter(Restaurant.id == idint).one()
                if delRestaurant != []:
                    session.delete(delRestaurant)
                    session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()

                return

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurantContent = fields.get('editRestaurantName')
                renamedRestaurant = str(restaurantContent[0])
                idstr = str(str.split(str(self.path),'/')[2])
                idint = int(idstr)
                editRestaurant = session.query(Restaurant).filter(Restaurant.id == idint).one()
                if editRestaurant != []:
                    editRestaurant.name = renamedRestaurant
                    session.add(editRestaurant)
                    session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return

            if self.path.endswith("/restaurants/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurantContent = fields.get('newRestaurantName')
                newRestaurant = Restaurant(name = str(restaurantContent[0]))
                session.add(newRestaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
              
                return



            #self.send_response(301)
            #self.send_header('Content-type', 'text/html')
            #self.end_headers()
            #ctype, pdict = cgi.parse_header(
            #    self.headers.getheader('content-type'))
            #if ctype == 'multipart/form-data':
             #   fields = cgi.parse_multipart(self.rfile, pdict)
              #  messagecontent = fields.get('message')
            #output = ""
            #output += "<html><body>"
            #output += "<h2>Alright, how about this: </h2>"
            #output += "<h1> %s </h1>" % messagecontent[0]
            #output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            #output += "</body></html>"
            #self.wfile.write(output)
            #print output
        except:
            pass



def main():
    try:
        port = 8080
        server = HTTPServer(('',port), WebServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping server..."
        server.socket.close()

if __name__ == '__main__':
    main()