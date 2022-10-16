from flask import Flask, render_template, redirect, url_for # we'll use Flask to render a template, redirecting to another url, and creating a URL.
from flask_pymongo import PyMongo # we'll use PyMongo to interact with our Mongo database
import scraping # use the scraping code, we will convert from Jupyter notebook to Python.


# set up Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)
# app.config["MONGO_URI"] tells Python that our app will connect to Mongo using a URI, a uniform resource identifier similar to a URL.
# URI we'll be using to connect our app to Mongo. This URI is saying that the app can reach Mongo through our localhost server, using port 27017, using a database named "mars_app".

# define the route for the HTML page
@app.route("/")
def index():
   mars = mongo.db.mars.find_one() # uses PyMongo to find the "mars" collection in our database
   return render_template("index.html", mars=mars) # , mars=mars) tells Python to use the "mars" collection in MongoDB.

# Abobe function is what links our visual representation of our work, our web app, to the code that powers it.

# function will set up our scraping route
@app.route("/scrape") #defines the route that Flask we are using
def scrape():
   mars = mongo.db.mars # new variable that points to our Mongo database
   mars_data = scraping.scrape_all() # variable to hold the newly scraped data, referencing the scrape_all function in the scraping.py file
   mars.update_one({}, {"$set":mars_data}, upsert=True) # use the data we have stored in mars_data. The syntax used here is {"$set": data}. This means that the document will be modified ("$set") with the data in question
   #upsert=True. This indicates to Mongo to create a new document if one doesn't already exist, and new data will always be saved
   return redirect('/', code=302) # will navigate our page back to / where we can see the updated content

# we need for Flask is to tell it to run
   if __name__ == "__main__":
   app.run()