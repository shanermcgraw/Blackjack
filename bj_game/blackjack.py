import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk

import random
import collections
import time

MAX_CARD_HAND = 5

""" Move window to right monitor, resizing screen on window resize, not showing score of both cards before card is flipped

"""

class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title = "Blackjack")
        self._insertedCards = 0
        self._eInsertedCards = 0
        self._playerScore = 0
        self._enemyScore = 0
        self._isCardDown = False

        self.set_screen_size()
         
        self.create_start_button()            

    def set_screen_size(self):
        screen = self.get_screen()
        monitors = []
        for m in range(screen.get_n_monitors()):
            monitors.append(screen.get_monitor_geometry(m))
        current_monitor = screen.get_monitor_at_window(screen.get_active_window())
        self.set_default_size(monitors[current_monitor].width / 2, monitors[current_monitor].height / 1.3)

        self.set_border_width(10) 
        self.move(0, 0)

    def create_start_button(self):
        self._box = Gtk.Box(Gtk.BaselinePosition.CENTER)
        self.add(self._box)
        self._box.set_halign(Gtk.Align.CENTER)
        self._box.set_valign(Gtk.Align.CENTER)
        self._bjButton = Gtk.Button(label = "Start Blackjack Game")
        self._box.pack_start(self._bjButton, True, True, 0) 

    def remove_start_button(self):
        self.remove(self._box)

    def create_player_hand(self):
        self._pCardTable = Gtk.Table()
        self.add(self._pCardTable)
        self._pCardTable.resize(10, 20)
        self._pCardTable.set_homogeneous(False)
        #self._pCardTable.set_resize_mode(Gtk.ResizeMode.QUEUE)

        self._pCardTable.set_row_spacings(60)
        self._pCardTable.set_col_spacings(20)

        self._buttonTable = Gtk.Table()
        self._buttonTable.set_homogeneous(False)
        self._buttonTable.resize(8,6)
        self._buttonTable.set_col_spacings(20)
        self._buttonTable.set_row_spacings(5)
        
        self._hitButton = Gtk.Button(label = "Hit")
        self._stayButton = Gtk.Button(label = "Stay")

        self._textTable = Gtk.Table()
        self._buttonTable.set_homogeneous(False)
        self._buttonTable.resize(8,6)
        self._buttonTable.set_col_spacings(20)
        self._buttonTable.set_row_spacings(5)
        

        self._playerText = Gtk.TextView()
        self._textBuffer = Gtk.TextBuffer()
        self._textBuffer.set_text("Score: 0")
        self._playerText.set_editable(False)

        self._playerText.set_buffer(self._textBuffer)


        self._buttonTable.attach(self._hitButton, 0, 5, 0, 2, Gtk.AttachOptions.FILL, Gtk.AttachOptions.FILL, 0, 0)
        self._buttonTable.attach(self._stayButton, 0, 5, 2, 4, Gtk.AttachOptions.FILL, Gtk.AttachOptions.FILL, 0, 0)

        self._textTable.attach(self._playerText, 0, 6, 4, 6, Gtk.AttachOptions.EXPAND, Gtk.AttachOptions.EXPAND, 0, 0)
        

        self._pCardTable.attach(self._textTable, 0, 2, 6, 7, Gtk.AttachOptions.FILL, Gtk.AttachOptions.FILL, 10, 0)
        self._pCardTable.attach(self._buttonTable, 0, 3, 7, 9, Gtk.AttachOptions.FILL, Gtk.AttachOptions.FILL, 10, 0)

    def add_player_card(self, card, player):
        self._pCard = Gtk.Image()
        self.get_card_image(card)

        self._playerScore = player.score
        if(player.contains_ace and player.score + 10 < 22):
            self._textBuffer.set_text("Score: " + str(self._playerScore) + " or " + str(self._playerScore + 10))
        else:
            self._textBuffer.set_text("Score: " + str(self._playerScore))
             
        self._playerText.set_buffer(self._textBuffer)

        self._pCardTable.attach(self._pCard, self._insertedCards + 4, self._insertedCards + 5, 7, 9, Gtk.AttachOptions.SHRINK, Gtk.AttachOptions.SHRINK, 10, 0)   

        self._insertedCards = self._insertedCards + 1
        self.show_all()


    def get_card_image(self, card):
        
        if(card.suit == 'Spades'):
            filename = "./imgs/" + card.rank + "S.png"
        elif(card.suit == 'Clubs'):
            filename = "./imgs/" + card.rank + "C.png"
        elif(card.suit == 'Hearts'):
            filename = "./imgs/" + card.rank + "H.png"
        else:
            filename = "./imgs/" + card.rank + "D.png"

        pixbuf = GdkPixbuf.Pixbuf.new_from_file(filename)
        pixbuf = pixbuf.scale_simple(80, 150, 2)

        self._pCard.set_from_pixbuf(pixbuf) 

    def create_enemy_hand(self):
        self._eTextTable = Gtk.Table()
        self._eTextTable.set_homogeneous(False)
        self._eTextTable.resize(8,6)
        self._eTextTable.set_col_spacings(20)
        self._eTextTable.set_row_spacings(5)

        self._enemyText = Gtk.TextView()
        self._eTextBuffer = Gtk.TextBuffer()
        self._eTextBuffer.set_text("Score: 0")
        self._enemyText.set_buffer(self._eTextBuffer)
        self._enemyText.set_editable(False)
        
        self._eTextTable.attach(self._enemyText, 0, 6, 4, 6, Gtk.AttachOptions.EXPAND, Gtk.AttachOptions.EXPAND, 0, 0)
        
        self._pCardTable.attach(self._eTextTable, 0, 2, 2, 3, Gtk.AttachOptions.FILL, Gtk.AttachOptions.FILL, 10, 0)   


    def add_enemy_card(self, card, player):
        self._pCard = Gtk.Image()
        self.get_card_image(card)

        self._enemyScore = player.score
        if(player.contains_ace and player.score + 10 < 22):
            self._eTextBuffer.set_text("Score: " + str(self._enemyScore) + " or " + str(self._enemyScore + 10))
        else:
            self._eTextBuffer.set_text("Score: " + str(self._enemyScore))

        self._pCardTable.attach(self._pCard, self._eInsertedCards + 4, self._eInsertedCards + 5, 1, 3, Gtk.AttachOptions.SHRINK, Gtk.AttachOptions.SHRINK, 10, 0)   

        self._eInsertedCards = self._eInsertedCards + 1
        self.show_all()

    def remove_hands(self):
        self.remove(self._pCardTable)
        self._insertedCards = 0
        self._eInsertedCards = 0

    def backwards_card(self):
        self._downCard = Gtk.Image()
        pixbuf = GdkPixbuf.Pixbuf.new_from_file("./imgs/red_back.png")
        pixbuf = pixbuf.scale_simple(80, 150, 2)
        self._downCard.set_from_pixbuf(pixbuf)

        self._pCardTable.attach(self._downCard, 5, 6, 1, 3, Gtk.AttachOptions.SHRINK, Gtk.AttachOptions.SHRINK, 10, 0)   
        self._isCardDown = True

        self.show_all()

    def remove_backwards_card(self, card):
        self._pCardTable.remove(self._downCard)  
        self._pCard = Gtk.Image()
        self.get_card_image(card)
        self._eInsertedCards = self._eInsertedCards + 1
        
        self._pCardTable.attach(self._pCard, 5, 6, 1, 3, Gtk.AttachOptions.SHRINK, Gtk.AttachOptions.SHRINK, 10, 0)   

        self._isCardDown = False
        
        self.show_all()

    
    def end_game_text(self, text):
        self._endText = Gtk.TextView()
        self._endBuffer = Gtk.TextBuffer()
        self._endBuffer.set_text(text)
        self._endText.set_buffer(self._endBuffer)
        self._endText.set_editable(False)

        self._pCardTable.attach(self._endText, 5, 6, 4, 5, Gtk.AttachOptions.SHRINK, Gtk.AttachOptions.SHRINK, 10, 0)   

        self.show_all()


    def play_again_buttons(self):
        self._yesButton = Gtk.Button(label = "Yes")
        self._noButton = Gtk.Button(label = "No")
        
        self._promptTable = Gtk.Table()
        self._promptTable.resize(3, 7)
        self._promptTable.set_col_spacings(20)
        self._promptTable.set_row_spacings(5)

        self._promptTable.attach(self._yesButton, 0, 3, 1, 2, Gtk.AttachOptions.FILL, Gtk.AttachOptions.FILL, 0, 0)   
        self._promptTable.attach(self._noButton, 4, 7, 1, 2, Gtk.AttachOptions.FILL, Gtk.AttachOptions.FILL, 0, 0)   

        self._pCardTable.attach(self._promptTable, 6, 8, 4, 5, Gtk.AttachOptions.FILL, Gtk.AttachOptions.FILL, 10, 0)   

        self.show_all()


    @property
    def screen_size_width(self):
        return self._screen_size_width

    @property
    def screen_size_height(self):
        return self._screen_size_height

    @property
    def bjButton(self):
        return self._bjButton

    @property
    def hitButton(self):
        return self._hitButton

    @property
    def stayButton(self):
        return self._stayButton

    @property
    def yesButton(self):
        return self._yesButton

    @property
    def noButton(self):
        return self._noButton

    @property
    def isCardDown(self):
        return self._isCardDown

    @property
    def startBox(self):
        return self._box

    def connect_button(self, func, button):
        wrapped_func = self.wrap_func(func) 
        button.connect("clicked", wrapped_func)

    def wrap_func(self, func):
        def wrap(button):
            func(button, self)
        return wrap

    def connect_button2(self, func, button, player, opponent, deck):
        wrapped_func = self.wrap_func2(func, player, opponent, deck)
        button.connect("clicked", wrapped_func)
    
    def wrap_func2(self, func, player, opponent, deck):
        def wrap2(button):
            func(button, self, player, opponent, deck)
        return wrap2

    def connect_end_buttons(self, func):
        self.play_again_buttons()
        self._noButton.connect("clicked", Gtk.main_quit)
        wrapped_func = self.wrap_func(func)
        self._yesButton.connect("clicked", wrapped_func)
    
    def disable_button(self, button):
        button.set_sensitive(False)

            

