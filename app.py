from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape import scrape_data
from datetime import datetime as dt

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars")


# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    last_updated = mongo.db.lastUpdate.find_one()
    latest_article = mongo.db.article.find_one()
    featured_image = mongo.db.featured_image.find_one()
    facts = mongo.db.facts.find_one()

    # Return template and data
    return render_template("index.html", last_updated=last_updated, latest_article=latest_article, featured_image=featured_image, facts=facts)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    article_title, article_teaser, featured_image_url, table_html, hemisphere_image_urls = scrape_data()

    mongo.db.article.update({}, {"title" : article_title, "teaser" : article_teaser}, upsert=True)
    mongo.db.featured_image.update({}, {"url" : featured_image_url}, upsert=True)
    mongo.db.facts.update({}, {"table_html" : table_html}, upsert=True)

    mongo.db.lastUpdate.update({}, {"last_updated": dt.now().strftime("%m/%d/%Y %H:%M")}, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
