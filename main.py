#! python3
#! main.py -- Journal project simular to Notepad.

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from sys import exit
from tkinter import font


import pyperclip
import logging
import datetime

# Make it work properly, then make it look pretty...

class journal:
    def __init__(self):     # initiates the app and sets up Tk object
        
        # Initializes the debug logger

        logging.basicConfig(filename='test.log', level=logging.DEBUG)

        # Basic tkinter setup

        self.boldFont = 'normal'
        self.italicFont = 'roman'
        self.underlineFont = False

        self.root = Tk()
        self.fileName = 'untitled.txt'
        self.root.title(f'Journal-{self.fileName}')
        self.mainMenu = Menu()
        self.root.config(menu=self.mainMenu)
        self.toolbarFrame = ttk.Frame(self.root, relief=SUNKEN)
        self.toolbarFrame.grid(column=0, row=0)
        self.mainframe = ttk.Frame(self.root)
        self.mainframe.grid(column=0, row=1)

        # Main loop informaiton

        self.display()
        self.menu()
        self.hotkeys()

        self.root.mainloop()    # Keeps tkinter loop going
    
    def menu(self):     # File Menu -- Stores Cascades for file menu options
        
        # File Menu Cascade (New, Open, Close, Save, Save As)

        self.fileMenu = Menu(self.mainMenu)
        self.mainMenu.add_cascade(label='File', menu=self.fileMenu)
        self.fileMenu.add_command(label='New', command=self.newFile)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label='Open', command=self.openFile)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label='Save')
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label='Save As', command=self.saveAsFile)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label='Close', command=exit)

        # Edit Menu Cascade (undo, redo, cut, copy, paste)

        self.editMenu = Menu(self.mainMenu)
        self.mainMenu.add_cascade(label='Edit', menu=self.editMenu)
        self.editMenu.add_command(label='Undo Ctrl+z', command=self.textEntry.edit_undo)
        self.editMenu.add_separator()
        self.editMenu.add_command(label='Redo Ctrl+Shift+z', command=self.textEntry.edit_redo)
        self.editMenu.add_separator()
        self.editMenu.add_command(label='Cut Ctrl+x', command=self.cutText)
        self.editMenu.add_separator()
        self.editMenu.add_command(label='Copy Ctrl+c', command=self.copyText)
        self.editMenu.add_separator()
        self.editMenu.add_command(label='Paste Ctrl+v', command=self.pasteText)

        # View menu Cascade (Display, Settings)

        self.viewMenu = Menu(self.mainMenu)
        self.mainMenu.add_cascade(label='View', menu=self.viewMenu)
        self.viewMenu.add_command(label='Display')

        # Options menu (Settings)

        self.optionsMenu = Menu(self.mainMenu)
        self.mainMenu.add_cascade(label='Options', menu=self.optionsMenu)
        self.optionsMenu.add_command(label='Settings')

    def hotkeys(self):      # Hotkeys - Bound to specific tasks  TODO: Fix Bindings
        self.textEntry.bind('<Control-Shift-z>', self.textEntry.edit_undo)
        self.textEntry.bind('<Control-z>', self.textEntry.edit_redo)   

    def display(self):      # Display -- Loads the widgets for project
        # Text Entry Window

        self.textEntry = Text(self.mainframe, undo=True)
        self.textEntry.grid(column=0, row=1, columnspan=3, sticky='NSEW')
        self.textEntry.focus()

        # Scrollbar 

        self.textVerticleScroll = ttk.Scrollbar(self.mainframe, orient=VERTICAL, command=self.textEntry.yview)
        self.textHorizontalScroll = ttk.Scrollbar(self.mainframe, orient=HORIZONTAL, command=self.textEntry.xview)

        self.textEntry.configure(yscrollcommand=self.textVerticleScroll.set)
        self.textEntry.configure(xscrollcommand=self.textHorizontalScroll.set)

        self.textVerticleScroll.grid(column=40, row=1, sticky='NS')
        self.textHorizontalScroll.grid(column=0, row=1, sticky='SEW', columnspan=3)

        # Buttons

        self.italicsBtn = ttk.Button(self.toolbarFrame, text='I', command=lambda: self.underlineBoldItalic('italic'))
        self.boldBtn = ttk.Button(self.toolbarFrame, text='B', command=lambda: self.underlineBoldItalic('bold'))
        self.underlineBtn = ttk.Button(self.toolbarFrame, text='U', command=lambda: self.underlineBoldItalic('underline'))

        self.alignLeftBtn = ttk.Button(self.toolbarFrame, text='AL', command=self.alignTextLeft)
        self.alignRightBtn = ttk.Button(self.toolbarFrame, text='AR', command=self.alignTextRight)
        self.alignCenterBtn = ttk.Button(self.toolbarFrame, text='AC', command=self.alignTextCenter)

        self.italicsBtn.grid(column=0, row=0)
        self.boldBtn.grid(column=1, row=0)
        self.underlineBtn.grid(column=2, row=0)

        self.alignLeftBtn.grid(column=3, row=0)
        self.alignRightBtn.grid(column=4, row=0)
        self.alignCenterBtn.grid(column=5, row=0)

    # Menu Functions

    def copyText(self):     # Copy -- Tries to copy text to clipboard
        try:
            pyperclip.copy(self.textEntry.selection_get())
        except Exception as e:
            dateInfo = datetime.datetime.now()
            logging.debug(f'''
            - Copy Error:
            \tError Level: 'DEBUG'
            \tDate: {dateInfo.strftime('%m/%d/%Y  Time: %H:%M:%S')}
            \tReason: {e}
            \t"###No Text To Copy###"
            ''')

    def pasteText(self):    # Paste -- Tries to paste text clipboard
        try:
            self.textEntry.insert('insert', pyperclip.paste())
        except Exception as e:
            dateInfo = datetime.datetime.now()
            logging.debug(f'''
            - Paste Error:
            \tError Level: 'DEBUG'
            \tDate: {dateInfo.strftime('%m/%d/%Y  Time: %H:%M:%S')}
            \tReason: {e}
            \t"### No Text To Paste ###"
            ''')

    def cutText(self):      # Cut -- Cuts Selected text to clipboard
        if self.textEntry.selection_get:
            pyperclip.copy(self.textEntry.selection_get())
            self.textEntry.delete('sel.first', 'sel.last')

    def openFile(self):     # Open File -- Opens dialogue box for opening .txt files
        try:
            filename = filedialog.askopenfilename(
                initialdir='C:/Users/fathe/Desktop/Portfolio projects/tkinter/journal/journals', 
                title='Open'
                ) 

            with open(filename, 'r') as file:
                self.textEntry.delete(1.0, END)
                fileInfo = []       # TODO -- Need to reduce the amount of lines this takes/make it append the file name to a list of file names for open files
                for lines in file:
                    fileInfo.append(lines)
                fileList = filename.split('/')
                self.fileName = fileList[-1]
                self.root.title(f'Journal-{self.fileName}')
                fileInfo = ' '.join(fileInfo)
                self.textEntry.insert(1.0, fileInfo)
        except FileNotFoundError as e:
            dateInfo = datetime.datetime.now()
            logging.debug(f'''
            - Open File Error:
            \tError Level: 'DEBUG'
            \tDate: {dateInfo.strftime('%m/%d/%Y  Time: %H:%M:%S')}
            \tReason: {e}
            \t"### No File Opened ###"
            ''')

    def saveAsFile(self):     # Save As File -- Opens dialogue box for opening .txt files
        try:
            filename = filedialog.asksaveasfilename(
                initialdir='C:/Users/fathe/Desktop/Portfolio projects/tkinter/journal/journals', 
                title='Save As'
                )

            with open(filename, 'a') as file:
                file.writelines(self.textEntry.get(1.0, END))
        except FileNotFoundError as e:
            print(e)
                
    def newFile(self):
        try:
            self.fileName = 'untitled.txt'
            self.root.title(f'Journal-{self.fileName}')
            self.textEntry.delete(1.0, END)
        except FileNotFoundError as e:
            print(e)

    """ TODO -- Buttons now clears the selection before the next highlighted text is altered, 
                so it no longer edits both. However it now doesnt clear the selections that 
                were previously set up on the previously selected text. So if the first text 
                is bold and underlined, and you click the bold on a newly selected seciton it 
                will apply both font styles to it."""

    #   TODO -- Add more buttons ()

    # Toolbar Functions

    def underlineBoldItalic(self, option):      # Handles italics, bold, and underline options

        # need to make it turn on and off for ongoing text
        # need to make it recognize what secitons should be unchecked for bold. 
        # may have to make a font for each potential option. 
        
        fontToEdit = font.Font(self.textEntry, self.textEntry.cget('font'))
        fontToEdit.configure(underline=self.underlineFont, weight=self.boldFont, slant=self.italicFont)
        currentTags = self.textEntry.tag_names('sel.first')

        if option == 'bold':
            if 'bold' in currentTags:
                self.boldFont = 'normal'
                self.textEntry.tag_remove(f'bold', 'sel.first', 'sel.last') 
            else:
                self.boldFont = 'bold'
                fontToEdit = font.Font(self.textEntry, self.textEntry.cget('font'))
                fontToEdit.configure(underline=self.underlineFont, weight=self.boldFont, slant=self.italicFont)
                self.textEntry.tag_configure(f'bold', font=fontToEdit)
                self.textEntry.tag_add(f'bold', 'sel.first', 'sel.last')
                self.textEntry.selection_clear()

        elif option == 'italic':
            if self.italicFont == 'italic':
                self.italicFont = 'roman'
                self.textEntry.tag_remove(f'italic', 'sel.first', 'sel.last')
            else:
                self.italicFont = 'italic'
                fontToEdit = font.Font(self.textEntry, self.textEntry.cget('font'))
                fontToEdit.configure(underline=self.underlineFont, weight=self.boldFont, slant=self.italicFont)
                self.textEntry.tag_configure(f'italic', font=fontToEdit)
                self.textEntry.tag_add(f'italic', 'sel.first', 'sel.last')
                self.textEntry.selection_clear()

        elif option == 'underline':
            if self.underlineFont == 'underline':
                self.underlineFont = False
                self.textEntry.tag_remove(f'underline', 'sel.first', 'sel.last')
            else:
                self.underlineFont = True
                fontToEdit = font.Font(self.textEntry, self.textEntry.cget('font'))
                fontToEdit.configure(underline=self.underlineFont, weight=self.boldFont, slant=self.italicFont)
                self.textEntry.tag_configure(f'underline', font=fontToEdit)
                self.textEntry.tag_add(f'underline', 'sel.first', 'sel.last')
                self.textEntry.selection_clear()
        

        
      
    
    def alignTextLeft(self):        # Aligns text to the left
        self.textEntry.tag_configure('left', justify='left')
        currentTags = self.textEntry.tag_names(1.0)

        if 'left' in currentTags:
            self.textEntry.tag_remove('left', 1.0, 'end')
            self.textEntry.focus()
        else:
            try:
                self.textEntry.tag_remove('right', 1.0, 'end')
                self.textEntry.tag_remove('center', 1.0, 'end')
            except Exception as e:
                print(self.textEntry.tag_names())

            self.textEntry.tag_add('left', 1.0, 'end')
            self.textEntry.focus()

    def alignTextRight(self):       # Aligns text to the right
        self.textEntry.tag_configure('right', justify='right')
        currentTags = self.textEntry.tag_names(1.0)

        if 'right' in currentTags:
            self.textEntry.tag_remove('right', 1.0, 'end')
            self.textEntry.focus()
        else:
            try:
                self.textEntry.tag_remove('left', 1.0, 'end')
                self.textEntry.tag_remove('center', 1.0, 'end')
            except Exception as e:
                print(self.textEntry.tag_names())

            self.textEntry.tag_add('right', 1.0, 'end')
            self.textEntry.focus()

    def alignTextCenter(self):      # Aligns text in the center
        self.textEntry.tag_configure('center', justify='center')
        currentTags = self.textEntry.tag_names(1.0)

        if 'center' in currentTags:
            self.textEntry.tag_remove('center', 1.0, 'end')
            self.textEntry.focus()
        else:
            try:
                self.textEntry.tag_remove('right', 1.0, 'end')
                self.textEntry.tag_remove('left', 1.0, 'end')
            except Exception as e:
                print(self.textEntry.tag_names())

            self.textEntry.tag_add('center', 1.0, 'end')
            self.textEntry.focus()


if __name__ == '__main__':
    journal()
    

    