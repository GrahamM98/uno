'''
this file provides the functions determining the actions in the game
'''

'''
this function draws a card
'''
def draw(deck):
    return deck.pop()

'''
This function checks if a move is valid
'''
def valid(card, discard, c):
    if card=='wild' or card=='+4':
        return True
    if card[0] == c or card[1:] == discard[1:]:
        if card != '+4' and discard == '+4' and card[0] != c:
            return False
        return True
'''
this function determines if a move is valid
'''
def checkMoves(hand, discard, c):
    for card in hand:
        if valid(card, discard, c):
            return True
    return False