from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():

    # here is a list that should be got from the db
    movies = [
        {"name":"Jurassic Park", "poster":"https://i.pinimg.com/originals/e4/ca/5a/e4ca5a0c6a7b2dac40358e3f217174e0.jpg"},
        {"name":"The Godfather", "poster":"https://thelogocompany.net/wp-content/uploads/2017/05/The-Godfather-poster.jpg"},
        {"name":"Jaws", "poster":"https://www.companyfolders.com/blog/media/2017/07/jaws.jpg"},
        {"name":"Star Wars: The Last Jedi", "poster":"https://www.digitalartsonline.co.uk/cmsdata/slideshow/3662115/star-wars-last-jedi-poster.jpg"},
        {"name":"The Shawshank Redemption", "poster":"https://cdn.shopify.com/s/files/1/0057/3728/3618/products/9f22e23817c4accbf052e0f91a2b7821_156f8e4f-814c-4dcb-896d-0b077053cd51_480x.progressive.jpg?v=1573593734"},
        {"name":"Bad Boys For Life", "poster":"https://cdn11.bigcommerce.com/s-yshlhd/images/stencil/1280x1280/products/22036/167222/full.badboysforlife_28858__15292.1589660739.jpg?c=2?imbypass=on"},
        {"name":"Black Panther", "poster":"https://www.washingtonpost.com/graphics/2019/entertainment/oscar-nominees-movie-poster-design/img/black-panther-web.jpg"},
        {"name":"Joker", "poster":"https://cdn11.bigcommerce.com/s-ydriczk/images/stencil/1280x1280/products/89058/93685/Joker-2019-Final-Style-steps-Poster-buy-original-movie-posters-at-starstills__62518.1572351179.jpg?c=2?imbypass=on"},
        {"name":"Narnia", "poster":"https://www.arthipo.com/image/cache/catalog/poster/movie/1-758/pfilm289-fronty-wardrobe-narnia-narniya-poster-cizgi-film-1000x1000.jpg"}
    ]
    movies_names = [movies[i]["name"] for i in range(len(movies))] # for auto complete
    movies_posters = [movies[i]["poster"] for i in range(len(movies))] # posters
    return render_template('homepage.html',movies=movies, movies_names=movies_names, movies_posters=movies_posters)

@app.route('/search')
def search_return_html():
    query = request.args.get('query')
    # if this movie is not from the auto complete, we redirect him for an "not found" html
        # return render_template('notFound.html', query=query)
    # with connector get to your mysql server and query the DB
    return render_template('moviePage.html',query=query)




if __name__ == '__main__':
    #app.run(host="delta-tomcat-vm",port="40998", debug=True)
    app.run(debug=True)