from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    tittle = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    data = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/', methods=['GET', 'POST'])
def main_page():
    articles = Article.query.order_by(Article.data.desc()).all()
    return render_template('main.html', articles=articles)


@app.route('/create-article', methods=['GET', 'POST'])
def create_article():
    if request.method == 'POST':
        tittle = request.form['tittle']
        author = request.form['author']
        text = request.form['text']
        article = Article(tittle=tittle, author=author, text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return 'При добавлении произошла ошибка'
    else:
        return render_template('create_article.html')


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.data.desc()).all()
    return render_template('posts.html', articles=articles)


@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template('post_detail.html', article=article)


@app.route('/posts/<int:id>/delete')
def post_delete(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return 'При удалении произошла ошибка'


@app.route('/posts/<int:id>/update', methods=['GET', 'POST'])
def post_update(id):
    if request.method == 'POST':
        tittle = request.form['tittle']
        author = request.form['author']
        text = request.form['text']
        article = Article(tittle=tittle, author=author, text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return 'При добавлении произошла ошибка'
    else:
        article = Article.query.get(id)
        return render_template('post_update.html', article=article)


if __name__ == '__main__':
    app.run(debug=True)
