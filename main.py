from flask import Flask
from flask.json import jsonify
import requests, json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api_key = "b3a61baf9130dd3b4bae6925120f5d9a"
@app.route('/')
def index():
    page=open('myHw6.html',encoding='utf-8')
    res=page.read()
    return res


@app.route('/happy')
def hello_world():
    return 'Hello, World!'

@app.route('/search/movie/<query>', methods = ['GET'])
def searchmovie(query):
    apikey = "b3a61baf9130dd3b4bae6925120f5d9a"
    api = "https://api.themoviedb.org/3/search/movie?api_key="+api_key+"&query="+query+"&language=en-US&page=1&include_adult=false"
    print(query)
    d = requests.get(api).json()
    d = d['results']
    movies = []
    for i in range(len(d)):
        movie = {
            'id':  d[i]['id'],
            'title': d[i]['title'],
            'overview': d[i]['overview'],
            'poster_path': d[i]['poster_path'],
            'release_date': d[i]['release_date'],
            'vote_average': d[i]['vote_average'],
            'vote_count': d[i]['vote_count'],
            'genre_ids': d[i]['genre_ids'],
        }
        movies.append(movie)
    
    
    return jsonify({'results':movies}) 

@app.route('/search/tv/<query>', methods = ['GET'])
def searchtv(query):
    apikey = "b3a61baf9130dd3b4bae6925120f5d9a"
    api = "https://api.themoviedb.org/3/search/tv?api_key="+api_key+"&query="+query+"&language=en-US&page=1&include_adult=false"
    print(query)
    d = requests.get(api).json()
    d = d['results']
    tvs = []
    for i in range(len(d)):
        tv = {
            'id':  d[i]['id'],
            'title': d[i]['name'],
            'overview': d[i]['overview'],
            'poster_path': d[i]['poster_path'],
            'release_date': d[i]['first_air_date'],
            'vote_average': d[i]['vote_average'],
            'vote_count': d[i]['vote_count'],
            'genre_ids': d[i]['genre_ids'],
        }
        tvs.append(tv)
    
    
    return jsonify({'results':tvs}) 


@app.route('/search/multi/<query>', methods = ['GET'])
def searchmulti(query):
    apikey = "b3a61baf9130dd3b4bae6925120f5d9a"
    api = "https://api.themoviedb.org/3/search/multi?api_key="+api_key+"&query="+query+"&language=en-US&page=1&include_adult=false"
    print(query)
    d = requests.get(api).json()
    d = d['results']
    multis = []
    for i in range(len(d)):
        multi = {
            'id':  d[i]['id'],
            'overview': d[i]['overview'],
            'poster_path': d[i]['poster_path'],
            'vote_average': d[i]['vote_average'],
            'vote_count': d[i]['vote_count'],
            'genre_ids': d[i]['genre_ids'],
            'media_type': d[i]['media_type'],
        }
        if d[i].__contains__('first_air_date'):
            multi['release_date'] =  d[i]['first_air_date']
        else:
            multi['release_date'] =  d[i]['release_date']
        if d[i].__contains__('name'):
            multi['title'] =  d[i]['name']
        else:
            multi['title'] =  d[i]['title']
                
        multis.append(multi)

    
    return jsonify({'results':multis}) 


@app.route('/trending', methods = ['GET'])
def trending():
    api = "https://api.themoviedb.org/3/trending/movie/week?api_key=b3a61baf9130dd3b4bae6925120f5d9a"
    d = requests.get(api).json()
    d = d['results']
    movies = []
    for i in range(0,6):
        movie = {
            'title': d[i]['title'],
            'backdrop_path': d[i]['backdrop_path'],
            'release_date' : d[i]['release_date'],
        }
        movies.append(movie)
    return jsonify({"results":movies})

@app.route('/airing', methods = ['GET'])
def airing():
    api = "https://api.themoviedb.org/3/tv/airing_today?api_key=b3a61baf9130dd3b4bae6925120f5d9a"
    d = requests.get(api).json()
    d = d['results']
    tvs = []
    for i in range(0,6):
        tv = {
            'name': d[i]['name'],
            'backdrop_path': d[i]['backdrop_path'],
            'first_air_date' : d[i]['first_air_date'],
        }
        tvs.append(tv)
    return jsonify({"results":tvs})

