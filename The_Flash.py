import shelve
import time
import tkinter
import random
from tkinter import ttk
from tkinter import messagebox



class Element:
    """Creates individual element for the APQ"""
    def __init__(self, k, v, i):
        self._key = k
        self._value = v
        self._index = i

    def __eq__(self, other):
        if other != None:
            return self._key == other._key
        else:
            return False

    def __lt__(self, other):
        return self._key < other._key

    def _wipe(self):
        self._key = None
        self._value = None
        self._index = None

    def __str__(self):
        return f"{self._key} = key, {self._value} = value, {self._index} = index"


class Queue:

    def __init__(self):
        self.queue = []

    def add(self, x):
        self.queue.append(x)

    def remove(self):
        item = self.queue.pop(0)
        return item

    def move_to_end(self):
        y = self.remove()
        self.add(y)

    def length(self):
        return len(self.queue)


class APQ:
    """Creates an Adaptable Priority Queue"""

    def __init__(self):
        self.queue = []


    def add(self,key,item):
        """Add given key and item to the APQ"""
        e = Element(key, item, self.length())
        self.queue.append(e)
        self.bubble_up(e._index)
        return e

    def min(self):
        """Return the minimum key its value in the APQ"""
        return self.queue[0]._value, self.queue[0]._key

    def remove_min(self):
        """Remove the minimum element from the APQ"""
        if self.length() > 1: # If there are at least 2 elts in APQ, swap first with last, pop last, bubble down first
            self.queue[0], self.queue[self.length() - 1] = self.queue[self.length() - 1], self.queue[0]
            self.queue[0]._index = 0
            self.queue[self.length() - 1]._index = self.length() - 1
            removed_elt = self.queue.pop(self.length() - 1)
            self.bubble_down(0)
            return removed_elt
        elif self.length() == 1: # if only one elt in APQ, dont bother bubbling, just remove it
            removed_elt = self.queue.pop(0)
            return removed_elt
        else:   # otherwise do nothing as APQ is empty
            return None

    def length(self):
        """Return the length of the APQ"""
        return len(self.queue)

    def update_key(self, element, newkey):
        """Update the key of a specific element, then fix its position in APQ"""
        element._key = newkey
        if element._index != 0:  # If element is not first element, check if it should bubble up or down
            if self.queue[self.get_parent(element._index)]._key > self.queue[element._index]._key:
                self.bubble_up(element._index)
            elif self.get_rchild(element._index) < self.length():
                if self.queue[self.get_rchild(element._index)]._key < self.queue[element._index]._key:
                    self.bubble_down(element._index)
            elif self.get_lchild(element._index) < self.length():
                if self.queue[self.get_lchild(element._index)]._key < self.queue[element._index]._key:
                    self.bubble_down(element._index)
        else:   # if element is the first element, check whether it bubbles down to left or right child
            if self.get_rchild(element._index) < self.length():
                if self.queue[self.get_rchild(element._index)]._key < self.queue[element._index]._key:
                    self.bubble_down(element._index)
            elif self.get_lchild(element._index) < self.length():
                if self.queue[self.get_lchild(element._index)]._key < self.queue[element._index]._key:
                    self.bubble_down(element._index)
        return element


    def get_parent(self, index):
        """Return parent of given index"""
        return (index-1) // 2

    def get_lchild(self, index):
        """Return left child of given index"""
        return (index*2) + 1

    def get_rchild(self, index):
        """Return right child of given index"""
        return (index*2) + 2

    def get_key(self, element):
        """Get key by element"""
        return element._key

    def get_element_by_value(self, value):
        """Get the element object by value"""
        for i in self.queue:
            if i._value == value:
                return i
        return None

    def get_key_by_value(self, value):
        """Get the key of an element by its balue"""
        for i in self.queue:
            if i._value == value:
                return i._key
        return None

    def remove(self, element):
        """Remove element from APQ by element reference"""
        if element._index == 0:  # If elt is in first index, use remove_min code
            ret_elt = self.remove_min()
            return ret_elt
        else:  # Otherwise, swap with last elt and pop, Since last elt has to be biggest, it will always use bubble down
            self.queue[element._index], self.queue[self.length() - 1] =  self.queue[self.length() - 1], self.queue[element._index]
            self.queue[element._index]._index = element._index
            self.bubble_down(element._index)
            removed_elt = self.queue.pop(self.length() - 1)
            return removed_elt

    def bubble_up(self, index):
        """Helper function to maintain position in APQ. Bubbles up
        the element to its correct place in the binary heap"""
        # while parent > child and current elt isn't first elt, bubble up current elt
        while index > 0 and self.queue[index]._key < self.queue[self.get_parent(index)]._key:
            self.queue[self.get_parent(index)]._index = index
            self.queue[index], self.queue[self.get_parent(index)] = self.queue[self.get_parent(index)], self.queue[index]
            index = self.get_parent(index)
            self.queue[index]._index = index

    def bubble_down(self, index):
        """Helper function to maintain position in APQ. Bubbles down
        the element to its correct place in the binary heap"""
        # While there is a left child (if there's a child, there will always be a left child, not always right)
        while self.get_lchild(index) < self.length():
            min_val = self.get_lchild(index)
            # If there is a right child (doesn't fall off list index)
            if self.get_rchild(index) < self.length():
                # Compare keys, set the smaller one as minimum value
                if self.queue[self.get_rchild(index)]._key < self.queue[self.get_lchild(index)]._key:
                    min_val = self.get_rchild(index)
            # If current key > minimum child, swap them around
            if self.queue[index]._key > self.queue[min_val]._key:
                self.queue[min_val]._index = index
                self.queue[index], self.queue[min_val] = self.queue[min_val], self.queue[index]
                index = min_val
                self.queue[index]._index = index
            else:
                break

    def __str__(self):
        mystr = ""
        for i in self.queue:
            mystr += f"{i._key}, {i._value}, {i._index} \n"
            mystr += "1 \n"
        return mystr


