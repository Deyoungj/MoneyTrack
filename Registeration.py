
import PySimpleGUI as sg
import sqlite3
import main



user_conn = sqlite3.connect('user_detail/user')
user_c = user_conn.cursor()

try:
    user_c.execute("""CREATE TABLE USERS (
        firstname text,
        lastname text,
        email text,
        username text,
        password text

    ) """) 
except:
    pass



def Add_users(firstname,lastname,email,username,password):
    with user_conn:
        user_c.execute("INSERT INTO USERS VALUES(?,?,?,?,?)",(firstname,lastname,email,username,password,))
        


def Registration_window():


    Registration_window_layout = [
       
        [sg.T('Registration',size=(25, 1), justification='center', font=("Helvetica", 20,),relief=sg.RELIEF_RIDGE,)],
        [sg.Text('               ')],
        [sg.Text('First Name',pad=(3,0)), sg.Input(key='-FIRST_NAME-')],
        [sg.Text('Last Name ',pad=(3,0)), sg.Input(key='-LAST_NAME-')],
        [sg.Text('Email         ', pad=(3,0)), sg.Input(key='-EMAIL-')],
        [sg.Text('User Name ',pad=(3,0)), sg.Input(key='-USER_NAME-')],
        [sg.Text('Password   ',pad=(3,0)), sg.Input(key='-PASSWORD-')],
        [sg.Text('               '),sg.Button('create account'), sg.Button('cancel'),
        sg.Text('                                                   ',key='-NOTIFY-')],
        
    ]

    registration_window = sg.Window('Expense Tracker', Registration_window_layout, margins=(150,200),disable_minimize=False, resizable=False, auto_size_buttons=True,auto_size_text=True,icon='images/wallet.ico')
    

    while True:
        event, values = registration_window.read()

        if event == 'cancel' or event == sg.WIN_CLOSED:    
            break

        if event == 'create account':
            #this takes the users data and adds it to the database
            Add_users(values['-FIRST_NAME-'], values['-LAST_NAME-'],values['-EMAIL-'],values['-USER_NAME-'],values['-PASSWORD-'])
            registration_window['-NOTIFY-'].update('Your profile has been created.')
            registration_window.close()
            main.Expense_data_win()
            break

       

    registration_window.close()


