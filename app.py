from flask import Flask, request, jsonify
from ml_model import recommend_movies

app = Flask(__name__)

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    movie_id = data.get('movie_id')
    user_id = data.get('user_id')

    if movie_id is None or user_id is None:
        return jsonify({"error": "Movie ID or User ID is missing."}), 400

    recommended_movies = recommend_movies(int(movie_id))

    return jsonify({"user_id": user_id, "movie_id": movie_id, "recommended_movies": recommended_movies})

if __name__ == '__main__':
    app.run(debug=True)
