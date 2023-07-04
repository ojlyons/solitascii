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
        self.color = Color.RED if suit % 2 == 0 else Color.BLACK

    def __str__(self):
        return ('~' if self.hidden else '') + str(self.number) + ' of ' + Suit(self.suit).name
    
    def reveal(self):
        self.hidden = False

    def hide(self):
        self.hidden = True

    # Requirements: 
    # Self is not hidden
    # Opposite colors
    # Self's number must be Other's number, plus one
    def isValidBaseFor(self, other):
        return not self.hidden and self.color != other.color and self.number == (other.number + 1)
    
class Column:
    def __init__(self, 
                 cards: List[Card] = []):
        self.cards: List[Card] = cards

    def addStack(self, stack: List[Card]):
        if len(stack) >= 1 and self.cards[-1].isValidBaseFor(stack[0]):
            self.cards.extend(stack)
        else:
            raise InvalidMoveError('Cannot place stack')

    # stackBase: index of the first thing to remove. Everything after the given index will also be taken.
    def takeStack(self, stackBase: int):
        # todo: validate it can be taken.
        # stackBase must be a valid index of the column, and the card there must be already revealed.
        if stackBase >= 0 and len(self.cards) > stackBase and not self.cards[stackBase].hidden:
            # pops the end elemets from the column
            taken = self.cards[stackBase:]
            del self.cards[stackBase:]

            # reveal the top card
            self.cards[-1].reveal()

            return taken
        else:
            raise InvalidMoveError('Cannot take stack')

    # In case a move is invalid and needs to be undone.    
    def replaceStack(self, stack: List[Card]):
        self.cards.extend(stack)


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

    def printCards(cards: List[Card]):
        print([str(card) for card in cards])       
 
    def moveStackBetweenColumns(self, fromColumnIndex: int, toColumnIndex: int, cardIndex: int):
        self.moveStackIntoHand(fromColumnIndex, cardIndex)
        if (self.hand):
            try:
                self.addHandToColumn(toColumnIndex)
            except InvalidMoveError as e:
                print(e.args[0])
                self.columns[fromColumnIndex].replaceStack(self.hand)
                self.hand = []
        
    def moveStackIntoHand(self, fromColumnIndex, cardIndex):
        try:
            self.hand = self.columns[fromColumnIndex].takeStack(cardIndex)
        except InvalidMoveError as e:
            print(e.args[0])

    def addHandToColumn(self, toColumnIndex):
        self.columns[toColumnIndex].addStack(self.hand)

def generateDeck():
    deck = []

    for suit in range(1, 5):
        for number in range(1, 14):
            deck.append(Card(number, suit))

    random.shuffle(deck)

    return deck

def dealTable(deck: List[Card]):
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
            
    return Table(columns, [], deck)

def revealTable(table: Table):
    for column in table.columns:
        Table.printCards(column.cards)
    print('...')
    Table.printCards(table.deck)
 
    


def main():
    print('hi :)')
    deck = generateDeck()
    table: Table = dealTable(deck)
    revealTable(table)

    #table.columns[-1].addStack(table.columns[0].takeStack(1))
    table.moveStackBetweenColumns(0, 6, 6)

    print('================================')

    revealTable(table)

main()
