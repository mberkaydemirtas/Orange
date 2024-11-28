import PySimpleGUI as sg
import sqlite3

def get_user_role(username, password):
    con = sqlite3.connect('Project.db')
    cur = con.cursor()
    
    # Check if the user is an admin
    cur.execute("SELECT * FROM Admin WHERE adusername = ?", (username,))
    if cur.fetchone():
        cur.execute("SELECT * FROM User WHERE username = ? AND password = ?", (username, password))
        user = cur.fetchone()
        if user:
            con.close()
            return 'admin', user[1]  # Assuming user[1] is the name of the user
    # Check if the user is a tour guide
    cur.execute("SELECT * FROM TourGuide WHERE tgusername = ?", (username,))
    if cur.fetchone():
        cur.execute("SELECT * FROM User WHERE username = ? AND password = ?", (username, password))
        user = cur.fetchone()
        if user:
            con.close()
            return 'tourguide', user[1]
    
    # Check if the user is a traveler
    cur.execute("SELECT * FROM Traveler WHERE trusername = ?", (username,))
    if cur.fetchone():
        cur.execute("SELECT * FROM User WHERE username = ? AND password = ?", (username, password))
        user = cur.fetchone()
        if user:
            con.close()
            return 'traveler', user[1]
    
    con.close()
    return None, None



#ADMIN PAGES


def show_create_tour_form():
    layout = [
        [sg.Text('Create a New Tour', font=('Helvetica', 16), background_color='navyblue', text_color='white')],
        [sg.Text('Tour Name', background_color='navyblue', text_color='white'), sg.InputText(key='tname')],
        [sg.Text('Starting Date', background_color='navyblue', text_color='white'), sg.InputText(key='stdate')],
        [sg.Text('Ending Date', background_color='navyblue', text_color='white'), sg.InputText(key='endate')],
        [sg.Text('Price', background_color='navyblue', text_color='white'), sg.InputText(key='price')],
        [sg.Text('Itinerary', background_color='navyblue', text_color='white'), sg.InputText(key='itinerary')],
        [sg.Text('Maximum Capacity', background_color='navyblue', text_color='white'), sg.InputText(key='maxcap')],
        [sg.Button('Create Tour', button_color=('white', 'navyblue'))],
        [sg.Button('Back', button_color=('white', 'navyblue'))]
    ]
    
    window = sg.Window('Create Tour', layout, background_color='navyblue')
    
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED :
            break
        if  event == 'Back':
            window.close()
            show_admin_page(username)
            break
        if event == 'Create Tour':
            tname = values['tname']
            stdate = values['stdate']
            endate = values['endate']
            price = values['price']
            itinerary = values['itinerary']
            maxcap = values['maxcap']


            try:
                print("Starting Create Tour logic", flush=True)
                tname = values['tname']
                stdate = values['stdate']
                endate = values['endate']
                price = values['price']
                itinerary = values['itinerary']
                maxcap = values['maxcap']

                print(f"Inserting: {tname}, {stdate}, {endate}, {price}, {itinerary}, {maxcap}", flush=True)
                con = sqlite3.connect('Project.db')
                cur = con.cursor()
                cur.execute("SELECT MAX(tid) FROM Tour")
                result = cur.fetchone()
                next_tid = (result[0] or 0) + 1
                print(f"Next tid determined: {next_tid}", flush=True)
                cur.execute("INSERT INTO Tour (tid, tname, stdate, endate, price, itinerary, maxcap) VALUES (?, ?, ?, ?, ?, ?, ?)",
                            (next_tid, tname, stdate, endate, price, itinerary, maxcap))
                con.commit()
                print("Insert committed successfully", flush=True)
                sg.popup('Tour created successfully', font=('Helvetica', 14))

            except Exception as e:
                print(f"Error occurred: {e}", flush=True)
            finally:
                con.close()
                print("Database connection closed", flush=True)
            window.close()
            show_add_transportation()
            break

    
    window.close()
    


#Transportation

