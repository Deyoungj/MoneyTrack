import PySimpleGUI as sg
import sqlite3
import datetime
import numpy as np
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')



conn = sqlite3.connect('data/Expenses.db')
cursor = conn.cursor()


try:
    cursor.execute("""CREATE TABLE EXPENSES(      
        Date text,
        Description text,
        Category text,      
        Income Real,
        Expense Real,
        Balance Real   
        )""")
except:
    pass



def Delete_data():
    with conn:
        cursor.execute("DELETE  FROM  EXPENSES")



def income(date, description, category, income, balance=0):
    with conn:
        cursor.execute("INSERT INTO EXPENSES(Date, Description, Category, Income, Balance) VALUES (?, ?, ?,?,?)",( date, description, category, income, balance))
        conn.commit()



def expenses(date, description, category, expense, balance=0):
    with conn:
        cursor.execute("INSERT INTO EXPENSES(Date, Description, Category, Expense, Balance) VALUES (?, ?, ?,?,?)",( date, description, category, expense,balance))
        
        conn.commit()


# this replaces the income null value with an empty string
def income_replace_null():
    with conn:
        cursor.execute("UPDATE EXPENSES SET Income='' WHERE Income IS NULL")
        conn.commit()


# this replaces the expense null value with an empty string
def expense_replace_null():
    with conn:
        cursor.execute("UPDATE EXPENSES SET Expense='' WHERE Expense IS NULL")
        conn.commit()





# this updates the balance
def balance_update():
    with conn:
        cursor.execute("UPDATE EXPENSES as a  SET Balance = (SELECT SUM(Income)-SUM(Expense)FROM EXPENSES as b WHERE a.rowid >= b.rowid ORDER BY rowid)") 
        conn.commit()


def graph_data(): 
    df = pd.read_sql_query("SELECT * FROM EXPENSES", conn)

    data = df.groupby('Category').mean()
    return data





def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=True)
    return figure_canvas_agg




