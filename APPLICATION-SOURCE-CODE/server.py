from flask import Flask, render_template, request

import random

import mysql.connector


app = Flask(__name__)

def connect_to_mysql_server():
    cnx = mysql.connector.connect(user='DbMysql07',
                                  password='BestSqlProject101',
                                  host='mysqlsrv1.cs.tau.ac.il',
                                  port=3306,
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
    cur = cnx.cursor()
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
    cur = cnx.cursor()
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
    cur = cnx.cursor()
    name = name.replace("'", "''")
    cur.execute("SELECT film_id FROM FILM WHERE title = '%s'" % name)

    rows = cur.fetchall()
    film_id = rows[0][0]

    close_connection(cnx)

    return get_details_by_id(film_id)

def get_awards(film_id):
    res = []

    cnx = connect_to_mysql_server()
    cur = cnx.cursor()
    cur.execute("SELECT award, count FROM FILM_AWARD WHERE film_id = '%s'" % film_id)
    rows = cur.fetchall()

    awards = ["Oscar", "Golden Globe", "BAFTA Film award"]
    for row in rows:
        res.append({'award':row[0], 'count':row[1]})

    close_connection(cnx)

    return res

def get_genres(film_id):
    res = []

    cnx = connect_to_mysql_server()
    cur = cnx.cursor()
    cur.execute("SELECT genre FROM FILM_GENRE WHERE film_id = '%s'" % film_id)
    rows = cur.fetchall()

    for row in rows:
        res.append(row[0])

    close_connection(cnx)

    return res

def get_locations(film_id):
    res = []

    cnx = connect_to_mysql_server()
    cur = cnx.cursor()
    cur.execute("SELECT location FROM FILM_LOCATION WHERE film_id = '%s'" % film_id)
    rows = cur.fetchall()

    for row in rows:
        res.append(row[0])

    close_connection(cnx)

    return res[:4]


def get_providers(film_id):
    res = []

    cnx = connect_to_mysql_server()
    cur = cnx.cursor()
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
    cur = cnx.cursor()
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
    
    # makes trailers works from outside requests like our website #
    res['trailer'] = res['trailer'].replace("watch?v=","embed/")

    return res


def more_like_this(f_id, delta_year, delta_rating):

    # returns a list with [{"id":"nifen", "poster":"link to poster"},]

    res = []

    cnx = connect_to_mysql_server()
    cur = cnx.cursor()

    query = (   "SELECT DISTINCT FILM.film_id, FILM.image "
                "FROM FILM, FILM_GENRE, "
                "(SELECT FILM.year AS f_year FROM FILM WHERE FILM.film_id = " + "'%s'" % f_id + " ) SUB_QUERY_1, "
                "(SELECT FILM.rating AS f_rating FROM FILM WHERE FILM.film_id = " + "'%s'" % f_id + " ) SUB_QUERY_2 "
                "WHERE FILM.film_id = FILM_GENRE.film_id "
                "AND FILM.film_id <> " + "'%s'" % f_id + " "
                "AND FILM_GENRE.genre in "
                    "(SELECT FILM_GENRE.genre FROM FILM_GENRE WHERE FILM_GENRE.film_id = " + "'%s'" % f_id + " ) "
                "AND ABS(FILM.year - f_year) < %s " % delta_year + " "
                "AND ABS(FILM.rating - f_rating) < %s " % delta_rating + " " )

    cur.execute(query)
    rows = cur.fetchall()

    for row in rows:
        row_map = {'id':row[0], 'poster':row[1]}
        res.append(row_map)

    close_connection(cnx)

    return res

def get_topcast(f_id):

    res = []

    cnx = connect_to_mysql_server()
    cur = cnx.cursor()

    query = (   "SELECT ACTOR.actor_id, ACTOR.actor_name, ACTOR.birthdate, ACTOR.image, r_avg FROM "
                "ACTOR, "
                    "(SELECT ACTOR.actor_id AS a_id, AVG(FILM.rating) as r_avg "
                    "FROM ACTOR, FILM_STAR, FILM "
                    "WHERE FILM.film_id = " + "'%s'" % f_id + " "
                    "AND FILM_STAR.film_id = " + "'%s'" % f_id + " "
                    "AND FILM_STAR.actor_id = ACTOR.actor_id "
                    "GROUP BY ACTOR.actor_id) SUB_QUERY "
                "WHERE ACTOR.actor_id = a_id;" )

    cur.execute(query)
    rows = cur.fetchall()

    for row in rows:

        row_map = {}
        keys = ['id', 'name', 'birthdate', 'image', 'avg']

        for i in range(0, len(keys)):
            row_map[keys[i]] = row[i]

        res.append(row_map)

    close_connection(cnx)

    return res[:5]

movies_names = get_movie_names() #global list for auto complete

@app.route('/')
@app.route('/index')
def index():
    movies_posters = get_movie_posters()
    return render_template('home.html', movies_names=movies_names, movies_posters=movies_posters)



@app.route('/search')
def search_return_html():
    context = {}

    f_id = request.args.get('id', default=None)
    if( f_id is not None):
        context = get_details_by_id(f_id)
    else:
        query = request.args.get('query', default = None)
        # sanitize input
        if(query not in movies_names):
            return render_template("not_found.html", query=query)

        context = get_details_by_name(query)

    recs = more_like_this(context['film_id'], 2, 1)
    topcast = get_topcast(context['film_id'])
    return render_template('movie.html',context=context, movies_names=movies_names, recs=recs, topcast=topcast)




if __name__ == '__main__':
    app.run(host="0.0.0.0",port="40444")