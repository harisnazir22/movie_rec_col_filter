from flask import Flask, render_template, request, jsonify
import pickle

app = Flask(__name__)

@app.route('/get_movie_list')
def get_movie_list():
    # Load movies list
    with open("movies_list.pkl", 'rb') as f:
        movies_list = pickle.load(f)
    # Get the list of movie titles
    movie_titles = movies_list['title'].tolist()
    return jsonify(movie_titles)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/recommendation', methods=['POST'])
def recommendation():
    search_movie_title = request.form['search_movie']
    
    # Load movies list
    with open("movies_list.pkl", 'rb') as f:
        movies_list = pickle.load(f)
    
    # Load similarity data
    similarity = pickle.load(open("similarity.pkl", 'rb'))
    
    # Find the most similar movies to the searched movie
    if search_movie_title in movies_list['title'].values:
        selected_movie_index = movies_list.index[movies_list['title'] == search_movie_title].tolist()[0]
        distance = sorted(list(enumerate(similarity[selected_movie_index])), reverse=True, key=lambda vector: vector[1])
        recommend_movie = [movies_list.iloc[i[0]]['title'] for i in distance[1:6]]
        return render_template('recommendation.html', recommend_movie=recommend_movie)
    else:
        return "Movie not found."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)