def Expense_data_win():
    sg.theme('LightBlue')

    # current date
    date = datetime.date.today()



    # canvas_size 
    wide = 900 # x
    tall = 500 # y


    # expense layout
    tab1_layout = [
        
        [sg.Text('Description  '),
         sg.Input(key='-DES-',
         background_color='white',
         text_color='Black',
         do_not_clear=False)
         ],

        [sg.Text('Amount      '),
         sg.Input(key='-AMT-',
         background_color='white',
         text_color='Black',
         do_not_clear=False)
         ],

        [sg.Text('                '),
        sg.Button('Save',
        key='-SAVE-'),
        ],

        [sg.Frame('Category',
        [
            [sg.Radio('Income','expense',key='-IN-')],
            [sg.Radio('Books','expense',key='-BOOKS-')],
            [sg.Radio('Tutoring fee','expense',key='-TUT-')],
            [sg.Radio('Tuition','expense',key='-SCH-')],
            [sg.Radio('Lodging','expense',key='-LODGE-')],
            [sg.Radio('Transport','expense',key='-TRANS-')],
            [sg.Radio('Outfit','expense',key='-OUTFIT-')],
            [sg.Radio('Entertainment','expense',key='-ENT-')],
            [sg.Radio('Other','expense',key='-OTH-')]

        ],title_color='blue')
        ]
       

    ]
    
    # categories
    category = {
        'income':'Income:',
        'book':'Books:',
        'tutor':'Tutoring fee:',
        'school':'Tuition fee:',
        'transport':'Transport:',
        'outfit':'shopping:',
        'entertainment':'Entertainment:',
        'lodge':'Lodging:',
        'other':'Others:'
    }

    # this fetches the header from the database
    cursor.execute('SELECT * FROM EXPENSES')
    header = [i[0] for i in cursor.description]

   
    # this fetches the data from the expenses table
    cursor.execute('SELECT * FROM EXPENSES')
    data = cursor.fetchall()
    

    # expense list layout
    tab2_layout = [
            [sg.Table(values=data,
            headings=header,
            col_widths=(19,50),
            auto_size_columns=False,
            display_row_numbers=False,
            justification='left',
            key = '-TABLE-',
            row_height=25,
            tooltip= 'this is a table',
            num_rows=(21),
            size=(150,20),
            alternating_row_color='lightgreen',
            pad=(0,0),
            header_background_color='darkgreen',
            text_color='Black', 
            background_color='white',
            )],
            [sg.Button('REFRESH'), sg.Button('Restart Table')]
    ]

    

    # graph plot
    fig = matplotlib.figure.Figure(figsize=(10, 5), dpi=100)
   
    


    # expense graph
    tab3_layout = [
        [sg.T('Your Expense Graph')],
        [sg.Canvas(size=(wide,tall), key='-CANVAS-',)],
        [sg.Button('Show')],
         

    ]


    # All layout together
    layout = [
        [sg.Text('                     '),
        sg.Text('EXPENSES TRACKER V1.0', 
        size=(30, 1), justification='center',
        font=("Helvetica", 25,),

        text_color='Blue')

    ],

        [sg.TabGroup([[sg.Tab('New Expenses', tab1_layout,), 
        sg.Tab('Expenses', tab2_layout), 
        sg.Tab('Expense Graph',tab3_layout)]])
        ],

        [sg.T('Date:',text_color='blue'), sg.T(date,text_color='Blue'),
        sg.T('                                                 '),
        sg.T('By: Chidi',text_color='Blue',justification='right')]
         
    ]
        
        
    expense_window = sg.Window('Expense Tracker',layout, disable_minimize=False, resizable=False, icon='images/wallet.ico',finalize=True)



    while True:
        event, values = expense_window.read()
        

        if event == sg.WIN_CLOSED:
            break
         
        
        if values['-IN-']:
            
            """ if true it takes in the input of the user and stores
            it to the database and then updates the table with 
            with the new values"""

            income(date,values['-DES-'],category['income'],values['-AMT-'])
            expense_replace_null() 
            balance_update()        
        
            cursor.execute("SELECT * FROM EXPENSES")
            update = cursor.fetchall()
            expense_window['-TABLE-'].update(update)

        
        
        if values['-TUT-']:
            
                
            """ if true it takes in the input of the user 
            and subtracts it from the balance and stores
            it to the database depending on the category  and then updates the table with 
            with the new values """

            expenses(date,values['-DES-'],category['tutor'],values['-AMT-'])
            balance_update()
            income_replace_null()
            cursor.execute("SELECT * FROM EXPENSES")
            update = cursor.fetchall()
            expense_window['-TABLE-'].update(update)



        if values['-BOOKS-']:
            """ if true it takes in the input of the user 
            and subtracts it from the balance and stores
            it to the database depending on the category  and then updates the table with 
            with the new values """

            expenses(date,values['-DES-'],category['book'],values['-AMT-'])
            balance_update()
            income_replace_null()
            cursor.execute("SELECT * FROM EXPENSES")
            update = cursor.fetchall()
            expense_window['-TABLE-'].update(update)



        if values['-TRANS-']:
            """ if true it takes in the input of the user 
            and subtracts it from the balance and stores
            it to the database depending on the category  and then updates the table with 
            with the new values """

            expenses(date,values['-DES-'],category['transport'],values['-AMT-'])
            balance_update()
            income_replace_null()
            cursor.execute("SELECT * FROM EXPENSES")
            update = cursor.fetchall()
            expense_window['-TABLE-'].update(update)


            

        if values['-SCH-']:
            """ if true it takes in the input of the user 
            and subtracts it from the balance and stores
            it to the database depending on the category  and then updates the table with 
            with the new values """

            expenses(date,values['-DES-'],category['school'],values['-AMT-'])
            balance_update()
            income_replace_null()
            cursor.execute("SELECT * FROM EXPENSES")
            update = cursor.fetchall()
            expense_window['-TABLE-'].update(update)



        if values['-OUTFIT-']:
            """ if true it takes in the input of the user 
            and subtracts it from the balance and stores
            it to the database depending on the category  and then updates the table with 
            with the new values """

            expenses(date,values['-DES-'],category['outfit'],values['-AMT-'])
            balance_update()
            income_replace_null()
            cursor.execute("SELECT * FROM EXPENSES")
            update = cursor.fetchall()
            expense_window['-TABLE-'].update(update)


        if values['-LODGE-']:
            """ if true it takes in the input of the user 
            and subtracts it from the balance and stores
            it to the database  and then updates the table with 
            with the new values """

            expenses(date,values['-DES-'],category['lodge'],values['-AMT-'])
            balance_update()
            income_replace_null()
            cursor.execute("SELECT * FROM EXPENSES")
            update = cursor.fetchall()
            expense_window['-TABLE-'].update(update)



        if values['-ENT-']:
            """ if true it takes in the input of the user 
            and subtracts it from the balance and stores
            it to the database depending on the category  and then updates the table with 
            with the new values """

            expenses(date,values['-DES-'],category['entertainment'],values['-AMT-'])
            balance_update()
            income_replace_null()
            cursor.execute("SELECT * FROM EXPENSES")
            update = cursor.fetchall()
            expense_window['-TABLE-'].update(update)




        if values['-OTH-']:
            """ if true it takes in the input of the user 
            and subtracts it from the balance and stores
            it to the database depending on the category and then updates
            the table with  with the new values """
           
            expenses(date,values['-DES-'],category['other'],values['-AMT-'])
            balance_update()
            income_replace_null()
            cursor.execute("SELECT * FROM EXPENSES")
            update = cursor.fetchall()
            expense_window['-TABLE-'].update(update)

        

        if event == 'REFRESH':
            # this updates the window
            balance_update()
            cursor.execute("SELECT * FROM EXPENSES")
            update = cursor.fetchall()
            expense_window['-TABLE-'].update(update)
            

        if event == 'Restart Table':
            """ this deletes all records from database
            and refreshes the window """
            Delete_data()
            update = cursor.fetchall()
            expense_window['-TABLE-'].update(update)


        if event == 'Show':
            fig.add_subplot().plot(graph_data())
            fig_canvas_agg = draw_figure(expense_window['-CANVAS-'].TKCanvas, fig)
            

        
                                
    conn.close()
    expense_window.close()


