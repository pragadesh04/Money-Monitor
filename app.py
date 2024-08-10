from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)  # Changed to Float for numeric values
    date = db.Column(db.String(100), nullable=False)

def delete_all():
    try:
        # Delete all records from the Data table
        num_deleted = db.session.query(Data).delete()
        db.session.commit()
        return f"Successfully deleted {num_deleted} records."
    except Exception as e:
        db.session.rollback()
        return f"An error occurred: {e}"
    
@app.route("/", methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        name = request.form.get('name')
        amount = request.form.get('amount')

        # Check if data is valid
        if not name or not amount:
            return "Name and Amount are required", 400

        try:
            amount = float(amount)
        except ValueError:
            return "Invalid amount. Must be a number.", 400

        name = name.upper()

        print(name, amount)
        olddate = datetime.now().date()
        olddate = str(olddate).split("-")
        date = olddate[2] + "-" + olddate[1] + "-" + olddate[0]
        new_data = Data(name=name, amount=amount, date=date)
        db.session.add(new_data)
        db.session.commit()

        return redirect(url_for('details'))

    return render_template("index.html")

@app.route("/see-details")
def details():
    records = Data.query.all()
    totalAmnt = sum(data.amount for data in records)
    print(totalAmnt)
    return render_template("see-details.html", records=records, totalAmnt=totalAmnt)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
