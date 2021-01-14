from flask import Flask, render_template, request

import random
import bleach

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


def get_born_today():
    # this func should return a list of strings, with info about the Database
    res = [
           "Number of alllll awards in the DB"
           "# ", #(this will Join awards with genre)#
           "Number of award in each genre",
           ###### randomize genre #####
    
    ]

    ####these string will be displayed in the homepage under the website name as a text slideshow

    return res


def get_ranks(f_id):
    # rank in the db
    # rank in each genre it has
    # [{'action':rank }, {'drama': rank}]

    res = {}

    cnx = connect_to_mysql_server()
    cur = cnx.cursor()

    query = (   "SELECT FILM_GENRE.genre, COUNT(*) "
                "FROM FILM, FILM_GENRE "
                "WHERE FILM.film_id = FILM_GENRE.film_id "
                "AND FILM.rating > "
                "(SELECT FILM.rating FROM FILM WHERE FILM.film_id = '%s')" % f_id + " "
                "GROUP BY FILM_GENRE.genre;"
            )


    cur.execute(query)
    rows = cur.fetchall()

    for row in rows:
        res[row[0]] = row[1]


    close_connection(cnx)
    if len(res) > 5 :
        res = dict(list(res.items())[:5])
    return res


def get_director_cast(director):
    director = director.replace("'", "''")
    res = []

    cnx = connect_to_mysql_server()
    cur = cnx.cursor()

    query = (   "SELECT ACTOR.actor_name, COUNT(*) AS times "
                "FROM ACTOR, FILM_STAR, FILM "
                "WHERE ACTOR.actor_id = FILM_STAR.actor_id "
                "AND FILM_STAR.film_id = FILM.film_id "
                "AND FILM.director = '%s'" % director + " "
                "GROUP BY ACTOR.actor_name "
                "ORDER BY times DESC"
            )

    cur.execute(query)
    rows = cur.fetchall()

    for row in rows:
        res.append(row[0])

    close_connection(cnx)
    if len(res) > 10 :
        res = res[:11]
    return res

def get_actor_spec(actor_id):

    res = []

    cnx = connect_to_mysql_server()
    cur = cnx.cursor()

    query = (   "SELECT FILM_GENRE.genre, COUNT(*) popularity "
                "FROM FILM_GENRE, FILM, FILM_STAR "
                "WHERE FILM_GENRE.film_id = FILM.film_id "
                "AND FILM.film_id = FILM_STAR.film_id "
                "AND FILM_STAR.actor_id = '%s'" % actor_id + " "
                "GROUP BY FILM_GENRE.genre "
                "ORDER BY popularity DESC;"
            )


    cur.execute(query)
    rows = cur.fetchall()



    for row in rows:
        res.append(row[0])

    close_connection(cnx)


    return res


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
        film_map = {'title': row[0], 'poster': row[1].replace("_V1_", "_SL500_")}
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

    res['rating'] = str(res['rating'])[:3]

    ##KHIMEL COMPRESSION
    res['image'] = res['image'].replace("_V1_", "_SL300_")

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
        row_map = {'id':row[0], 'poster':row[1].replace("_V1_", "_SL200_")}
        res.append(row_map)

    close_connection(cnx)

    return res

def order_list(actors_list, ordered_actors):

    ordered_list = []

    for actor in ordered_actors:
        for d in actors_list:
            if d['id'] == actor:
                ordered_list.append(d)
                break

    return ordered_list

def get_topcast(f_id):

    res = []

    cnx = connect_to_mysql_server()
    cur = cnx.cursor()

    query_1 = ("SELECT ACTOR.actor_id, ACTOR.actor_name, ACTOR.birthdate, ACTOR.image, AVG(FILM.rating) "
             "FROM ACTOR, FILM_STAR, FILM "                    
             "WHERE ACTOR.actor_id IN "
             "(SELECT actor_id "
             "FROM FILM_STAR "
             "WHERE FILM_STAR.film_id = " + "'%s'" % f_id +") "
             "AND FILM_STAR.film_id = FILM.film_id "
             "AND FILM_STAR.actor_id = ACTOR.actor_id "
             "GROUP BY ACTOR.actor_id;"
             )

    cur.execute(query_1)
    rows_1 = cur.fetchall()

    query_2 =   ("SELECT actor_id "
                "FROM FILM_STAR "
                "WHERE FILM_STAR.film_id = " + "'%s'" % f_id +";")

    cur.execute(query_2)
    rows_2 = cur.fetchall()

    ordered_actors = [rows_2[i][0] for i in range(0, len(rows_2))]

    for row in rows_1:

        row_map = {}
        keys = ['id', 'name', 'birthdate', 'image', 'avg']

        for i in range(0, len(keys)):
            if keys[i] == 'image':
                if row[i] is not None:
                    row_map[keys[i]] = row[i].replace("_V1_", "_SL300_")
                else:
                    row_map[keys[i]] = " "
            else:
                row_map[keys[i]] = row[i]

        res.append(row_map)

    close_connection(cnx)

    res = order_list(res, ordered_actors)

    # adding here his specialziation
    for i in range(0, len(res)):
        res.append({'spec':get_actor_spec(res[i]['id'])})

    if len(res) >= 10:
        res = res[:10]
    return res



movies_names = get_movie_names() #global list for auto complete

@app.route('/')
@app.route('/index')
def index():
    born_today = get_born_today()

    movies_posters = get_movie_posters()
    return render_template('home.html', movies_names=movies_names, movies_posters=movies_posters, born_today=born_today)



@app.route('/search')
def search_return_html():
    context = {}

    f_id = request.args.get('id', default=None)
    text = request.args.get('text', default=None)
    if( f_id is not None):
        context = get_details_by_id(f_id)
    elif(text is not None):
        text = bleach.clean(text)
        context = get_details_by_name("Inception")
    else:
        query = request.args.get('query', default = None)
        if(query not in movies_names):
            return render_template("not_found.html", query=query)

        context = get_details_by_name(query)

    recs = more_like_this(context['film_id'], 2, 1)
    topcast = get_topcast(context['film_id'])

    context['ranks'] = get_ranks(context['film_id']) ## put here the ranks

    d_cast = get_director_cast(context['director'])


    return render_template('movie.html',context=context, movies_names=movies_names, recs=recs, topcast=topcast, d_cast=d_cast)




if __name__ == '__main__':
    app.run(host="0.0.0.0",port="40444")