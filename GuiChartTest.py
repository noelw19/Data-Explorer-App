import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import PySimpleGUI as sg
import matplotlib
import datetime as dt
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import os.path as Path
from DES_View import View as DES
# from NewWindow import open_window as O_Window

message=''
def receive():
    """Handles receiving of messages."""
    while True:
        try:
            global msg_list
            msg_list = ''
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            print(msg, ' Hi')
            msg_list += (msg + '\n')


            window['msg'].update(msg_list, append=True)
        except OSError:  # Possibly client has left the chat.
            break


def send(event=None):  # event is passed by binders.
    """Handles sending of messages."""
    msg = message
    client_socket.send(bytes(msg, "utf8"))
    if msg == "{end}":
        client_socket.close()
        window.close()


def on_closing(event=None):
    """This function is to be called when the window is closed."""
    global message 
    message = "{end}"
    send()

sg.theme('Dark Blue 3')  # please make your windows colorful
# login credentials for testing purposes
user = 'Noel'
password = '1234'
# scene Variable to indicate where the program is in its lifecycle
current = 'login'

def des(screen=0):

    login = DES().login(sg)
    screen1 = DES().layout('DES Screen 1', sg)
    screen2 = DES().layout('DES Screen 2', sg)
    screen3 = DES().layout('DES Screen 3', sg)

    if screen == 1:
        return screen1
    if screen == 2:
        return screen2
    if screen == 3:
        return screen3
    return login

# Define the initial window layout
layout = des()

def SetGraphCoordinates(fig, xVals, yVals):
    valsX = np.array(xVals)
    valsY = np.array(yVals)
    fig.add_subplot(1, 1, 1).plot(valsX, valsY)

def initSocket(w, num):
    # will need to change port numbers here in the future before the connection is made 
    client_socket.connect(ADDR)
    receive_thread = Thread(target=receive)
    receive_thread.start()
    print('Rendering: Screen ' + str(num))
    w['msg'].update(msg_list)

matplotlib.use("TkAgg")

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg


def des_render(prevWindow, num, csv= None):
    prevWindow.close()
    # VARIABLE equals a new layout that corresponds to function num value
    layout_instance = des(num)

    def event_checker(w):
    # if event == '#1' for button click and loginEvent for if user logs out and logs back in
    # since the des1 button is not pushed on login
        if event == '#1' or event == 'loginEvent':
            initSocket(w, 1)
        elif event == '#2':
            initSocket(w, 2)
        elif event == '#3':
            initSocket(w, 3)

    # new global window obj 
    global window
    # window equals a new PySimpleGUI.Window(screen name, layout, other methods)
    window = sg.Window('Data exploration Screen #' + str(num), layout_instance, size=(700, 500), finalize=True)
    # added draw figure for the graph to render properly
    newFig = matplotlib.figure.Figure(figsize=(3, 2), dpi=100)
    if csv == None:
        if num == 1:
            SetGraphCoordinates(newFig, [3, 2, 1, 0], [9, 5, 8, 1])
        if num == 2:
            SetGraphCoordinates(newFig, [1, 3, 2, 4], [7, 3, 6, 7])
        if num == 3:
            SetGraphCoordinates(newFig, [1, 4, 6, 8], [9, 7, 3, 2])
    else:
        dates = []
        # iterating through the date strings and converting them to date objects
        for j in csv[0][1:]:
            dates.append(dt.datetime.strptime(j, '%Y-%m-%d'))
        SetGraphCoordinates(newFig, dates, csv[1][1:])
        print(csv[0][1], csv[0][len(csv)])
        # ax = matplotlib.axes.Axes.plot_date(x=csv[0], y=None , xDate=True)
    draw_figure(window["-CANVAS-"].TKCanvas, newFig)
    event_checker(window)


# first window instance
window = sg.Window('Login', layout, size=(700, 500))

# when page change port will be changed to reflect different rooms per screen so
# users can talk to other people within the same room.
HOST = '127.0.0.1'
PORT = 33000

BUFSIZ = 1024
ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)


def structureCsvData(data):
    rows = []
    list1 = [list(row) for row in f.values]
    newRows = []
    count = 0
        # newRows.append(datum)
    
    # print(rows)
    for d in data.columns:
        newRows.append(d)
        for dataList in list1:
            newRows.append(dataList[count])
        count += 1
        rows.append(newRows)
        newRows = []
    # print(rows)
    return rows
# closes current socket instance and instantiates a new one then returns it
def resetSocket(client):
    client.close()
    client_socket = socket(AF_INET, SOCK_STREAM)        
    return client_socket
    

while True:
    # Event Loop
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        on_closing()
        break
    # IF send message button is pressed
    if event == 'Send':
        message = values['choice']
        send()
        print(message)
    # LOGIN PAGE 
    if current == 'login' or event == 'loginEvent':
        # if the username and password entered match local data
        if values['-USER-'] == user and values['-PASSWORD-'] == password:
            # print logged in and change current scene to des1
            print('User logged in')
            current = des_render(window, 1)
            message = user
            send()
    
    if event == 'logout':
        # if it is a logout event we close the current window by passing it as an arg
        window.close()
        # have to create new socket instance incase user logs in without restarting prog
        client_socket = resetSocket(client_socket)
        # login_screen becomes a layout list by calling the des func which returns a login list layout if no args or 0 is input
        login_screen = des()
        # open new window, with new layout
        window = sg.Window('Logged Out', login_screen, size=(700, 500))
        print('User is logged out.')
        # return 'login'

    if event == '#1':
        # closing socket then creating new instance of client socket for new
        # communications, error is received wwhen new instance is not created,
        # because closed comms cannot be reopened with socket.
        client_socket = resetSocket(client_socket)
        des_render(window, 1)
        message = user
        send()
    if event == '#2':
        client_socket = resetSocket(client_socket)
        des_render(window, 2)
        message = user
        send()
    if event == '#3':
        client_socket = resetSocket(client_socket)
        des_render(window, 3)
        message = user
        send()
    # Conditional for when upload button i pressed
    if event == 'uploadBtn':
        filename = values['upload']
        print(filename)
        if Path.isfile(filename):
            try:
                value = []
                val = pd.read_csv(filename, delimiter=',')
                listData = structureCsvData(val)
                XandY = [listData[0], listData[1]]
                print(XandY)
                # dateObj = datetime.strptime(vChild[0], "%Y-%m-%d")
                # values.append(dateObj)
                uploadWindow  = des_render(window,1 , XandY)
            except Exception as e:
                print("Error: ", e)
window.close()
