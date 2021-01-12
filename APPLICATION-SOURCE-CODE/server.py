from flask import Flask, render_template, request

import random
import MySQLdb
import MySQLdb.cursors
import mysql.connector

app = Flask(__name__)

# movies = [
#         {"name":"Jurassic Park", "poster":"https://i.pinimg.com/originals/e4/ca/5a/e4ca5a0c6a7b2dac40358e3f217174e0.jpg"},
#         {"name":"The Godfather", "poster":"https://thelogocompany.net/wp-content/uploads/2017/05/The-Godfather-poster.jpg"},
#         {"name":"Jaws", "poster":"https://www.companyfolders.com/blog/media/2017/07/jaws.jpg"},
#         {"name":"Star Wars: The Last Jedi", "poster":"https://www.digitalartsonline.co.uk/cmsdata/slideshow/3662115/star-wars-last-jedi-poster.jpg"},
#         {"name":"The Shawshank Redemption", "poster":"https://cdn.shopify.com/s/files/1/0057/3728/3618/products/9f22e23817c4accbf052e0f91a2b7821_156f8e4f-814c-4dcb-896d-0b077053cd51_480x.progressive.jpg?v=1573593734"},
#         {"name":"Bad Boys For Life", "poster":"https://cdn11.bigcommerce.com/s-yshlhd/images/stencil/1280x1280/products/22036/167222/full.badboysforlife_28858__15292.1589660739.jpg?c=2?imbypass=on"},
#         {"name":"Black Panther", "poster":"https://www.washingtonpost.com/graphics/2019/entertainment/oscar-nominees-movie-poster-design/img/black-panther-web.jpg"},
#         {"name":"Joker", "poster":"https://cdn11.bigcommerce.com/s-ydriczk/images/stencil/1280x1280/products/89058/93685/Joker-2019-Final-Style-steps-Poster-buy-original-movie-posters-at-starstills__62518.1572351179.jpg?c=2?imbypass=on"},
#         {"name":"Narnia", "poster":"https://www.arthipo.com/image/cache/catalog/poster/movie/1-758/pfilm289-fronty-wardrobe-narnia-narniya-poster-cizgi-film-1000x1000.jpg"}
# ]





def connect_to_mysql_server():
    cnx = mysql.connector.connect(user='DbMysql07',
                                  password='BestSqlProject101',
                                  host='127.0.0.1',
                                  port=3305,
                                  database='DbMysql07')
    if not cnx.is_connected():
        print("Couldn't connect!")
        exit(-1)
    else:
        return cnx


def close_connection(cnx):
    cnx.close()


#global list with movie names for auto complete
def get_movie_names():
    res = []

    cnx = connect_to_mysql_server()
    cur = cnx.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT DISTINCT title FROM FILM")

    rows = cur.fetchall()

    for row in rows:
        res.append((row[0]))

    close_connection(cnx)

    return res

def get_movie_posters():
    # returns a list with [{"id":"nifen", "poster":"link to poster"},]
    # size of list is 30

###### khimel - changed it to title with poster not id #####
    res = []

    cnx = connect_to_mysql_server()
    cur = cnx.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT title, image FROM FILM")

    rows = cur.fetchall()

    for row in rows:
        film_map = {'title': row[0], 'poster': row[1]}
        res.append(film_map)

    close_connection(cnx)
    random.shuffle(res)

    return res[0:30]

# details =  {"film_id":"", "title":"", "year":"", "image":"", "summary":"","trailer":"", "raiting":"", "director":"", "awards":{"":int, "":int}, "genre":[], "locations":[], "providers":[size of max 3], ("topcast":[{"id":"", "name":"", "img":"", "avg_movie_rating":""}])}
def get_details_by_name(name):
    cnx = connect_to_mysql_server()
    cur = cnx.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT film_id FROM FILM WHERE title = '%s'" % name)

    rows = cur.fetchall()
    film_id = rows[0][0]

    close_connection(cnx)

    return get_details_by_id(film_id)

def get_awards(film_id):
    res = {}

    cnx = connect_to_mysql_server()
    cur = cnx.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT award, count FROM FILM_AWARD WHERE film_id = '%s'" % film_id)
    rows = cur.fetchall()

    for row in rows:
        res[row[0]] = row[1]

    close_connection(cnx)

    return res

def get_genres(film_id):
    res = []

    cnx = connect_to_mysql_server()
    cur = cnx.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT genre FROM FILM_GENRE WHERE film_id = '%s'" % film_id)
    rows = cur.fetchall()

    for row in rows:
        res.append(row[0])

    close_connection(cnx)

    return res

