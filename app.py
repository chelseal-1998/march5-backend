import sqlite3

from flask import Flask, render_template, request, jsonify

from flask_cors import CORS


app = Flask(__name__)
CORS(app)


def update_tables():
    try:

        conn = sqlite3.connect('database.db')
        print("Opened database successfully")
        conn.execute("UPDATE blogs SET video = 'https://youtube/embed/jN4dXenlxbI' WHERE id = 3")
        print("Table updated successfully")

        conn.close()
    except Exception as e:
        print(str(e))
    finally:
        pass


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def init_sqlite_db():
    conn = sqlite3.connect('database.db')
    print("Opened database successfully")
    conn.execute('CREATE TABLE IF NOT EXISTS blogs (id INTEGER PRIMARY KEY AUTOINCREMENT ,header TEXT, title TEXT, '
                 'description TEXT, body1 TEXT, body2 TEXT, body3 TEXT, body4 TEXT, body5 TEXT ,image TEXT,'
                 'category TEXT, video TEXT)')

    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT ,username TEXT,email TEXT, '
                 'surname TEXT, contact TEXT)')
    print("Table created successfully")

    # print(conn.execute("PRAGMA table_info('users')").fetchall())
    # conn.execute("ALTER TABLE users ADD COLUMN contact TEXT")
    print(conn.execute("SELECT * FROM users").fetchall())


    conn.close()






init_sqlite_db()
update_tables()



@app.route('/')
@app.route('/blog-form/')
def enter_data():
    return render_template('blog-form.html')


@app.route('/add-data/', methods=['POST'])
def add_new_record():
    if request.method == "POST":
        try:
            header = request.form['header']
            title = request.form['title']
            description = request.form['description']
            body1 = request.form['body1']
            body2 = request.form['body2']
            body3 = request.form['body3']
            body4 = request.form['body4']
            body5 = request.form['body5']
            image = request.form['image']
            category = request.form['category']
            video = request.form['video']
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT INTO blogs (header, title, description, body1, body2,body3,body4,body5, image, "
                            "category, video) VALUES (?, "
                            "?, ?, "
                            "?,?,?,?,?,?,?,?)",
                            (header, title, description, body1, body2, body3, body4, body5, image, category, video))
                con.commit()
                msg = "Record successfully added."
        except Exception as e:
            con.rollback()
            msg = "Error occurred in insert operation: " + e
        finally:
            con.close()
            return render_template('result.html', msg=msg)


@app.route('/edit-data/<int:data_id>', methods=['PUT'])
def update_record(data_id):
    if request.method == "PUT":
        try:
            header = request.form['header']
            title = request.form['title']
            description = request.form['description']
            body1 = request.form['body1']
            body2 = request.form['body2']
            body3 = request.form['body3']
            body4 = request.form['body4']
            body5 = request.form['body5']
            image = request.form['image']
            category = request.form['category']
            video = request.form['video']
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("UPDATE blogs (header, title, description, body1,body2,body3,body4,body5, image, "
                            "category, video) VALUES (?, "
                            "?, ?, "
                            "?,?,?,?,?,?,?,?) WHERE id=?",
                            (header, title, description, body1, body2, body3, body4, body5, image, category, video,
                             data_id))
                con.commit()
                msg = "Record successfully updated."
        except Exception as e:
            con.rollback()
            msg = "Error occurred in insert operation: " + e
        finally:
            con.close()
            return render_template('result.html', msg=msg)


@app.route('/show-data/', methods=['GET'])
def show_data():
    data = []
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM blogs")
            data = cur.fetchall()
    except Exception as e:
        con.rollback()
        print("There was an error fetching results from the database.")
    finally:
        con.close()

        # return render_template('records.html', data=data)
        return jsonify(data)


@app.route('/show-blog-item/<int:data_id>/', methods=['GET'])
def show_blog_item(data_id):
    data = []
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute("SELECT * FROM blogs WHERE id=" + str(data_id))
            data = cur.fetchone()
    except Exception as e:
        con.rollback()
        print("There was an error fetching results from the database: " + str(e))
    finally:
        con.close()
        return jsonify(data)


@app.route('/delete-data/<int:data_id>/', methods=["GET"])
def delete_data(data_id):
    msg = None
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("DELETE FROM blogs WHERE id=" + str(data_id))
            con.commit()
            msg = "A record was deleted successfully from the database."
    except Exception as e:
        con.rollback()
        msg = "Error occurred when deleting a student in the database: " + str(e)
    finally:
        con.close()
    return render_template('delete-success.html', msg=msg)


@app.route('/show-users/', methods=["GET"])
def show_users():
    try:
        with sqlite3.connect('database.db') as con:
            con.row_factory = dict_factory
            cur = con.cursor()
            cur.execute('SELECT * users')
            data = cur.fetchall()
            print("user added")

    except Exception as e:
        con.rollback()
        print("There was an error fetching users:" + str(e))

    finally:
        con.close()
    return jsonify(data)


@app.route('/add-user/', methods=["POST"])
def new_user():
    if request.method == "POST":
        msg = None
        try:
            data = request.get_json()
            username = data['username']
            surname = data['surname']
            email = data['email']
            contact = data['contact']

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("INSERT into users (username,email,surname,contact) VALUES (?,?,?,?)",
                            (username, email, surname, contact))
                con.commit()
                msg = username + "was succcessfully added to the database."
        except Exception as e:
            con.rollback()
            msg = "Error occurred:" + str(e)
        finally:
            con.close()
            return jsonify(msg=msg)


if __name__ == '__main__':
    app.run(debug=True)