class Card:

    def __init__(self, l1 , l2):
        self.l1 = l1
        self.l2 = l2
        self.interval = 0
        self.last_grade = None
        self.date_done = None
        self.repetition = 0 # Number of times successfully recalled
        self.easiness = 2.5 # How fast interval grows

    def opposite(self, label):
        if label == self.l1:
            return self.l2
        elif label == self.l2:
            return self.l1
        else:
            return None


class Deck:

    def __init__(self, name):
        self.name = name
        self.new = []
        self.fails = Queue()
        self.due_repetitions = []
        self.all_repetitions = APQ()


    def check_repetitions(self):
        while True:
            if self.all_repetitions.min()[1] == 0:
                minimum = self.all_repetitions.remove_min()
                self.due_repetitions.append(minimum[0])
            else:
                break

    def check_total_size(self):
        t = len(self.new) + len(self.fails.queue) + len(self.due_repetitions) + len(self.all_repetitions.queue)
        return t

class IntervalAlgorithm:

    def algo(self, card):
        if card.last_grade >= 1:  # correct response
            if card.repetition == 0:
                card.interval = 1
            elif card.repetition == 1:
                card.interval = 6
            else:
                card.interval = card.interval * card.easiness
                card.easiness = card.easiness + (0.1 - (2 - card.last_grade) * (0.08 + (2 - card.last_grade) * 0.02))
                if card.easiness < 1.3:
                    card.easiness = 1.3
                card.repetition += 1
        else:  # incorrect response
            card.repetition = 0
            card.interval = 1
        return card


class MainWindow:

    def __init__(self):
        self.app = tkinter.Tk()
        self.tab_control = ttk.Notebook(self.app)
        self.cards = CardsTab(self.tab_control)
        self.decks = DecksTab(self.tab_control)
        self.declare_tabs()
        self.app.title("The Flash")
        self.app.protocol("WM_DELETE_WINDOW", self.on_closing)


    def declare_tabs(self):
        self.tab_control.add(self.decks.frame, text='Decks')
        self.tab_control.add(self.cards.frame, text='Cards')
        self.tab_control.grid(row=0, column=0)

    def on_closing(self):
        self.app.destroy()

