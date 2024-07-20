from flask import Flask, render_template, request, jsonify
import requests
import matplotlib
matplotlib.use('Agg')  # Utilise le backend Agg qui ne nécessite pas tkinter
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__,static_url_path='/static')

# Clé d'API TMDb (remplacez par votre propre clé)
API_KEY = '300066dea82222bd19ab8f7bf8ce47da'

@app.route('/')
def index():
    return render_template('index_movie.html')

@app.route('/search')
def search_movies():
    query = request.args.get('query')
    url = f'https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&language=fr&query={query}'
    
    try:
        response = requests.get(url) 
        data = response.json()
        
        movies = data['results']
        
        popularity_data = [movie['popularity'] for movie in movies]
        movie_titles = [movie['title'] for movie in movies]
        
        # Création de l'histogramme
        plt.figure(figsize=(10, 5))
        plt.hist(popularity_data, bins=10, edgecolor='black')
        plt.xlabel('Popularité')
        plt.ylabel('Nombre de Films')
        plt.title('Distribution de la Popularité des Films')
        
        img_hist = io.BytesIO()
        plt.savefig(img_hist, format='png')
        img_hist.seek(0)
        hist_url = base64.b64encode(img_hist.getvalue()).decode()
        plt.close()
        
        # Création du graphique en barres
        plt.figure(figsize=(14, 8))
        plt.barh(movie_titles, popularity_data, color='skyblue')
        plt.xlabel('Popularité')
        plt.ylabel('Films')
        plt.title('Popularité par Film')
        plt.gca().invert_yaxis()
        
        img_bar = io.BytesIO()
        plt.savefig(img_bar, format='png')
        img_bar.seek(0)
        bar_url = base64.b64encode(img_bar.getvalue()).decode()
        plt.close()

        return jsonify({
            'data': movies,
            'nombre_films': len(movies),
            'histogram': hist_url,
            'bar_chart': bar_url
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(port=1946,debug=True)
