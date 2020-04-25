import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor

app = Flask(__name__)

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)

@app.route('/add-donation/', methods=['GET', 'POST'])
def add_donation():

    # Give the option to add a new donation
    if request.method == 'POST':
        try:
            donor = Donor.select().where(Donor.name == request.form['donor']).get()
        except Donor.DoesNotExist:
            return render_template('add-donation.jinja2', error="Donor does not exist")

        value = int(request.form['donation-amount'])
        new_donation = Donation(value=value, donor=donor)
        new_donation.save()

        return redirect(url_for('all'))

    return render_template('add-donation.jinja2')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