class CardsTab:

    def __init__(self, parent):
        self.parent = parent
        self.frame = tkinter.Frame(self.parent)
        self.tab_control = ttk.Notebook(self.frame, width=370, height=220)
        self.repetitions = Repetitions(self.tab_control)
        self.new = New(self.tab_control)
        self.fails = Fails(self.tab_control)
        self.declare_tabs()
        self.position()

    def declare_tabs(self):
        self.tab_control.add(self.repetitions.frame, text='Repetitions')
        self.tab_control.add(self.new.frame, text='New')
        self.tab_control.add(self.fails.frame, text='Fails')

    def position(self):
        self.tab_control.grid(row=0, column=0)

class GeneralCardTab:

    def __init__(self, parent):
        self.parent = parent
        self.frame = tkinter.Frame(self.parent)
        self.current_card = None
        self.current_card_index = 0
        self.card_list = []
        self.cards_left = 0
        self.cards_left_label = tkinter.Label(self.frame, text="0")
        self.label1 = tkinter.Label(self.frame, text="Label1")
        self.label2 = tkinter.Label(self.frame, text="Label2")
        self.check_button = tkinter.Button(self.frame, text="Check", command=self.check)
        self.good = tkinter.Button(self.frame, text="Good", command=self.good)
        self.medium = tkinter.Button(self.frame, text="Medium", command=self.medium)
        self.bad = tkinter.Button(self.frame, text="Bad", command=self.bad)
        self.m = tkinter.Menu(self.frame, tearoff=0)
        self.m.add_command(label="Edit Card", command=self.edit)
        self.m.add_command(label="Delete Card", command=self.delete)
        self.frame.bind("<Button-3>", self.do_popup)
        self._position()

    def new_load(self):
        self.current_card_index = len(self.card_list) + 1
        self.label1['text'] = self.card_list[0].l1
        self.label2['text'] = " "

    def do_popup(self, event):
        try:
            self.m.tk_popup(event.x_root, event.y_root)
        finally:
            self.m.grab_release()

    def check(self):
        self.label2['text'] = self.card_list[self.current_card_index].l2


    def _position(self):
        self.cards_left_label.grid(row=0, column=1)
        self.label1.grid(row=1, column=1)
        self.label2.grid(row=2, column=1)
        self.check_button.grid(row=3, column=1)
        self.good.grid(row=4, column=0)
        self.medium.grid(row=4, column=1)
        self.bad.grid(row=4, column=2)

    def good(self):
        self.card_list[self.current_card_index].last_grade = 2
        self.next_card()

    def medium(self):
        self.card_list[self.current_card_index].last_grade = 1
        self.next_card()

    def bad(self):
        self.card_list[self.current_card_index].last_grade = 0
        self.next_card()

    def next_card(self):
        # To be overridden by each function anyway
        sm = IntervalAlgorithm()
        sm.algo(self.card_list[self.current_card_index])
        c = self.card_list.pop()
        if c.last_grade < 2:
            application.cards.fails.card_list.append(c)
        else:
            application.decks.loaded_deck.all_repetitions.append(c)
        if self.current_card_index > 0:
            self.current_card_index -= 1
        else:
            if len(self.card_list) > 0:
                self.current_card_index = len(self.card_list) + 1
            else:
                self.label1['text'] = " "
                self.label2['text'] = " "

        self.label1['text'] = self.card_list[self.current_card_index].l1
        self.label2['text'] = self.card_list[self.current_card_index].l2


    def edit(self):
        self.card_list = 1

    def delete(self):
        self.card_list = 1




class Repetitions(GeneralCardTab):

    def __init__(self, parent):
        super().__init__(parent)

    def next_card(self):
        # To be overridden by each function anyway
        sm = IntervalAlgorithm()
        sm.algo(self.card_list[self.current_card_index])

        self.current_card_index += 1
        self.label1['text'] = self.card_list[self.current_card_index].l1
        self.label2['text'] = self.card_list[self.current_card_index].l2




class New(GeneralCardTab):

    def __init__(self, parent):
        super().__init__(parent)

    def next_card(self):
        # To be overridden by each function anyway
        sm = IntervalAlgorithm()
        sm.algo(self.card_list[self.current_card_index])

        self.current_card_index += 1
        self.label1['text'] = self.card_list[self.current_card_index].l1
        self.label2['text'] = self.card_list[self.current_card_index].l2

