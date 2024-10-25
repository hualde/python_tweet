import os
from flask import Flask, render_template, request, redirect, url_for, flash
import tweepy

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configuración de la API de Twitter
auth = tweepy.OAuthHandler(
    os.environ.get('TWITTER_API_KEY'),
    os.environ.get('TWITTER_API_SECRET')
)
auth.set_access_token(
    os.environ.get('TWITTER_ACCESS_TOKEN'),
    os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
)

api = tweepy.API(auth)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tweet', methods=['POST'])
def tweet():
    tweet_content = request.form['tweet_content']
    try:
        api.update_status(tweet_content)
        flash('Tweet publicado con éxito!', 'success')
    except tweepy.TweepError as e:
        flash(f'Error al publicar el tweet: {str(e)}', 'error')
    return redirect(url_for('home'))

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)