class Card():

    def __init__(self, rank, suit):
        self._rank = rank
        self._suit = suit

    def __repr__(self):
        return str(self._rank) + " of " + str(self._suit)

    @property
    def rank(self):
        return self._rank

    @property
    def suit(self):
        return self._suit
    
    @property
    def score(self):
        if self._rank in '2':
            return 2
        elif self._rank in '3':
            return 3
        elif self._rank in '4':
            return 4
        elif self._rank in '5':
            return 5
        elif self._rank in '6':
            return 6
        elif self._rank in '7':
            return 7
        elif self._rank in '8':
            return 8
        elif self._rank in '9':
            return 9
        elif self._rank in ['10', 'J', 'Q', 'K']:
            return 10
        else:
            return 1
       

class CardDeck():

    ranks = [str(n) for n in range(2, 11)] + list('JQKA')
    suits = 'Clubs Spades Diamonds Hearts'.split()

    def __init__(self):
        self._cards = []
        ordered_cards = [Card(rank, suit) for rank in self.ranks
                                          for suit in self.suits]
        while len(ordered_cards) > 0:
            rand_index = random.randrange(len(ordered_cards))
            rand_card =  ordered_cards.pop(rand_index) 
            self._cards.append(rand_card)

    def __getitem__(self, position):
        return self._cards[position]

    def __len__(self):
        return len(self._cards)

    def __repr__(self):
        return 'CardDeck(%r)' % (len(self._cards))  
    
    def pop(self):
        return self._cards.pop()


