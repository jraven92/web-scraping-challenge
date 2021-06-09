from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app =Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")


@app.route("/")
def index():
    mars_dict= mongo.db.mars.find.one()
    return render_template("index.html", mars_dict=mars_dict)

@app.route("/scrape")
def scrape():
    mars_dict = scrape_mars.scrape()
    mongo.db.mars.update({}, mars_dict, upsert=True)
    return redirect("/")
    
if __name__ == "__main__":
    app.run(debug=True)