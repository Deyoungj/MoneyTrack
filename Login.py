import PySimpleGUI as sg
import Registeration as reg
from Registeration import user_conn, user_c
import main



def Login_window():
    
    sg.theme('dark')

    Validation_window_layout = [
                [sg.T('username')],
                [sg.In(key='-USERNAME-')],
                [sg.T('password')],
                [sg.In(key='-PASSWORD-',password_char='*')],
                [sg.Button('Sign Up'),sg.Button('Login'),
                sg.Text('dont have an account? please sign up', key='-TEXT-'),
                ]
    ]
    validation_window = sg.Window('Expense Tracker', Validation_window_layout, margins=(150, 200),disable_minimize=False, resizable=False,icon='images/wallet.ico')
    validation_window_active = False
    
   
    while True:
        event, values = validation_window.read()
        if event == sg.WIN_CLOSED or event == None:
            break


        if event == 'Sign Up':      # when true validation window closes
            validation_window.close() # and regsteraion window opens than breaks out of the loop
            reg.Registration_window()
            break


        if event =='Login':
            with user_conn:
                user_c.execute("SELECT * FROM USERS WHERE username = ? AND password = ?",(values['-USERNAME-'], values['-PASSWORD-'],))
                if user_c.fetchone(): # if it fetches any with the username and password                                             
                    validation_window.close() # it closes the login window and runs the main module
                    main.Expense_data_win()
                    break
                else:

                    validation_window['-TEXT-'].update('Wrong password',text_color='red')
            


    validation_window.close()

if __name__ == "__main__":
    Login_window()
