from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    # here is a list that should be got from the db # (for auto complete)
    movies_names = ["Harry Potter", "Batman: The Dark Knight", "The Hunger Games", "Transformers"]
    return render_template('homepage.html',movieNames=movies_names)

@app.route('/search')
def search_return_html():
    query = request.args.get('query')
    # with connector get to your mysql server and query the DB
    return render_template('moviePage.html',query=query)




if __name__ == '__main__':
    #app.run(host="delta-tomcat-vm",port="40998", debug=True)
    app.run(debug=True)