@app.route('/detail/movie/<id>',methods =['GET'])
def moviedetail(id):
    api = "https://api.themoviedb.org/3/movie/"+id+"?api_key=b3a61baf9130dd3b4bae6925120f5d9a&language=en-US"
    d = requests.get(api).json()
    details = []
    detail = {
        'id' : d['belongs_to_collection']['id'],
        'name': d['belongs_to_collection']['name'],
        'runtime' : d['runtime'],
        'release_date' : d['release_date'],
        'spoken_languages' : d['spoken_languages'][0]['name'],
        'vote_average': d['vote_average'],
        'poster_path' : d['belongs_to_collection']['poster_path'],
        'backdrop_path' : d['belongs_to_collection']['backdrop_path'],
        'genres' : d['genres'],
        'vote_count' : d['vote_count'],
        'overview' :d['overview'],
    }
    return jsonify({"results":detail})

@app.route('/cast/movie/<id>', methods = ['GET'])
def moviecast(id):
    api = "https://api.themoviedb.org/3/movie/"+id+"/credits?api_key=b3a61baf9130dd3b4bae6925120f5d9a&language=en-US"
    d = requests.get(api).json()
    d = d['cast']
    casts = []
    num = min(8,len(d))
    for i in range(0,num):
        cast = {
            'name': d[i]['name'],
            'profile_path': d[i]['profile_path'],
            'character' : d[i]['character'],
        }
        casts.append(cast)
    return jsonify({"results" : casts})

@app.route('/review/movie/<id>', methods = ['GET'])
def moviereview(id):
    api = "https://api.themoviedb.org/3/movie/"+id+"/reviews?api_key=b3a61baf9130dd3b4bae6925120f5d9a&language=en-US"
    d = requests.get(api).json()
    d = d['results']
    reviews = []
    num = min(5,len(d))
    for i in range(0,num):
        review = {
            'username': d[i]['author_details']['username'],
            'content' : d[i]['content'],
            'rating' : d[i]['author_details']['rating'],
            'created_at' : d[i]['created_at'],
        }
        reviews.append(review)
    return jsonify({"results":reviews})




@app.route('/detail/tv/<id>',methods =['GET'])
def tvdetail(id):
    api = "https://api.themoviedb.org/3/tv/"+id+"?api_key=b3a61baf9130dd3b4bae6925120f5d9a&language=en-US"
    d = requests.get(api).json()
    details = []
    detail = {
        'backdrop_path' : d['backdrop_path'],
        'episode_run_time' : d['episode_run_time'],
        'release_date' : d['first_air_date'],
        'genres' : d['genres'],
        'id' : d['id'],
        'name': d['name'],
        'number_of_seasons': d['number_of_seasons'],
        'overview': d['overview'],
        'poster_path' : d['poster_path'],
        'spoken_languages' : d['spoken_languages'][0]['name'],
        'vote_average': d['vote_average'],        
        'vote_count' : d['vote_count'],
    }
    return jsonify({"results":detail})

@app.route('/cast/tv/<id>', methods = ['GET'])
def tvcast(id):
    api = "https://api.themoviedb.org/3/tv/"+id+"/credits?api_key=b3a61baf9130dd3b4bae6925120f5d9a&language=en-US"
    d = requests.get(api).json()
    d = d['cast']
    casts = []
    num = min(8,len(d))
    for i in range(0,num):
        cast = {
            'name': d[i]['name'],
            'profile_path': d[i]['profile_path'],
            'character' : d[i]['character'],
        }
        casts.append(cast)
    return jsonify({"results" : casts})

@app.route('/review/tv/<id>', methods = ['GET'])
def tvreview(id):
    api = "https://api.themoviedb.org/3/tv/"+id+"/reviews?api_key=b3a61baf9130dd3b4bae6925120f5d9a&language=en-US"
    d = requests.get(api).json()
    d = d['results']
    reviews = []
    num = min(5,len(d))
    for i in range(0,num):
        review = {
            'username': d[i]['author_details']['username'],
            'content' : d[i]['content'],
            'rating' : d[i]['author_details']['rating'],
            'created_at' : d[i]['created_at'],
        }
        reviews.append(review)
    return jsonify({"results":reviews})


