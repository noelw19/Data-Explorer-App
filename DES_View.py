#  This is the des screen class that is used to seperate concerns and improve readability.
# did not use the def __init__ because it returns none whereas i needed the class to return the list containing the 
# layout for pysimple gui, and with only 1 call that returns my needed data i didnt see an issue with my current setup...
#  -------Famous Last Words------------
class View:
    # passed the name of the screen as well at the pysimplegui object as arguements, so my current code did not pass errors
    # regarding sg is undefined.
    def layout(self, name, sg):
        self.current = name[:-1]
        self.name = name
        self.layout = [
            [sg.Button("DES 1", key='#1', mouseover_colors=('yellow', 'green')),
            sg.Button("DES 2", key='#2', mouseover_colors=('yellow', 'green')),
            sg.Button("DES 3", key='#3', mouseover_colors=('yellow', 'green')),
            sg.Text('', size=(50, 1)),
            sg.Button('Logout', key='logout')],
            [sg.Text(self.name, expand_x=True, justification='center')],
            [sg.Canvas(key="-CANVAS-", expand_x=True)],
            [sg.Input(key='upload'), sg.FileBrowse(file_types=(("TXT Files", "*.csv"), ("ALL Files", "*.*"))), sg.Button("Upload", key='uploadBtn')],
            [sg.Text('Chat Below', size=(20, 2), expand_x=True, justification='center')],
            [sg.Multiline('Mssages are shown here!', key='msg', size=(50, 3), expand_x=True, justification='left', no_scrollbar=False, autoscroll=True, disabled=True)],
            [sg.Input(key='choice', do_not_clear=False, expand_x=True)],
            [sg.Button("Ok", key='Send', expand_x=True)],
        ]
        return self.layout
# login method that returns the login screen when called.
    def login(self, sg):
        self.login = [
            [sg.Text('Please enter your login credentials', justification='center', size=(100, 1))],
            # input values are there but later will add login finctionality.
            [sg.Text('Username', justification='center', size=(35, 1)), sg.InputText('Noel', key='-USER-')],
            [sg.Text('Password', justification='center', size=(35, 1)), sg.InputText('1234', key='-PASSWORD-')],
            [sg.Button('Submit', key='loginEvent', expand_x=True), sg.Cancel()]
        ]
        return self.login

    