class PlayerHand():

    def __init__(self, deck):
        self._hand = []
        self._score = 0
        self._hasAce = False 
        self.deal_hand(deck) 

    def __repr__(self):
        return str(self._hand) 

    def __len__(self):
        return len(self._hand)

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, x):
        self._score = self._score + x 

    @property
    def contains_ace(self):
        return self._hasAce

    @property
    def hand(self):
        return self._hand

    def score_increase(self, x):
        self._score = self._score + x
    
    def deal_hand(self, deck):
        self.draw_card(deck)
        self.draw_card(deck)

    def draw_card(self, deck):
        card = deck.pop()
        self._score += card.score
        if card.rank == 'A':
           self._hasAce = True
        self._hand.append(card)

 
""" Check player score in blackjack terms, returns 0 for under 21, 1 for 21, and 2 for over 21 """
def check_score(player):
    if player.contains_ace and player.score + 10 <= 21:
        if player.score + 10 == 21:
            player.score_increase(10)
            return 1 
        else:
            return 0
    if player.score < 21:
        return 0
    elif player.score == 21:
        return 1
    else:
        return 2



def player_loss(win, player, opponent):
    win.end_game_text("You Lose\nPlay Again?")
    win.connect_end_buttons(play_again)

def player_tie(win, player):
    win.end_game_text("You Tie\nPlay Again?")
    win.connect_end_buttons(play_again)