class Fails(GeneralCardTab):

    def __init__(self, parent):
        super().__init__(parent)


'''Need to change size of each card. Need to implement system that laods label2 after pressing a button. Need to
implement edit card. Need to correctly implement loaded deck to each card tab.'''

class DecksTab:

    def __init__(self, parent):
        self.parent = parent
        self.frame = tkinter.Frame(self.parent)
        self.loaded_deck = None
        self.loaded_deck_label = tkinter.Label(self.frame, text="Currently Loaded Deck: None", wraplength=140)
        self.new_button = tkinter.Button(self.frame, text="New+", command=self.new)
        self.new_name_entry = tkinter.Entry(self.frame, text="New Deck")
        self.name_label = tkinter.Label(self.frame, text="Name")
        self.total_cards_label = tkinter.Label(self.frame, text="Total Cards")
        self.repetitions_label = tkinter.Label(self.frame, text="Repetitions Due")
        self.name_list = tkinter.Listbox(self.frame)
        self.total_list = tkinter.Listbox(self.frame)
        self.repetitions_list = tkinter.Listbox(self.frame)
        self._position()
        self.name_list.bind("<MouseWheel>", self.mousewheel1)
        self.total_list.bind("<MouseWheel>", self.mousewheel2)
        self.repetitions_list.bind("<MouseWheel>", self.mousewheel3)
        self.m = tkinter.Menu(self.frame, tearoff=0)
        self.m.add_command(label="Edit Deck", command=self.edit)
        self.m.add_command(label="Delete Deck", command=self.confirm)
        self.m.add_command(label="Load Deck", command=self.load)
        self.name_list.bind("<Button-3>", self.do_popup)
        # self.hard_refresh()
        self.soft_refresh()

    def confirm(self):
        answer = tkinter.messagebox.askokcancel(title='Confirmation',
                          message='Are you sure that you want to delete?')
        if answer:
            self.delete()

    def edit(self):
        name = self.name_list.get(self.name_list.curselection())
        d = storage.access_deck(name)
        wind = EditDeck(d)

    def delete(self):
        name = self.name_list.get(self.name_list.curselection())
        storage.remove_deck(name)
        self.soft_refresh()


    def do_popup(self, event):
        try:
            self.m.tk_popup(event.x_root, event.y_root)
        finally:
            self.m.grab_release()

    def load(self):
        name = self.name_list.get(self.name_list.curselection())
        deck = storage.access_deck(name)
        print(deck.name)
        application.cards.new.card_list = deck.new
        application.cards.new.new_load()
        application.cards.repetitions.card_list = deck.due_repetitions
        application.cards.repetitions.new_load()
        application.cards.fails.card_list = deck.fails.queue
        application.cards.fails.new_load()
        self.loaded_deck = deck
        self.loaded_deck_label['text'] = "Currently loaded deck: " + deck.name

    def _position(self):
        self.loaded_deck_label.grid(row=0, column=1)
        self.new_button.grid(row=1, column=0, sticky="e")
        self.new_name_entry.grid(row=1, column=1, sticky="w")
        self.name_label.grid(row=2, column=0)
        self.total_cards_label.grid(row=2, column=1)
        self.repetitions_label.grid(row=2, column=2)
        self.name_list.grid(row=3, column=0)
        self.total_list.grid(row=3, column=1)
        self.repetitions_list.grid(row=3, column=2)


    def new(self):
        d_name = self.new_name_entry.get()
        if d_name != "":
            d = Deck(d_name)
            wind = EditDeck(d)

    def soft_refresh(self):
        the_list = storage.all_decks()
        self.name_list.delete(0, 'end')
        self.total_list.delete(0, 'end')
        self.repetitions_list.delete(0, 'end')
        j = 0
        for i in the_list:
            temp = storage.access_deck(i)
            self.name_list.insert(j, temp.name)
            self.total_list.insert(j, temp.check_total_size())
            self.repetitions_list.insert(j, len(temp.due_repetitions))
            j += 1
        self.colour_coordinate()

    def colour_coordinate(self):
        i = 0
        while i < self.name_list.size():
            if i % 2 == 0:
                self.name_list.itemconfig(i, bg="ivory")
                self.total_list.itemconfig(i, bg="ivory")
                self.repetitions_list.itemconfig(i, bg="ivory")
            else:
                self.name_list.itemconfig(i, bg="light blue")
                self.total_list.itemconfig(i, bg="light blue")
                self.repetitions_list.itemconfig(i, bg="light blue")
            i += 1


    ''' Need method for commiting progress to save file upon exiting. Save after each repetition/newcard etc???? Might
    have a counter to save after x cards, otherwise might take too long to constantly access hard drive. Need to start
    with the card tabs. Need to test extensively to see if working. Need to implement dates for repetitions.'''

    def hard_refresh(self):
        the_list = storage.all_decks()
        self.name_list.delete(0, 'end')
        self.total_list.delete(0, 'end')
        self.repetitions_list.delete(0, 'end')
        j = 0
        for i in the_list:
            temp = storage.access_deck(i)
            temp.check_repetitions()
            self.name_list.insert(j, temp.name)
            self.total_list.insert(j, temp.check_total_size())
            self.repetitions_list.insert(j, len(temp.due_repetitions))
            j += 1

        self.colour_coordinate()


    def mousewheel1(self, event):
        self.total_list.yview_scroll(-4 * int(event.delta / 120), "units")
        self.repetitions_list.yview_scroll(-4 * int(event.delta / 120), "units")

    def mousewheel2(self, event):
        self.name_list.yview_scroll(-4 * int(event.delta / 120), "units")
        self.repetitions_list.yview_scroll(-4 * int(event.delta / 120), "units")

    def mousewheel3(self, event):
        self.name_list.yview_scroll(-4 * int(event.delta / 120), "units")
        self.total_list.yview_scroll(-4 * int(event.delta / 120), "units")





    """Simple list of all decks with options of deleting decks and editing decks)"""






