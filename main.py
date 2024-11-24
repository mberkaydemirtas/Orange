import PySimpleGUI as sg
import sqlite3

# Connect to the database
con = sqlite3.connect('Project.db')
cur = con.cursor()

# Query to get all admins
cur.execute("SELECT User.name FROM User, Admin WHERE Admin.adusername = User.username")
admins = cur.fetchall()

# Close the connection
con.close()

# Define the layout of the window
layout = [
    [sg.Text('Admin')],
    [sg.Listbox(values=admins, size=(50, 20))],
    [sg.Button('Exit')]
]

# Create the window
window = sg.Window('Admin List', layout, background_color='orange')

# Event loop to process events and get values of inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit':
        break

window.close()