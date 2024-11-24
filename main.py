import PySimpleGUI as sg
import sqlite3

def get_user_role(username, password):
    con = sqlite3.connect('Project.db')
    cur = con.cursor()
    
    # Check if the user is an admin
    cur.execute("SELECT * FROM Admin WHERE adusername = ?", (username,))
    if cur.fetchone():
        cur.execute("SELECT * FROM User WHERE username = ? AND password = ?", (username, password))
        if cur.fetchone():
            con.close()
            return 'admin'
    
    # Check if the user is a tour guide
    cur.execute("SELECT * FROM TourGuide WHERE tgusername = ?", (username,))
    if cur.fetchone():
        cur.execute("SELECT * FROM User WHERE username = ? AND password = ?", (username, password))
        if cur.fetchone():
            con.close()
            return 'tourguide'
    
    # Check if the user is a traveler
    cur.execute("SELECT * FROM Traveler WHERE trusername = ?", (username,))
    if cur.fetchone():
        cur.execute("SELECT * FROM User WHERE username = ? AND password = ?", (username, password))
        if cur.fetchone():
            con.close()
            return 'traveler'
    
    con.close()
    return None

def show_admin_page():
    con = sqlite3.connect('Project.db')
    cur = con.cursor()
    
    # Query to get all admins
    cur.execute("SELECT User.name FROM User WHERE User.username IN (SELECT adusername FROM Admin)")
    admins = cur.fetchall()
    
    # Close the connection
    con.close()
    
    # Define the layout of the admin window
    layout = [
        [sg.Text('Admin')],
        [sg.Listbox(values=admins, size=(50, 20))],
        [sg.Button('Exit')]
    ]
    
    # Create the admin window
    window = sg.Window('Admin List', layout, background_color='navyblue')
    
    # Event loop to process events and get values of inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
    
    window.close()

def show_tourguide_page():
    # Define the layout of the tour guide window
    layout = [
        [sg.Text('Tour Guide Page')],
        [sg.Button('Exit')]
    ]
    
    # Create the tour guide window
    window = sg.Window('Tour Guide Page', layout, background_color='navyblue')
    
    # Event loop to process events and get values of inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
    
    window.close()

def show_traveler_page():
    # Define the layout of the traveler window
    layout = [
        [sg.Text('Traveler Page')],
        [sg.Button('Exit')]
    ]
    
    # Create the traveler window
    window = sg.Window('Traveler Page', layout, background_color='navyblue')
    
    # Event loop to process events and get values of inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
    
    window.close()

# Define the layout of the login window
layout = [
    [sg.Text('Username'), sg.InputText(key='username')],
    [sg.Text('Password'), sg.InputText(key='password', password_char='*')],
    [sg.Button('Login')]
]

# Create the login window
window = sg.Window('Login', layout, background_color='navyblue')

# Event loop to process events and get values of inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
        break
    if event == 'Login':
        username = values['username']
        password = values['password']
        if not username:
            sg.popup('Username must be entered')
        elif not password:
            sg.popup('Password must be entered')
        else:
            role = get_user_role(username, password)
            if role == 'admin':
                window.close()
                show_admin_page()
                break
            elif role == 'tourguide':
                window.close()
                show_tourguide_page()
                break
            elif role == 'traveler':
                window.close()
                show_traveler_page()
                break
            else:
                sg.popup('Invalid username or password')

window.close()