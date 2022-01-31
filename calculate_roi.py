from turtle import color
from decimal import Decimal
from requests import Request, Session, Response

import PySimpleGUI as sg
import constans
import json

# Construccion de session get para obtener el precio actual del bombcrypto token

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

parameters = {
    'slug': 'bombcrypto',
    'convert': 'USD'
}

web_headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive'

}

session = Session()
session.headers.update(web_headers)

response = session.get(url, params=parameters)
bc_price = str('{:.2f}'.format(json.loads(response.text)['data']['12252']['quote']['USD']['price']))

# Construccion del Leyaut

sg.theme('DarkAmber')

heading = ['Inversión', 'BC x Día', 'Meta Días']
headers = [
    [sg.Text('')] + [sg.Text(h, size=(10, 1)) for h in heading]
]

col_rows = [
    [
        sg.Input(size=(11, 1), pad=(1, 5), justification='center', enable_events=True),
        sg.Input(size=(11, 1), pad=(1, 5), justification='center', enable_events=True),
        sg.Input(size=(11, 1), pad=(1, 5), justification='center', text_color='black', disabled=True, key="days_left")
    ] for row in range(1)]

heading = ['Tiempo', 'Rec. BC', 'Rec. USD']
headers2 = [
    [sg.Text('')] + [sg.Text(h, size=(10, 1)) for h in heading]
]

col_rows2 = [
    [
        sg.Text(constans.DAYS_7, size=(11, 1), pad=(1, 1)),
        sg.Input(size=(11, 1), pad=(1, 1), text_color='black', readonly=True, key='bc_gain3'),
        sg.Input(size=(11, 1), pad=(1, 1), text_color='black', disabled=True, key='bc_gain4')
    ],
    [
        sg.Text(constans.DAYS_15, size=(11, 1), pad=(1, 1)),
        sg.Input(size=(11, 1), pad=(1, 1), text_color='black', disabled=True, key='bc_gain5'),
        sg.Input(size=(11, 1), pad=(1, 1), text_color='black', disabled=True, key='bc_gain6')
    ],
    [
        sg.Text(constans.MONTH_1, size=(11, 1), pad=(1, 1)),
        sg.Input(size=(11, 1), pad=(1, 1), text_color='black', disabled=True, key='bc_gain7'),
        sg.Input(size=(11, 1), pad=(1, 1), text_color='black', disabled=True, key='bc_gain8')
    ],
    [
        sg.Text(constans.MONTHS_6, size=(11, 1), pad=(1, 1)),
        sg.Input(size=(11, 1), pad=(1, 1), text_color='black', disabled=True, key='bc_gain9'),
        sg.Input(size=(11, 1), pad=(1, 1), text_color='black', disabled=True, key='bc_gain10')
    ],
    [
        sg.Text(constans.YEAR_1, size=(11, 1), pad=(1, 1)),
        sg.Input(size=(11, 1), pad=(1, 1), text_color='black', disabled=True, key='bc_gain11'),
        sg.Input(size=(11, 1), pad=(1, 1), text_color='black', disabled=True, key='bc_gain12')
    ]
]



layout = [
    headers + col_rows,
    headers2 + col_rows2,
    [
        sg.Button(constans.CLOSE_BTN, size=(8, 0), pad=(1, 5)),
        sg.Button(constans.UPDATE_BTN, size=(15, 0), pad=(1, 5), tooltip='Actualiza precio de $BC.'),
        sg.Text('$BC: ' + bc_price, key='bc_price')
    ]
]
usd_value = Decimal(20.79)
days_list = [7, 7, 15, 15, 30, 30, 365/2, 365/2, 365, 365]

def update_price():
    response = session.get(url, params=parameters)
    bc_price = str('{:.2f}'.format(json.loads(response.text)['data']['12252']['quote']['USD']['price']))
    window['bc_price'].update("$BC: " + bc_price)

def calculate_roi(values):

    counter = 2

    price = Decimal(bc_price)

    invest = Decimal(0.0)
    bc_per_day = Decimal(0.0)

    if values[0] != '' and values[1] != '':
        invest = Decimal(values[0])
        bc_per_day = Decimal(values[1])

        values[2] = round(invest / bc_per_day, 0)

        for i in days_list:
            counter = counter + 1

            if counter % 2:
                values[counter] = round(Decimal((Decimal(i) * bc_per_day)) - invest, 1)
            else:
                values[counter] = round(Decimal(Decimal(i) * bc_per_day * price) - Decimal((invest * price)), 2)

            window['bc_gain' + str(counter)].update(values[counter])

        window['days_left'].update(values[2])


# Create the Window
window = sg.Window('Cálculo ROI Bombcrypto', layout, font='Courier 12')
# Event Loop to process "events" and get the "values" of the inputs
while True:

    event, values = window.read()

    # if user closes window or clicks cancel
    if event == sg.WIN_CLOSED or event == constans.CLOSE_BTN:
        session.close()
        break
    elif event == constans.UPDATE_BTN:
        update_price()

    calculate_roi(values)

window.close()
