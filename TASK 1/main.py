from flask import Flask, render_template, request, redirect
import shortuuid

app = Flask(__name__)

url_database = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    original_url = request.form.get('url')
    if original_url:
        short_url = generate_short_url()
        url_database[short_url] = original_url
        return render_template('index.html', short_url=short_url)
    else:
        return render_template('index.html', error="Please enter a valid URL.")

@app.route('/<short_url>')
def redirect_to_original(short_url):
    if short_url in url_database:
        original_url = url_database[short_url]
        return redirect(original_url)
    else:
        return render_template('index.html', error="URL not found.")

def generate_short_url():
    return shortuuid.uuid()[:8]

if __name__ == '__main__':
    app.run(debug=True)
