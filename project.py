from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import jinja2

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Mysql1234'
app.config['MYSQL_DB'] = 'rentride'

mysql = MySQL(app)


@app.route('/login-link')
def login_link():

    return render_template("login_link.html")


@app.route('/signup-borrower',methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        pswd = request.form.get('password')
        contact = request.form.get('contact')
        cur = mysql.connection.cursor()
        cur.execute("insert into borrower values('%s','%s','%s','%s')" % (username, email, contact, pswd))
        mysql.connection.commit()

        return render_template("borrower_login.html")
    return render_template('borrower_signup.html')


@app.route('/login-borrower',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        password = request.form.get('password')
        cur = mysql.connection.cursor()
        cur.execute("select * from borrower where name = '%s';"%(user))
        data = cur.fetchone()

        if data == None:
            return render_template('borrower_login.html')


        elif password == data[-1]:
            print("valid successfully")
            return render_template("main.html")

        else:
            return render_template('borrower_login.html')


    return render_template('borrower_login.html')


@app.route('/home')
def home():
    return render_template('Main.html')


@app.route('/cycles')
def user():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM list_of_cycles WHERE availability = 'yes'")
    user = cur.fetchall()
    return render_template('cycle_list.html', user = user)

@app.route('/rent/<owner>')
def rent(owner):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM list_of_cycles WHERE owner = '%s'"%(owner))
    lender = cur.fetchall()

    return render_template('cycle_rent.html', lender = lender)


if __name__=="__main__":
    app.run(debug=True)