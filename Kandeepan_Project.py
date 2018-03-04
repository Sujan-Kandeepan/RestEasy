#import statements for graphics, file dialogs and reading from csv files
import math
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import csv

#Item class to be instantiated to create new objects of type Item (stored in inventory)
class Item:
    #Variables for item number, quantity, item name, item location, and item description
    number, quantity, name, location, description = None, None, None, None, None

    #Constructor with arguments, initializes all variables using parameter values
    def __init__(self, number, quantity, name, location, description):
        self.number = number
        self.quantity = quantity
        self.name = name
        self.location = location
        self.description = description

    #Accessor methods (get values)
    def getNumber(self):
        return self.number

    def getQuantity(self):
        return self.quantity

    def getName(self):
        return self.name

    def getLocation(self):
        return self.location

    def getDescription(self):
        return self.description

    #Mutator mmethods (set values)
    def setNumber(self, number):
        self.number = number

    def setQuantity(self, quantity):
        self.quantity = quantity

    def setName(self, name):
        self.name = name

    def setLocation(self, location):
        self.location = location

    def setDescription(self, description):
        self.description = description

    #String method (display item information neatly)
    def __str__(self):
        string = ""
        string += "Number: " + str(self.number)
        string += "\nQuantity: " + str(self.quantity)
        string += "\nName: " + self.name
        string += "\nLocation: " + self.location
        string += "\nDescription: " + self.description + "\n"
        return string

