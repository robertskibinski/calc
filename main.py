import csv
import requests
from flask import Flask, render_template, request
import array

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()

rates = data[0]['rates']

with open('rates.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')

    writer.writerow(['currency', 'code', 'bid', 'ask'])

    for rate in rates:
        writer.writerow([rate['currency'], rate['code'], rate['bid'], rate['ask']])


########
# cz.2 #
########

app = Flask(__name__)


@app.route("/", methods=["GET","POST"])
def home():
    bid = []
    for rate in rates:
        bid.append(rate["code"])

    if request.method == "POST":
        currency = request.form.get("currency")
        if request.form.get("amount") == "":
            return render_template("index.html", bid = bid)
        else:
            amount = float(request.form.get("amount"))
            for rate in rates:
                if currency == rate["code"]:
                    result = round(amount * float(rate["bid"]), 2)
            return render_template("index.html", result = result, bid = bid)


    return render_template("index.html", bid = bid)


app.run()
