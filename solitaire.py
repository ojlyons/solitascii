from enum import Enum
from typing import List
import random

# Even suits are red
# Odd suits are black
class Suit(Enum):
    SPADE = 1   # black
    HEART = 2   #red
    CLUB = 3    # black
    DIAMOND = 4 # red

class Color(Enum):
    RED = 0
    BLACK = 1

class InvalidMoveError(Exception):
    pass

class Card:
    def __init__(self, 
                 number: int, 
                 suit: Suit, 
                 hidden: bool=False):
        self.number = number
        self.suit = suit
        self.hidden = hidden
        self.color = Color.RED if suit.value % 2 == 0 else Color.BLACK

    def __str__(self):
        if (self.hidden):
            return '############'
        return self.getNumberDisplay() + ' of ' + Suit(self.suit).name
    
    def reveal(self):
        self.hidden = False

    def hide(self):
        self.hidden = True

    def getNumberDisplay(self):
        if self.number == 1:
            return 'A'
        elif self.number == 11:
            return 'J'
        elif self.number == 12:
            return 'Q'
        elif self.number == 13:
            return 'K'
        return str(self.number)

    # Requirements: 
    # Self is not hidden
    # Opposite colors
    # Self's number must be Other's number, plus one
    def isValidBaseFor(self, other):
        return not self.hidden and self.color != other.color and self.number == (other.number + 1)
    
class Stack:
    def __init__(self, cards:List[Card] = []):
        self.cards: List[Card] = cards

    def addCards(self, stack: List[Card]):
        self.cards.extend(stack)

class Foundation(Stack):
    def __init__(self, suit: Suit, cards: List[Card] = []):
        super().__init__(cards)
        self.suit = suit

    def peekTopNumber(self):
        if (len(self.cards) == 0):
            return 0
        else:
            return self.cards[-1].number

    def addCard(self, card: Card):
        if card and card.suit == self.suit and (self.peekTopNumber() + 1) == card.number:
            self.addCards([card])

    def takeTopCard(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        return None 
    
class Column(Stack):
    def addStack(self, stack: List[Card]):
        valid = False

        if len(self.cards) == 0 and len(stack) > 0 and stack[0].number == 13:
            valid = True
        elif len(stack) >= 1 and self.cards[-1].isValidBaseFor(stack[0]):
            valid = True
        else:
            valid = False
            raise InvalidMoveError('Cannot place stack')
        if valid:
            self.cards.extend(stack)

    # stackBase: index of the first thing to remove. Everything after the given index will also be taken.
    def takeStack(self, stackBase: int):
        # todo: validate it can be taken.
        # stackBase must be a valid index of the column, and the card there must be already revealed.
        if stackBase >= 0 and len(self.cards) > stackBase and not self.cards[stackBase].hidden:
            # pops the end elemets from the column
            taken = self.cards[stackBase:]
            del self.cards[stackBase:]

            return taken
        else:
            raise InvalidMoveError('Cannot take stack')

    def revealTopCard(self):
        if len(self.cards) > 0:
            self.cards[-1].reveal()


class Table:
    def __init__(self, 
                 columns: List[Column], 
                 foundation: List[Column], 
                 deck: List[Card], 
                 maximumColumns: int=7):
        self.columns = columns
        self.foundation = foundation
        self.deck = deck
        self.maximumColumns = maximumColumns
        self.hand = []

    @staticmethod
    def printCards(cards: List[Card]):
        print([str(card) for card in cards])       
 
    def moveStackBetweenColumns(self, fromColumnIndex: int, toColumnIndex: int, cardIndex: int):
        self.moveStackIntoHand(fromColumnIndex, cardIndex)
        if (self.hand):
            try:
                self.addHandToColumn(toColumnIndex)
                self.columns[fromColumnIndex].revealTopCard()
            except InvalidMoveError as e:
                print(e.args[0])
                self.columns[fromColumnIndex].addCards(self.hand)
            finally:
                self.hand = []
        
    def moveStackIntoHand(self, fromColumnIndex, cardIndex):
        try:
            self.hand = self.columns[fromColumnIndex].takeStack(cardIndex)
        except InvalidMoveError as e:
            print(e.args[0])

    def addHandToColumn(self, toColumnIndex):
        self.columns[toColumnIndex].addStack(self.hand)

    def draw(self):
        if len(self.deck) > 0:
            self.deck[-1].reveal()

def generateDeck() -> List[Card]:
    deck = []

    for suit in Suit:
        for number in range(1, 14):
            deck.append(Card(number, suit))

    random.shuffle(deck)

    return deck

def dealTable(deck: List[Card]) -> Table:
    columns = []

# 0 1 2 3 4 5 6
# x 1 2 3 4 5 6
# x x 2 3 4 5 6
# x x x 3 4 5 6 

    for column in range(7):
        columns.append(Column([]))
        for row in range(column, 7):
            draw = deck.pop()
            if row != 6:
                draw.hidden = True
            columns[column].cards.append(draw)

    for card in deck:
        card.hide()        
    
    return Table(columns, [], deck)

def revealTable(table: Table):
    for i, column in enumerate(table.columns):
        print(i)
        Table.printCards(column.cards)
    print('...')
    Table.printCards(table.deck)
 
def main():
    print('Welcome to SOLITASCII :D')
    print('Type `quit` to end the program.')
    print('Example input: `1 4 3` will take from col 1 all cards after and including the 3rd and move them to col 4.')
    print('Drawing from the deck is not yet supported.')
    print('Moving cards to the foundation is not yet supported.')
    print('Hints are not yet supported.')
    deck = generateDeck()
    table: Table = dealTable(deck)
    revealTable(table)

    move = None

    while move is not 'quit':
        move = input('Your move? ')
        if move == 'quit':
            continue
        elif move == 'draw':
            table.draw()
        elif move:
            parts = move.split(' ')
            table.moveStackBetweenColumns(int(parts[0]), int(parts[1]), int(parts[2]))
        revealTable(table)
        

    #table.moveStackBetweenColumns(0, 6, 6)

    #print('================================')

    #revealTable(table)

main()