class EditDeck:

    def __init__(self, deck):
        self.window = tkinter.Tk()
        self.deck = deck
        try:
            self.current_deck = storage.access_deck(self.deck)
        except:
            self.current_deck = deck
        self.deck_name_entry = tkinter.Entry(self.window)
        self.deck_name_entry.insert(0, self.current_deck.name)
        self.var = 0
        self.old_name = self.current_deck.name
        self.e1 = tkinter.Entry(self.window)
        self.e2 = tkinter.Entry(self.window)
        self.checkbox = tkinter.Checkbutton(self.window, text="2 sided", variable=self.var, command=self.checkbutton)
        self.checkbox.var = self.var
        self.add_button = tkinter.Button(self.window, text="Add", command=self.add_card)
        self.save_button = tkinter.Button(self.window, text="Save", command=self.save)
        self.total_cards_label = tkinter.Label(self.window, text="Total cards: 0")
        self.list1 = tkinter.Listbox(self.window)
        self.list2 = tkinter.Listbox(self.window)
        self._position()
        self.m = tkinter.Menu(self.list1, tearoff=0)
        self.m2 = tkinter.Menu(self.list2, tearoff=0)
        self.m.add_command(label="Delete Card", command=self.delete)
        self.m2.add_command(label="Delete Card", command=self.delete)
        self.m.add_command(label="Edit Card", command=self.edit)
        self.m2.add_command(label="Edit Card", command=self.edit)
        self.list1.bind("<Button-3>", self.do_popup)
        self.list2.bind("<Button-3>", self.do_popup)
        self.list1.bind("<MouseWheel>", self.mousewheel1)
        self.list2.bind("<MouseWheel>", self.mousewheel2)
        self.deck_name_entry.bind("<Button-1>", self.change_state)
        self.fill_tables()
        self.total_cards = self.list1.size()
        self.total_cards_label['text'] = "Total cards: " + str(self.total_cards)
        self.deck_name_entry['state'] = tkinter.DISABLED


    def change_state(self, event):
        if self.deck_name_entry['state'] == tkinter.DISABLED:
            self.deck_name_entry['state'] = tkinter.NORMAL
        else:
            self.deck_name_entry['state'] = tkinter.DISABLED

    def mousewheel1(self, event):
        self.list2.yview_scroll(-4 * int(event.delta / 120), "units")

    def mousewheel2(self, event):
        self.list1.yview_scroll(-4 * int(event.delta / 120), "units")

    def do_popup(self, event):
        try:
            self.m.tk_popup(event.x_root, event.y_root)
        finally:
            self.m.grab_release()

    def edit(self):
        if self.list1.index(tkinter.ACTIVE) is not None:
            number = self.list1.index(tkinter.ACTIVE)
            name1 = self.list1.get(tkinter.ACTIVE)
            name2 = self.list2.get(number)
        else:
            number = self.list2.index(tkinter.ACTIVE)
            name1 = self.list2.get(tkinter.ACTIVE)
            name2 = self.list1.get(number)
        for i in self.current_deck.new:
            if i.l1 == name1 or i.l1 == name2:
                if i.l2 == name1 or i.l2 == name2:
                    s = EditCard(i)
                    return
        for i in self.current_deck.due_repetitions:
            if i.l1 == name1 or i.l1 == name2:
                if i.l2 == name1 or i.l2 == name2:
                    s = EditCard(i)
                    return
        for i in self.current_deck.fails.queue:
            if i.l1 == name1 or i.l1 == name2:
                if i.l2 == name1 or i.l2 == name2:
                    s = EditCard(i)
                    return
        for i in self.current_deck.all_repetitions.queue:
            if i._value.l1 == name1 or i._value.l1 == name2:
                if i._value.l2 == name1 or i._value.l2 == name2:
                    s = EditCard(i._value)
                    return


    def checkbutton(self):
        if self.var == 0:
            self.var = 1
        else:
            self.var = 0

    def _position(self):
        self.deck_name_entry.grid(row=0, column=0)
        self.e1.grid(row=1, column=0)
        self.e2.grid(row=1, column=1)
        self.checkbox.grid(row=2, column=0)
        self.add_button.grid(row=3, column=0)
        self.save_button.grid(row=3, column=1)
        self.total_cards_label.grid(row=4, column=0)
        self.list1.grid(row=5, column=0)
        self.list2.grid(row=5, column=1)

    def add_card(self):
        e1 = self.e1.get()
        e2 = self.e2.get()
        if not (e1 == "" or e2 == ""):
            c = Card(e1, e2)
            self.current_deck.new.append(c)
            print(self.var)
            if self.var == 1:
                print("hi")
                c1 = Card(e2, e1)
                self.current_deck.new.append(c1)
        self.e1.delete(0, 'end')
        self.e2.delete(0, 'end')
        self.fill_tables()
        self.total_cards = self.list1.size()
        self.total_cards_label['text'] = "total cards:", self.total_cards
        self.list1.yview(tkinter.END)
        self.list2.yview(tkinter.END)

    def fill_tables(self):
        self.list1.delete(0, 'end')
        self.list2.delete(0, 'end')
        j = 0
        for i in self.current_deck.new:
            self.list1.insert(j, i.l1)
            self.list2.insert(j, i.l2)
            j += 1
        for i in self.current_deck.fails.queue:
            self.list1.insert(j, i.l1)
            self.list2.insert(j, i.l2)
            j += 1
        for i in self.current_deck.due_repetitions:
            self.list1.insert(j, i.l1)
            self.list2.insert(j, i.l2)
            j += 1
        for i in self.current_deck.all_repetitions.queue:
            self.list1.insert(j, i._value.l1)
            self.list2.insert(j, i._value.l2)
            j += 1
        self.colour_coordinate()



    def delete(self):
        if self.list1.index(tkinter.ACTIVE) is not None:
            number = self.list1.index(tkinter.ACTIVE)
            name1 = self.list1.get(tkinter.ACTIVE)
            name2 = self.list2.get(number)
        else:
            number = self.list2.index(tkinter.ACTIVE)
            name1 = self.list2.get(tkinter.ACTIVE)
            name2 = self.list1.get(number)
        card_counter = 0
        list_index = 0
        for card in self.current_deck.new:
            if card.l1 == name1:
                if card.l2 == name2:
                    card_counter += 1
                    del self.current_deck.new[list_index]
            if self.var == 1:
                if card.l1 == name2:
                    if card.l2 == name1:
                        card_counter += 1
                        del self.current_deck.new[list_index]
            if self.var == 1:
                if card_counter == 2:
                    return
            else:
                if card_counter == 1:
                    return
            list_index += 1
        list_index = 0
        for card in self.current_deck.fails.queue:
            if card.l1 == name1:
                if card.l2 == name2:
                    card_counter += 1
                    del self.current_deck.fails.queue[list_index]
            if self.var == 1:
                if card.l1 == name2:
                    if card.l2 == name1:
                        card_counter += 1
                        del self.current_deck.fails.queue[list_index]
            if self.var == 1:
                if card_counter == 2:
                    return
            else:
                if card_counter == 1:
                    return
            list_index += 1
        list_index = 0
        for card in self.current_deck.due_repetitions:
            if card.l1 == name1:
                if card.l2 == name2:
                    card_counter += 1
                    del self.current_deck.due_repetitions[list_index]
            if self.var == 1:
                if card.l1 == name2:
                    if card.l2 == name1:
                        card_counter += 1
                        del self.current_deck.due_repetitions[list_index]
            if self.var == 1:
                if card_counter == 2:
                    return
            else:
                if card_counter == 1:
                    return
            list_index += 1
        list_index = 0
        for card in self.current_deck.all_repetitions.queue:
            if card._value.l1 == name1:
                if card._value.l2 == name2:
                    card_counter += 1
                    del self.current_deck.all_repetitions.queue[list_index]
            if self.var == 1:
                if card.l1 == name2:
                    if card._value.l2 == name1:
                        card_counter += 1
                        del self.current_deck.all_repetitions.queue[list_index]
            if self.var == 1:
                if card_counter == 2:
                    return
            else:
                if card_counter == 1:
                    return
            list_index += 1
        self.fill_tables()
        self.total_cards = self.list1.size()
        self.total_cards_label['text'] = "total cards:", self.total_cards

    def colour_coordinate(self):
        i = 0
        while i < self.list1.size():
            if i % 2 == 0:
                self.list1.itemconfig(i, bg="ivory")
                self.list2.itemconfig(i, bg="ivory")

            else:
                self.list1.itemconfig(i, bg="light blue")
                self.list2.itemconfig(i, bg="light blue")
            i += 1


    def save(self):
        if self.deck_name_entry.get() != self.old_name:
            storage.remove_deck(self.old_name)
            self.current_deck.name = self.deck_name_entry.get()
        name = self.deck_name_entry.get()
        cd = self.current_deck
        storage.save_deck(name, cd)
        time.sleep(0.25)
        application.decks.soft_refresh()
        self.window.destroy()

    ''' Need to have decks tab actively read database and update each time,Need to have another look at the delete card.'''

class EditCard:

    def __init__(self, card):
        self.window = tkinter.Tk()
        self.e1 = tkinter.Entry(self.window)
        self.e2 = tkinter.Entry(self.window)
        self.card = card
        self.e1.insert(0, self.card.l1)
        self.e2.insert(0, self.card.l2)
        self.save = tkinter.Button(self.window, text="Save", command=self.save)

    def save(self):
        self.card.l1 = self.e1.get()
        self.card.l2 = self.e2.get()
        self.window.destroy()

    '''Need to handle database somewhere or handle the list where card is stored.'''

class DeckFile:

    def __init__(self):
        self.name = "Decks"


    def access_deck(self, name):
        st = shelve.open(self.name)
        temp = st[name]
        st.close()
        return temp

    def all_decks(self):
        st = shelve.open(self.name)
        mylist = list(st.keys())
        st.close()
        return mylist

    def save_deck(self, name, value):
        st = shelve.open(self.name, writeback=True)
        st[name] = value
        st.close()

    def remove_deck(self, name):
        st = shelve.open(self.name, writeback=True)
        del st[name]
        st.close()

    '''Might need to add a bunch of checks to run at start of entire program and at end of entire program.'''


storage = DeckFile()
application = MainWindow()
application.app.mainloop()

