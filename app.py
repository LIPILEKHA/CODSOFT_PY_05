from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'  # SQLite database file
db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    address = db.Column(db.String(200))


@app.route('/')
def index():
    contacts = Contact.query.all()
    return render_template('index.html', contacts=contacts)

@app.route('/add_contact', methods=['GET','POST'])
def add_contact():
    success_message = None
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']

        new_contact = Contact(name=name, phone=phone, email=email, address=address)
        db.session.add(new_contact)
        db.session.commit()
    contacts = Contact.query.all()
    return render_template('index.html', success_message=success_message, contacts=contacts)


@app.route('/view_contacts', methods=['GET'])
def view_contacts():
    contacts = Contact.query.all()
    return render_template('view_contacts.html', contacts=contacts)

@app.route('/search_contact', methods=['POST'])
def search_contact():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        contacts = []

        if name:
            contacts = Contact.query.filter_by(name=name).all()
        elif phone:
            contacts = Contact.query.filter_by(phone=phone).all()

        return render_template('view_contacts.html', contacts=contacts)

    return redirect(url_for('view_contacts'))

@app.route('/update_contact', methods=['POST'])
def update_contact():
    if request.method == 'POST':
        contact_id = request.form['contact_id']
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']

        contact = Contact.query.get(contact_id)
        if contact:
            contact.name = name
            contact.phone = phone
            contact.email = email
            contact.address = address

            db.session.commit()

    return redirect(url_for('view_contacts'))

@app.route('/delete_contact', methods=['POST'])
def delete_contact():
    if request.method == 'POST':
        contact_id = request.form['contact_id']
        contact = Contact.query.get(contact_id)

        if contact:
            db.session.delete(contact)
            db.session.commit()

    return redirect(url_for('view_contacts'))

def init_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