def show_add_transportation():
    transportation_options=[
    ("Bus", "Istanbul", "Rome"),
    ("Plane", "Moscow", "Paris"),
    ("Train", "Berlin", "Prague"),
    ("Boat", "Athens", "Santorini"),
    ("Plane", "New York", "Boston"),
    ("Plane", "Tokyo", "Seoul"),
    ("Train", "London", "Edinburgh"),
    ("Bus", "Madrid", "Barcelona"),
    ("Boat", "Naples", "Palermo"),
    ("Boat", "Los Angeles", "San Francisco"),
    ("Plane", "Dubai", "Cairo"),
    ("Train", "Zurich", "Geneva"),
    ("Bus", "Helsinki", "Stockholm"),
    ("Boat", "Tallinn", "Helsinki"),
    ("Plane", "Bangkok", "Singapore"),
    ("Train", "Munich", "Vienna"),
    ("Train", "Brussels", "Amsterdam"),
    ("Plane", "Sydney", "Melbourne"),
    ("Bus", "Warsaw", "Krakow"),
    ("Boat", "Oslo", "Copenhagen")
] 
    
    layout = [
        [sg.Text("Choose Transportation of Tour", font=('Helvetica', 16))],
        [sg.Text("Filter by type", font=('Helvetica', 16))],
        [sg.Combo(["All", "Plane", "Train", "Boat", "Bus"], key="t_filter", enable_events=True)],
        [sg.Text("Filter by starting point", font=('Helvetica', 16))],
        [sg.Combo(["All", "Istanbul", "Moscow", "Berlin", "Athens", "New York", "Tokyo", "London", "Madrid", "Naples", "Los Angeles", "Dubai", "Zurich", "Helsinki", "Tallinn", "Bangkok", "Munich", "Brussels", "Sydney", "Warsaw", "Oslo"], key= "s_filter", enable_events=True)],
        [sg.Text("Filter by destination", font=('Helvetica', 16))],
        [sg.Combo(["All",'Rome', 'Paris', 'Prague', 'Santorini', 'Boston', 'Seoul', 'Edinburgh', 'Barcelona', 'Palermo', 'San Francisco', 'Cairo', 'Geneva', 'Stockholm', 'Helsinki', 'Singapore', 'Vienna', 'Amsterdam', 'Melbourne', 'Krakow', 'Copenhagen'], key= "d_filter", enable_events=True)],
        [sg.Listbox(transportation_options, key="transportation_options", size=(30, len(transportation_options)), select_mode='single', enable_events=True)],
        [sg.Button("Done", font=('Helvetica', 16))],
        [sg.Button("Close", font=('Helvetica', 16))]]
    
    window = sg.Window('Transportation_Page', layout)
    

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == "Close":
            break
        if event == "Done":
            t_transportation = values['transportation_options']
            try:
                print("Starting choose tour options", flush=True)
                t_transportation = values['transportation_options']


                print(f"Inserting: {t_type}, {t_start}, {t_destination}",  flush=True)
                con = sqlite3.connect('Project.db')
                cur = con.cursor()
                cur.execute("SELECT MAX(tid) FROM Tour")
                result = cur.fetchone()
                t_code = result[0]
                t_type= t_transportation[0]
                t_start = t_transportation[1]
                t_destination = t_transportation[2]
                cur.execute("INSERT INTO Transportation (tcode, type, starting_point, destination) VALUES (?, ?, ?, ?)",
                                (t_code, t_type[0], t_start[0], t_destination[0]))
                con.commit()
                print("Insert committed successfully", flush=True)
                sg.popup('Transportation created successfully', font=('Helvetica', 14))
            except Exception as e:
                print(f"Error occurred: {e}", flush=True)
            finally:
                con.close()
                print("Database connection closed", flush=True)
            

    window.close()
    



def show_admin_page(username):
    con = sqlite3.connect('Project.db')
    cur = con.cursor()
    cur.execute("SELECT name FROM User WHERE username = ?", (username,))
    user = cur.fetchone()
    con.close()
    
    name = user[0]
    
    # Define the layout of the admin window
    layout = [
        [sg.Text(f'Welcome {name}', font=('Helvetica', 16), justification='center', background_color='navyblue', text_color='white')],
        [sg.Button('Create New Tour', button_color=('white', 'navyblue'))],
        [sg.Button('Exit', button_color=('white', 'navyblue'))]
    ]
    
    # Create the admin window
    window = sg.Window('Admin Page', layout, background_color='navyblue')
    
    # Event loop to process events and get values of inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'Create New Tour':
            window.close()
            show_create_tour_form()
            break

    window.close()




#TOURGUIDE PAGES  



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




#TRAVELER PAGES



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




#LOGIN PAGES


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
            role, name = get_user_role(username, password)
            if role == 'admin':
                window.close()
                show_admin_page(username)
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