def get_locations(film_id):
    res = []

    cnx = connect_to_mysql_server()
    cur = cnx.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT location FROM FILM_LOCATION WHERE film_id = '%s'" % film_id)
    rows = cur.fetchall()

    for row in rows:
        res.append(row[0])

    close_connection(cnx)

    return res


def get_providers(film_id):
    res = []

    cnx = connect_to_mysql_server()
    cur = cnx.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT provider FROM FILM_PROVIDER WHERE film_id = '%s'" % film_id)
    rows = cur.fetchall()

    for row in rows:
        res.append(row[0])

    close_connection(cnx)

    # khimel added here for now #
    if(len(res) >= 3):
        res = res[:3]

    return res

    
def get_details_by_id(film_id):

    res = {}

    cnx = connect_to_mysql_server()
    cur = cnx.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM FILM WHERE film_id = '%s'" % film_id)
    rows = cur.fetchall()

    details = rows[0]
    keys = ['film_id', 'title', 'year', 'image', 'summary', 'trailer', 'rating', 'director']

    for i in range(0, len(keys)):
        res[keys[i]] = details[i]

    close_connection(cnx)

    res['awards'] = get_awards(film_id)
    res['genres'] = get_genres(film_id)
    res['locations'] = get_locations(film_id)
    res['providers'] = get_providers(film_id)

    return res


def more_like_this(film_id):
    pass
    #returns a list with [{"id":"nifen", "poster":"link to poster"},]



movies_names = get_movie_names() #global list for auto complete

@app.route('/')
@app.route('/index')
def index():
    movies_posters = get_movie_posters()
    return render_template('home.html', movies_names=movies_names, movies_posters=movies_posters)



@app.route('/search')
def search_return_html():
    query = request.args.get('query')
    # sanitize input
    if(query not in movies_names):
        return render_template("not_found.html", query=query)

    context = get_details_by_name(query)
    movies_posters = get_movie_posters() ## this should be more like this 
    # context={
	# 	'Title': 'The Dark Knight',
	# 	'StoryLine': "Set within a year after the events of Batman Begins (2005), Batman, Lieutenant James Gordon, and new District Attorney Harvey Dent successfully begin to round up the criminals that plague Gotham City, until a mysterious and sadistic criminal mastermind known only as -The Joker- appears in Gotham, creating a new wave of chaos. Batman's struggle against The Joker becomes deeply personal, forcing him to confront everything he believes and improve his technology to stop him. A love triangle develops between Bruce Wayne, Dent, and Rachel Dawes. Written by Leon Lombardi",
	# 	'Synopsis': "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
	# 	'Premiere': '4 October 2019',
	# 	'Director': 'Christopher Nolan',
	# 	'FL': 'Chicago, Illinois, USA',
	# 	'Genres': 'Action | Crime | Drama | Thriller',
	# 	'Trailer': 'https://www.youtube.com/embed/EXeTwQWrcwY',
	# 	'Raiting':'9.5',
	# }
    topcast=[{'name':"Mhamad Khimel", "avg_rating":"10", "img":"https://media.self.com/photos/57d8a1044b76f0f832a0e34c/4:3/w_2560%2Cc_limit/leo-dicaprio-tux.jpg"},
             {'name':"Yazan Zoabi", "avg_rating":"5.5", "img":"https://upload.wikimedia.org/wikipedia/commons/6/6f/Dwayne_Johnson_Hercules_2014_%28cropped%29.jpg"},
             {'name':"Sumaya Saleh", "avg_rating":"9.9", "img":"https://www.biography.com/.image/t_share/MTE4MDAzNDEwNzQzMTY2NDc4/will-smith-9542165-1-402.jpg"},
             {'name':"Muhammad Watad", "avg_rating":"9.5", "img":"https://m.media-amazon.com/images/M/MV5BMjExNzA4MDYxN15BMl5BanBnXkFtZTcwOTI1MDAxOQ@@._V1_.jpg"}
    ]
    # if this movie is not from the auto complete, we redirect him for an "not found" html
        # return render_template('notFound.html', query=query)
    # with connector get to your mysql server and query the DB
    return render_template('movie.html',query=query,context=context, movies_names=movies_names, movies_posters=movies_posters, topcast=topcast)




if __name__ == '__main__':
    #app.run(host="delta-tomcat-vm",port="40998", debug=True)
    app.run(debug=True)