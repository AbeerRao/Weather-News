import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, url_for

# Initializing the flask application
app = Flask(__name__)

# The base URLS
weatherURL = "https://weather.com/en-GB/weather/today/l/918056b2315d3502cd0e3a7b10b84db86fe78d885fb8c74b9d5c06ca748e9263"
foxNewsURL = "https://www.foxnews.com/"

# The headers
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.5 Safari/605.1.15"
}

# The home route
@app.route("/")
@app.route("/home")
# What does the user want?
def userWants():
    return render_template("home.html")

# The news route
@app.route("/news")
# Getting the news
def getNews():
    page = requests.get(foxNewsURL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    # Saving all the articles
    articles = []
    # Getting the headlines
    articlesGot = soup.find_all('h2', class_="title title-color-default")
    for article in articlesGot:
        articles.append(article.text)

    return render_template("news.html", articles=articles)

# The weather route
@app.route("/weather")
# Getting the weather
def getWeather():
    page = requests.get(weatherURL, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    # Getting the weather
    location = soup.find('h1', class_="_-_-components-src-organism-CurrentConditions-CurrentConditions--location--1YWj_").get_text().strip()
    time = soup.find('div', class_="_-_-components-src-organism-CurrentConditions-CurrentConditions--timestamp--1ybTk").get_text().strip()
    degrees = soup.find('span', class_="_-_-components-src-organism-CurrentConditions-CurrentConditions--tempValue--MHmYY").get_text().strip()
    rainDiv = soup.find('div', class_="_-_-components-src-organism-CurrentConditions-CurrentConditions--precipValue--2aJSf")
    for item in rainDiv.find_all('span'):
        rainChance = item.text
    # Printing the result
    return f"In {location} {time} the temp is {degrees} with {rainChance}"

if __name__ == '__main__':
    app.run(debug=True)
    print()