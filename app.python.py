from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from sqlalchemy import select
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee.sqlite3'
app.config['SECRET_KEY'] = "random string"
engine = sqlalchemy.create_engine('mysql://root:root@localhost:3306/employee',echo=True)
db = SQLAlchemy(app)

class employeedetails(db.Model):
    name = db.Column(db.String(100), primary_key=True)
    designation = db.Column(db.String(50))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(10))


def __init__(self, name, designation, address, phone):
    self.name = name
    self.designation = designation
    self.address = address
    self.phone = phone


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/list_employee')
def show_all():
    Session = sqlalchemy.orm.sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    myresult = session.query(employeedetails);
    return render_template('list.html', myresult=myresult)

@app.route('/new_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == "POST":
        details = request.form
        name = details['name']
        designation = details['designation']
        address = details['address']
        phone = details['phone']
        Session = sqlalchemy.orm.sessionmaker()
        Session.configure(bind=engine)
        session = Session()
        new_employee = employeedetails(name=name,designation=designation,address=address,phone=phone)
        session.add(new_employee)
        session.commit()
        return 'success'
    return render_template('add.html')

@app.route('/search_employee', methods=['GET', 'POST'])
def search_employee():
    if request.method == "POST":
        details = request.form
        option = details['optionselected']
        if(option == "name"):
            Session = sqlalchemy.orm.sessionmaker()
            Session.configure(bind=engine)
            session = Session()
            search_employee = session.query(employeedetails).filter(employeedetails.name == details['name'])
            session.commit()
            return render_template('search2.html', search_employee=search_employee)
        elif(option == "designation"):
            name = details['name']
            Session = sqlalchemy.orm.sessionmaker()
            Session.configure(bind=engine)
            session = Session()
            search_employee = session.query(employeedetails).filter(employeedetails.designation == details['designation'])
            session.commit()
            return render_template('search2.html', search_employee=search_employee)
        elif (option == "phone"):
            name = details['name']
            Session = sqlalchemy.orm.sessionmaker()
            Session.configure(bind=engine)
            session = Session()
            search_employee = session.query(employeedetails).filter(
                employeedetails.phone == details['phone'])
            session.commit()
            return render_template('search2.html', search_employee=search_employee)
    return render_template('search1.html')

@app.route('/delete_employee', methods=['GET', 'POST'])
def delete_employee():
    if request.method == "POST":
        details = request.form
        name = details['name']
        Session = sqlalchemy.orm.sessionmaker()
        Session.configure(bind=engine)
        session = Session()
        session.query(employeedetails).filter(employeedetails.name == name).delete()
        session.commit()
        return "deleted"
    return render_template('delete1.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)