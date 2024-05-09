import json
import ast
import pandas as pd


def weighted_rating(x, m, c):

    v = x['vote_count']
    r = x['vote_average']
    return (v / (v + m) * r) + (m / (m + v) * c)


def get_recommendations(user_genres):
    try:
        print("Running get_recommendations")
        movies = pd.read_csv('new_dataset.csv')
        c = movies['vote_average'].mean()
        m = movies['vote_count'].quantile(0.95)

        qualified = movies[movies['vote_count'] >= m].copy()
        qualified.loc[:, 'vote_count'] = qualified['vote_count'].astype(int)
        qualified.loc[:, 'vote_average'] = qualified['vote_average'].astype(int)
        qualified['wr'] = qualified.apply(weighted_rating, axis=1, args=(m, c))
        qualified = qualified.sort_values('wr', ascending=False)

        movies['genre_names'] = movies['genres'].str.split(", ")
        s = movies['genre_names'].explode().reset_index()
        s.rename(columns={'genre_names': 'genre'}, inplace=True)

        gen_md = movies.join(s.set_index('index'), rsuffix='_exploded')

        recommended_movies = gen_md[gen_md['genre'].isin(user_genres)].head(10)
        print(recommended_movies)
        return recommended_movies.to_json(orient='records')
    except Exception as e:
        print('Error in get_recommendations:', str(e))
        return json.dumps([])


def handler(event, context):
    try:
        print("Running handler")
        data = json.loads(event['args'][0])
        user_genres = data.get('genres', [])
        recommendations = get_recommendations(user_genres)
        print("Recommendations:", recommendations)
    except Exception as e:
        print('Error in handler:', str(e))


get_recommendations(['Romance', 'Action'])