class Inventory:
    #List of items, objects of type Item
    itemList = []

    #String variable to switch between confirming deletion of items and specifying how data should be loaded
    deletemode = ""

    #Method to modify deletemode variable
    def setDeletemode(self, value):
        self.deletemode = value

    #Method to add an item to the list, remains sorted
    def add(self, number, quantity, name, location, description, label):
        #Removing trailing new-line characters in string parameter arguments
        number = number.strip()
        quantity = quantity.strip()
        name = name.strip()
        location = location.strip()
        description = description.strip()

        #Attempting to add item, checking that all required preconditions are met
        try:
            #Throwing error if item with given item number already exists
            if self.search(eval(number)) != -1:
                label.config(text = "Error: Item number taken!")
                raise IndexError

            #Throwing error if item number and quantity are not given as positive integers
            if type(eval(number)) != int or type(eval(quantity)) != int: raise NameError
            if eval(number) < 0 or eval(quantity) < 0: raise ValueError

            #Adding item to list, using merge sort to keep it sorted
            self.itemList.append(Item(eval(number), eval(quantity), name.strip(), location.strip(), description.strip()))
            self.itemList = self.mergeSort(self.itemList)

            #Updating status label to show that item was added
            label.config(text = "Item #" + str(number).strip() + " added to inventory")

        #Handling errors, updating status label to reflect each possible type of error
        except SyntaxError:
            label.config(text = "Error: One or more entry fields are empty!")
        except NameError:
            label.config(text = "Error: Item number and quantity must be integers!")
        except ValueError:
            label.config(text = "Error: Item number and quantity must be positive!")
        except IndexError:
            label.config(text = "Error: Item number taken!")

    #Method for sorting the list each time an item is added, uses the merge sort algorithm
    def mergeSort(self, l):
        #Returning entire list if length is 0 or 1
        if len(l) == 0 or len(l) == 1:
            return l
        #Returning sorted pair of items if list is exactly 2
        elif len(l) == 2:
            if l[0].getNumber() < l[1].getNumber():
                return [l[0],l[1]]
            else:
                return [l[1],l[0]]
        else:
            #Dividing list in two, merge sorting each half
            first = self.mergeSort(l[:len(l) // 2])
            second = self.mergeSort(l[len(l) // 2:])

            #Combining lists by removing the smallest item from either list and adding it to the new list
            newlist = []
            while len(first) != 0 and len(second) != 0:
                if first[0] .getNumber()< second[0].getNumber():
                    newlist.append(first[0])
                    first = first[1:]
                else:
                    newlist.append(second[0])
                    second = second[1:]

            #Cases where one or both halves are now empty, append any non-empty half to the end of the new list and return it
            if len(first) == 0 and len(second) == 0:
                return newlist
            elif len(first) != 0:
                return newlist + first
            else:
                return newlist + second

    #Method to remove an item from the list, given its item number
    def delete(self, numberBox, quantityBox, nameBox, locationBox, descriptionBox, label):
        #Taking values from text fields and passing them into variables
        number = numberBox.get('1.0', END).strip()
        quantity = quantityBox.get('1.0', END).strip()
        name = nameBox.get('1.0', END).strip()
        location = locationBox.get('1.0', END).strip()
        description = descriptionBox.get('1.0', END).strip()

        try:
            #Item found, will be deleted
            if self.search(eval(number)) != -1:
                #Updating status label to show that the item was deleted
                label.config(text = "Removed item #" + str(self.itemList[self.search(eval(number))].getNumber()))

                #Remoivng item form the list
                self.itemList.remove(self.itemList[self.search(eval(number))])

                #Clearing text fields after deleeting item since it no longer exists
                numberBox.delete('1.0', END)
                quantityBox.delete('1.0', END)
                nameBox.delete('1.0', END)
                locationBox.delete('1.0', END)
                descriptionBox.delete('1.0', END)

            #Item not found, nothing to be deleted
            else:
                label.config(text = "Error: Item not found!")

        #Handling case where one or more entry fields are empty, updating status label to show this
        except:
            label.config(text = "Error: One or more entry fields are empty!")

    #Method for enabling delete confirmation buttons and disabling all others
    def confirmButtons(self, newButton, deleteButton, searchButton, updateButton, loadButton, saveButton, yesButton, noButton):
        #Disabling all buttons except for Yes and No
        newButton.config(state = DISABLED)
        deleteButton.config(state = DISABLED)
        searchButton.config(state = DISABLED)
        updateButton.config(state = DISABLED)
        loadButton.config(state = DISABLED)
        saveButton.config(state = DISABLED)

        #Enabling Yes and No buttons
        yesButton.config(state = NORMAL)
        noButton.config(state = NORMAL)

    #Method for restoring buttons to their original states
    def regularButtons(self, newButton, deleteButton, searchButton, updateButton, loadButton, saveButton, yesButton, noButton):
        #Enabling all buttons except for Yes and No
        newButton.config(state = NORMAL)
        deleteButton.config(state = NORMAL)
        searchButton.config(state = NORMAL)
        updateButton.config(state = NORMAL)
        loadButton.config(state = NORMAL)
        saveButton.config(state = NORMAL)

        #Disabling Yes and No buttons
        yesButton.config(state = DISABLED)
        noButton.config(state = DISABLED)

    #Method to search for an item the list using binary search, given its item number, returns an index
    def search(self, number):
        #List is empty, item cannot be found in an empty list
        if len(self.itemList) == 0: return -1

        #Getting indexes at the start, end and middle of the item list
        start, end, midpoint = 0, len(self.itemList) - 1, (len(self.itemList) - 1) // 2

        #Iterating until item is found or proven to not exist
        while start <= end:
            #Item proven to not exist in the list
            if start == end and self.itemList[start].getNumber() != number: return -1

            #Item found, will be returned
            if self.itemList[midpoint].getNumber() == number: return midpoint

            #Item must be in the second half of the list, will search there
            elif self.itemList[midpoint].getNumber() < number:
                start = midpoint + 1
                midpoint = math.ceil((midpoint + end) / 2)

            #Item must be in the first half of the list, will search there
            else:
                end = midpoint - 1
                midpoint = math.floor((start + midpoint) / 2)
        return -1

    #Method for returning the entire object found when doing a search for an item, or an error message if it was not found
    def searchResult(self, numberBox, quantityBox, nameBox, locationBox, descriptionBox, statusLabel):
        #Taking value for item number from text box and storing it into a variable
        number = numberBox.get('1.0', END).strip()

        #Item found, will be displayed
        if number.strip() != "" and self.search(eval(number.strip())) != -1:
            #Creating an object identical to the one that was found, working with that instead
            found = self.itemList[self.search(eval(number.strip()))]

            #Clearing text fields
            numberBox.delete('1.0', END)
            quantityBox.delete('1.0', END)
            nameBox.delete('1.0', END)
            locationBox.delete('1.0', END)
            descriptionBox.delete('1.0', END)

            #Inserting info about found item into text fields
            numberBox.insert(INSERT, found.getNumber())
            quantityBox.insert(INSERT, found.getQuantity())
            nameBox.insert(INSERT, found.getName())
            locationBox.insert(INSERT, found.getLocation())
            descriptionBox.insert(INSERT, found.getDescription())

            #Updating status label to reflect what just happened
            statusLabel.config(text = "Item found, information for item #" + number.strip() + " displayed")

        #Item not found, updating status label to reflect this
        else:
            statusLabel.config(text = "Error: Item not found!")

    def update(self, number, quantity, name, location, description, statusLabel):
        #Removing trailing new-line characters in string parameter arguments
        number = number.strip()
        quantity = quantity.strip()
        name = name.strip()
        location = location.strip()
        description = description.strip()

        try:
            #Item found, will be updated
            if self.search(eval(number.strip())) != -1:
                #Updating item information
                index = self.search(eval(number))
                self.itemList[index].setQuantity(eval(quantity))
                self.itemList[index].setName(name.strip())
                self.itemList[index].setLocation(location.strip())
                self.itemList[index].setDescription(description.strip())

                #Updating status label to show that item was updated
                statusLabel.config(text = "Item #" + number.strip() + " updated!")

            #Throwing error if item wasn't found
            else:
                raise IndexError

            #Throwing error if item number and quantity are not given as positive integers
            if type(eval(number)) != int or type(eval(quantity)) != int: raise NameError
            if eval(number) < 0 or eval(quantity) < 0: raise ValueError

        #Handling errors, updating status label to reflect each possible type of error
        except NameError:
            statusLabel.config(text = "Error: Item number and quantity must be integers!")
        except ValueError:
            statusLabel.config(text = "Error: Item number and quantity must be positive!")
        except IndexError:
            statusLabel.config(text = "Error: Item not found!")
        except:
            statusLabel.config(text = "Error: One or more entry fields are empty!")

    #Method for loading inventory data using a text file, adds to existing inventory
    def loadExtra(self, filename, label):
        #Storing a temporary list to restore if anything goes wrong
        preserved = self.itemList
        try:
            #Throwing error if file is not of .txt or .csv format
            if not (filename.endswith('.txt') or filename.endswith('.csv')):
                raise NameError

            #Opening file, trying to load
            with open(filename, 'r') as f:
                #Storing lines in file in a list
                filecontents = f.read().split('\n')
                for i in filecontents:
                    #Dividing lines in list into attributes
                    attributes = i.split(',')

                    #Item not found, adding new item
                    if self.search(eval(attributes[0])) == -1:
                        self.add(attributes[0], attributes[1], attributes[2], attributes[3], attributes[4], label)

                    #Item exists already, will just update it
                    else:
                        self.update(attributes[0], attributes[1], attributes[2], attributes[3], attributes[4], label)

                    #Updating status label to show that inventory data was successfully loaded
                    label.config(text = "Existing data preserved, inventory data loaded successfully!")

        #Throwing error if file is invalid for any reason, restoring preserved list
        except NameError:
            self.itemList = preserved
            label.config(text = "Error: must choose a .txt or .csv file!")
        except:
            self.itemList = preserved
            label.config(text = "Error: invalid file chosen, items must be on separate\n \
            lines with attributes separated by commas!")

    #Method for loading inventory data using a text file, overwrites existing inventory
    def loadNew(self, filename, label):
        #Updating status label to show that inventory data was successfully loaded
        label.config(text = "Existing data overwritten, inventory data loaded successfully!")

        #Clearing list, then loading new data using same method as loadExtra method
        self.itemList = []
        self.loadExtra(filename, label)

    #Method for saving inventory data using a text file
    def save(self, filename, label):
        try:
            #Throwing error if file is not of .txt or .csv format
            if not (filename.endswith('.txt') or filename.endswith('.csv')):
                raise NameError

            #Opening file, trying to save
            with open(filename, 'w') as f:
                #Writing item information to file, line by line per item and with attributes separated by commas
                for i in range(len(self.itemList)):
                    f.write(str(self.itemList[i].getNumber()) + ',')
                    f.write(str(self.itemList[i].getQuantity()) + ',')
                    f.write(self.itemList[i].getName() + ',')
                    f.write(self.itemList[i].getLocation() + ',')
                    f.write(self.itemList[i].getDescription())
                    if i != len(self.itemList) - 1: f.write('\n')

            #Updating status label to inventory data was successfully saved
            label.config(text = "Inventory saved to " + filename + "!")

        #Throwing error if file is invalid for any reason, restoring preserved list
        except NameError:
            label.config(text = "Error: must choose a .txt or .csv file!")
        except:
            label.config(text = "Error: file invalid or does not exist!")

    #Method for initializing GUI and placing all elements on screen
    def __init__(self, master):
        #initializing main frame
        mainFrame = Frame(master, relief = SUNKEN, padx = 10, pady = 10, bg = "gray15")
        mainFrame.grid(row = 0, column = 0, rowspan = 10, columnspan = 10, sticky = "NWES")

        #Left labels for item information display
        titleLabel = Label(mainFrame, text = "DISPLAY/UPDATE ITEM INFORMATION", \
            bg = "gray15", fg = "dark orange", font = "arial 16 bold")
        titleLabel.grid(row = 0, column = 0, columnspan = 5, padx = 20, sticky = "W")

        numberLabel = Label(mainFrame, text = "Number:", bg = "gray15", fg = "white", font = "arial 10 bold")
        numberLabel.grid(row = 1, column = 0, sticky = "E")

        quantityLabel = Label(mainFrame, text = "Quantity:", bg = "gray15", fg = "white", font = "arial 10 bold")
        quantityLabel.grid(row = 2, column = 0, sticky = "E")

        nameLabel = Label(mainFrame, text = "Name:", bg = "gray15", fg = "white", font = "arial 10 bold")
        nameLabel.grid(row = 3, column = 0, sticky = "E")

        locationLabel = Label(mainFrame, text = "Location:", bg = "gray15", fg = "white", font = "arial 10 bold")
        locationLabel.grid(row = 4, column = 0, sticky = "E")

        descriptionLabel = Label(mainFrame, text = "Description:", bg = "gray15", fg = "white", font = "arial 10 bold")
        descriptionLabel.grid(row = 5, column = 0, sticky = "E")

        #Bottom text for status/errors
        statusLabel = Label(mainFrame, text = "Instructions for this program can be viewed in the console",\
            bg = "gray15", fg = "white", font = "arial 12 bold")
        statusLabel.grid(row = 7, column = 0, columnspan = 5, padx = 5, pady = 10, sticky = "S")

        #Text fields for item information display
        numberBox = Text(mainFrame, height = 1, width = 40, bg = "gray75", font = "arial 10 bold")
        numberBox.grid(row = 1, column = 1, columnspan = 3, padx = 5, pady = 5, sticky = "NWES")

        quantityBox = Text(mainFrame, height = 1, width = 40, bg = "gray75", font = "arial 10 bold")
        quantityBox.grid(row = 2, column = 1, columnspan = 3, padx = 5, pady = 5, sticky = "NWES")

        nameBox = Text(mainFrame, height = 1, width = 40, bg = "gray75", font = "arial 10 bold")
        nameBox.grid(row = 3, column = 1, columnspan = 3, padx = 5, pady = 5, sticky = "NWES")

        locationBox = Text(mainFrame, height = 1, width = 40, bg = "gray75", font = "arial 10 bold")
        locationBox.grid(row = 4, column = 1, columnspan = 3, padx = 5, pady = 5, sticky = "NWES")

        descriptionBox = Text(mainFrame, height = 1, width = 40, bg = "gray75", font = "arial 10 bold")
        descriptionBox.grid(row = 5, column = 1, columnspan = 3, padx = 5, pady = 5, sticky = "NWES")

        #Button to create new inventory record
        newButton = Button(mainFrame, text = "New", bg = "steelblue1", fg = "black", width = 12, font = "arial 10 bold", \
            command = lambda: self.add(numberBox.get('1.0', END), quantityBox.get('1.0', END), nameBox.get('1.0', END),
            locationBox.get('1.0', END), descriptionBox.get('1.0', END), statusLabel))
        newButton.grid(row = 0, column = 4, sticky = "E", padx = 5, pady = 5)

        #Button to delete currently displayed inventory record
        deleteButton = Button(mainFrame, text = "Delete", bg = "steelblue1", fg = "black", width = 12, font = "arial 10 bold", \
            command = lambda: (statusLabel.config(text =
            "Do you really want to delete the displayed item? Is all info correct?"),
            self.confirmButtons(newButton, deleteButton, searchButton, updateButton, loadButton, saveButton, yesButton,
            noButton), self.setDeletemode("delete"), deleteLabel.config(text = "Confirm delete:")))
        deleteButton.grid(row = 1, column = 4, sticky = "E", padx = 5, pady = 5)

        #Button to search inventory for specified item
        searchButton = Button(mainFrame, text = "Search", bg = "steelblue1", fg = "black", width = 12, font = "arial 10 bold", \
            command = lambda: self.searchResult(numberBox, quantityBox, nameBox, locationBox, descriptionBox, statusLabel))
        searchButton.grid(row = 2, column = 4, sticky = "E", padx = 5, pady = 5)

        #Button to update item information
        updateButton = Button(mainFrame, text = "Update", bg = "steelblue1", fg = "black", width = 12, font = "arial 10 bold", \
            command = lambda: self.update(numberBox.get('1.0', END), quantityBox.get('1.0', END), nameBox.get('1.0', END),
            locationBox.get('1.0', END), descriptionBox.get('1.0', END), statusLabel))
        updateButton.grid(row = 3, column = 4, sticky = "E", padx = 5, pady = 5)

        #Button to initiate command to load inventory data from a separate file, more options given later
        loadButton = Button(mainFrame, text = "Load", bg = "steelblue1", fg = "black", width = 12, font = "arial 10 bold", \
            command = lambda: (self.setDeletemode("load"),
            self.confirmButtons(newButton, deleteButton, searchButton, updateButton, loadButton, saveButton, yesButton,
            noButton), deleteLabel.config(text = "Overwrite data:")))
        loadButton.grid(row = 4, column = 4, sticky = "E", padx = 5, pady = 5)

        #Button to save inventory data to a separate file
        saveButton = Button(mainFrame, text = "Save", bg = "steelblue1", fg = "black", width = 12, font = "arial 10 bold", \
            command = lambda: self.save(filedialog.askopenfilename(), statusLabel))
        saveButton.grid(row = 5, column = 4, sticky = "E", padx = 5, pady = 5)

        #Label which shows beside 'Yes' and 'No' buttons to indicate what they are for
        deleteLabel = Label(mainFrame, text = "Confirm delete:", bg = "gray15", fg = "white", font = "arial 10 bold")
        deleteLabel.grid(row = 6, column = 1, sticky = "E")

        #Button to either confirm deletion of items or allow existing data to be overwriiten when loading from a file
        yesButton = Button(mainFrame, text = "Yes", state = DISABLED, bg = "springgreen4", fg = "white", width = 12, \
            font = "arial 10 bold", command = lambda: ((self.delete(numberBox, quantityBox, nameBox, locationBox,
            descriptionBox, statusLabel) if self.deletemode == "delete" else self.loadNew(filedialog.askopenfilename(),
            statusLabel)), self.regularButtons(newButton, deleteButton, searchButton, updateButton,
            loadButton, saveButton, yesButton, noButton)))
        yesButton.grid(row = 6, column = 2, padx = 10, pady = 5, sticky = "E")

        #Button to either cancel deletion of items or prevent existing data to be overwriiten when loading from a file
        noButton = Button(mainFrame, text = "No", state = DISABLED, bg = "red2", fg = "white", width = 12, \
            font = "arial 10 bold", command = lambda: ((statusLabel.config(text = "Item not deleted")
            if self.deletemode == "delete" else self.loadExtra(filedialog.askopenfilename(), statusLabel)),
            self.regularButtons(newButton, deleteButton, searchButton, updateButton,
            loadButton, saveButton, yesButton, noButton)))
        noButton.grid(row = 6, column = 3, padx = 5, pady = 5, sticky = "E")

        #Button to close the program and its GUI
        exitButton = Button(mainFrame, text = "Exit", bg = "steelblue4", fg = "white", width = 12, \
            font = "arial 10 bold", command = master.destroy)
        exitButton.grid(row = 6, column = 4, sticky = "W", padx = 5, pady = 5)

#Method for printing user instructions into the command line
def instructions():
    print("\n***INSTRUCTIONS***")
    print("All items have an item number, quantity, item name, item location and item description.")
    print("Six main functions supported, controlled by the buttons on the right, explanations given below.")
    print("\nNew:")
    print("- Enter item number, quantity, name, location and description into respective text fields.")
    print("- Press the 'New' button to add a new item with those attributes to the inventory.")
    print("\nDelete:")
    print("- Have all information about an item showing in the text fields.")
    print("- The easiest way to do this would be using the search function.")
    print("- Press the 'Delete' button once all information has been entered.")
    print("- Press the 'Yes' button when it appears to confirm, or the 'No' button to cancel.")
    print("\nSearch:")
    print("- Enter the item number of the item you would like to search for into the first text field.")
    print("- Then press the 'Search' button to fill the rest of the text fields with complete information about that item.")
    print("\nUpdate:")
    print("- Enter the item number of the item you would like to update into the first text field.")
    print("- Enter the rest of the item's new information in the text fields below it.")
    print("- Press the 'Update' button to have the item information updated.")
    print("- This will only work for items that are already in the list.")
    print("\nLoad:")
    print("- Press the 'Load' button to load new inventory data from a file.")
    print("- When asked if you would like to overwrite existing data, press the 'Yes' button to have the program load an")
    print("  entirely new set of data, or the 'No' button to simply add to the existing data without erasing any of it.")
    print("- Items in the file will replace any items with the same item number regardless.")
    print("- Select a file in the file dialog which comes up, the information will then be loaded.")
    print("- Files should follow the file format given at the bottom of these instructions.")
    print("\nSave:")
    print("- Press the 'Save' button to save all inventory data to a file.")
    print("- Select a file in the file dialog which comes up, the information will then be saved.")
    print("- The file will be saved according to the file format given at the bottom of these instructions.")
    print("\nFile format:")
    print("------------------------------------------------------------------")
    print("| 1111111,170,wrenches,Warehouse B,steel wrenches                |")
    print("| 3333333,133,screws,Warehouse A,standard screws                 |")
    print("| 2222222,21,screwdrivers,Warehouse C,Large philips screwdrivers |")
    print("|                               ...                              |")
    print("------------------------------------------------------------------")

#Main method, brings up GUI and rus program
def main():
    #Display instructions in the command line, all interacton happens in GUI
    instructions()

    #Set up GUI, instantiate Inventory object which contains main program and interface
    master = Tk()
    Inventory(master)

    #Configure window title and background
    master.title("RestEasy Inventory - Sujan's Final Project")
    master.config(bg = "gray15")

    #GUI remains open until user exits program
    master.mainloop()
    exit()

if __name__ == main():
    main()