def player_win(win, player, opponent):
    win.end_game_text("You Win\nPlay Again?")
    win.connect_end_buttons(play_again)


def game_over(win, player, opponent, scenerio):
    disableButtons(win)
    if(win.isCardDown):
        win.remove_backwards_card(opponent.hand[1])
    if scenerio == 0:
        if(player.contains_ace and player.score + 10 <= 21):
            player.score_increase(10)
        if(opponent.contains_ace and opponent.score + 10 <= 21):
            opponent.score_increase(10)
        if opponent.score <= 21:
            if opponent.score < player.score:
                player_win(win, player, opponent)
            elif opponent.score == player.score:
                player_tie(win, player) 
            else:
                player_loss(win, player, opponent)
        else:
            player_win(win, player, opponent)
    elif scenerio == 1:
        if opponent.score == 21:
            player_tie(win, player)
        else:
            player_win(win, player, opponent)
    else:
        player_loss(win, player, opponent)


def dealer_turn(win, player, opponent, deck):
    player_score = player.score
    if(player.contains_ace and player.score + 10 <= 21):
        player_score = player_score + 10
    if (player_score < opponent.score) or (len(opponent) >= MAX_CARD_HAND) or (opponent.score >= 17):
        scenerio = check_score(player)
        game_over(win, player, opponent, scenerio)
    elif opponent.contains_ace and opponent.score + 10 > player_score: 
        scenerio = check_score(player)
        game_over(win, player, opponent, scenerio)
    else: 
        opponent.draw_card(deck) 
        win.add_enemy_card(opponent.hand[len(opponent) - 1], opponent)
        dealer_turn(win, player, opponent, deck)
 

def player_hit(button, win, player, opponent, deck):
    player.draw_card(deck)
    win.add_player_card(player.hand[len(player) - 1], player)
    scenerio = check_score(player)
    if scenerio:
        game_over(win, player, opponent, scenerio)

def player_stayed(button, win, player, opponent, deck):
    disableButtons(win)    
    win.remove_backwards_card(opponent.hand[1])
    dealer_turn(win, player, opponent, deck)

def disableButtons(win):
    win.disable_button(win.hitButton)
    win.disable_button(win.stayButton)

        
def play_bj(button, win):
    win.remove_start_button()
    win.create_player_hand()
    win.create_enemy_hand()

    deck = CardDeck()
    player = PlayerHand(deck)

    win.add_player_card(player.hand[0], player)
    win.add_player_card(player.hand[1], player)
    
    opponent = PlayerHand(deck)

    win.add_enemy_card(opponent.hand[0], opponent)
    win.backwards_card()

    win.connect_button2(player_hit, win.hitButton, player, opponent, deck)
    win.connect_button2(player_stayed, win.stayButton, player, opponent, deck)

    if check_score(player) == 1:
        game_over(win, player, opponent, 1)
    elif check_score(opponent) == 1:
        win.remove_backwards_card(opponent.hand[1])
        player_loss(win, player, opponent)

def play_again(button, win):
    win.remove_hands()
    win.create_start_button()
    win.show_all()
    win.connect_button(play_bj, win.bjButton)


def main():
    win = MyWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    win.connect_button(play_bj, win.bjButton)
    Gtk.main()

    
if __name__ == "__main__":
    main()
