from flask import *
import sqlite3
import os
from werkzeug.utils import secure_filename
import datetime


UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
DATABASE = 'app.db'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    db = get_db()
    pictures = db.execute("SELECT id, path, title, description, category, create_date FROM pictures ORDER BY create_date DESC")
    show_pictures = pictures.fetchall()
    all_category = db.execute("SELECT category FROM pictures")
    all_cat = all_category.fetchall()
    cat_list = []
    for cat in all_cat:
        if cat not in cat_list:
            cat_list.append(cat)
    return render_template("layout.html", all_pictures=show_pictures, cat_list=cat_list)


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route('/vue_picture/uploads/<name>')
def downoload_vue(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/vue_picture/<id>')
def titre(id):
    db = get_db()
    picture = db.execute("SELECT id, path, title, description FROM pictures WHERE id=?", [id])
    commentaire = db.execute("SELECT comment FROM comments WHERE image_id=?", [id])
    return render_template("vue.html", picture=picture, message=commentaire)


@app.route('/vue_picture/<id>', methods=["POST"])
def comment(id):
    if request.method == 'POST':
        comment = request.form["comment"]
        db = get_db()
        db.execute("INSERT INTO comments (comment, image_id) VALUES (?, ?)", [comment, id])
        picture = db.execute("SELECT id, path, title, description FROM pictures WHERE id=?", [id])
        commentaire = db.execute("SELECT comment FROM comments WHERE image_id=?", [id])
        db.commit()
    return render_template("vue.html", picture=picture, message=commentaire)


@app.route('/category')
def category():
    recup_category = request.args.get("category")
    db = get_db()
    pic_from_cat = db.execute("SELECT path FROM pictures WHERE category=?", [recup_category])
    return render_template("category.html", pic_from_cat=pic_from_cat, recup_category=recup_category)


@app.route("/upload", methods=["POST"])
def create():
    if "file" not in request.files:
        return redirect("/")
    file = request.files["file"]
    title = request.form["title"]
    description = request.form["description"]
    category = request.form["category"]
    datetime_object = datetime.datetime.now()
    if file.filename != "" and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        db = get_db()
        db.execute("INSERT INTO pictures (path, title, description, category, create_date) VALUES (?, ?, ?, ?, ?)", [filename, title, description, category, datetime_object])
        db.commit()
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
