from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
import string
import random
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# MongoDB connection
client = MongoClient('mongodb://localhost:27017/')        
db = client['url_shortener']
urls_collection = db['urls']                                                                    

def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(random.choice(characters) for _ in range(6))
    link = urls_collection.find_one({'short_url': short_url})

    if link:
        return generate_short_url()
    else:
        return short_url

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['original_url']
        existing_url = urls_collection.find_one({'original_url': original_url})

        if existing_url:
            flash('This URL has already been shortened!')
            return render_template('index.html', short_url=existing_url['short_url'])

        short_url = generate_short_url()
        new_url = {
            'original_url': original_url,
            'short_url': short_url
        }
        urls_collection.insert_one(new_url)

        return render_template('index.html', short_url=short_url)

    return render_template('index.html')

@app.route('/<short_url>')
def redirect_to_url(short_url):
    link = urls_collection.find_one({'short_url': short_url})
    if link:
        return redirect(link['original_url'])
    else:
        return "URL not found", 404

# if __name__ == '__main__':
#     app.run(debug=True)











#https://tokyols.co.in/
    

#https://scholarships.punjab.gov.in/         




