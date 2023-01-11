import csv
import requests
import tkinter as tk

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

rates_dict = {rate['code']: rate['currency'] for rate in rates}

window = tk.Tk()
window.title("Currency Calculator")

frame = tk.Frame(window)
frame.pack()

tk.Label(frame, text="Currency:").grid(row=0, column=0, sticky='W')
currency_var = tk.StringVar(frame)
currency_menu = tk.OptionMenu(frame, currency_var, *rates_dict.keys())
currency_menu.grid(row=0, column=1, sticky='W')

tk.Label(frame, text="Amount:").grid(row=1, column=0, sticky='W')
amount_var = tk.DoubleVar(frame)
amount_entry = tk.Entry(frame, textvariable=amount_var)
amount_entry.grid(row=1, column=1, sticky='W')

def calculate():
    code = currency_var.get()
    amount = amount_var.get()
    rate = next(rate['ask'] for rate in rates if rate['code'] == code)
    cost = rate * amount
    tk.Label(frame, text=f"Cost: {cost:.2f} PLN").grid(row=2, column=0, columnspan=2, sticky='W')

calculate_button = tk.Button(frame, text="Calculate", command=calculate)
calculate_button.grid(row=3, column=0, columnspan=2, sticky='W')

for i in range(4):
    tk.Grid.columnconfigure(frame, i, weight=1)
    tk.Grid.rowconfigure(frame, i, weight=1)

window.mainloop()