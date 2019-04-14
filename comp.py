'''
This file contains the functions for the computer players
'''

import uno

cardValues={'num':1, 'special':20, 'wild':50}

'''
This function controls the color choices of the computer
'''
def color(hand):
    rC=0
    bC=0
    gC=0
    yC=0
    for card in hand:
        if card[0]=='r': rC+=1
        if card[0]=='b': bC+=1
        if card[0]=='g': gC+=1
        if card[0]=='y': yC+=1
    if max(rC, bC, gC, yC)==rC:return 'r'
    if max(rC, bC, gC, yC)==bC:return 'b'
    if max(rC, bC, gC, yC)==gC:return 'g'
    if max(rC, bC, gC, yC)==yC:return 'y'


'''
this function counts frequency of colors
'''
def colFreq(val):
    for card in val:
        for card2 in val:
            if card[0] == card2[0]:
                val[card]+=1

'''
This function counts the frequency of numbers
'''
def numFreq(val):
    for card in val:
        for card2 in val:
            if card[1:] == card2[1:]:
                if card != '+4' and card2 != '+4':
                    val[card]+=1
                elif card != '+4' and card2 != '+4':
                    val[card]+=1


'''
this function adds card type value
'''
def cardVal(val, turn):
    for card in val:
        if card[0] in ['r', 'b', 'g', 'y'] and card[1:] in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            val[card]=int(val[card]*(turn/cardValues['num']))
            if val[card]==0: val[card]=1
        elif card[0] in ['r', 'b', 'g', 'y'] and card[1:] in ['reverse', 'skip', '+2']:
            val[card]=int(val[card]*(turn/cardValues['special']))
            if val[card]==0: val[card]=1
        elif card[:] in ['wild', '+4']:
            val[card]=int(val[card]*(turn/cardValues['special']))
            if val[card]==0: val[card]=1

'''
this function will choose the card to play
'''
def cardChoice(hand, discard, c, turn):
    valid = {}
    for card in hand:
        if uno.valid(card, discard, c):
           valid.update({card:0})
    colFreq(valid)
    numFreq(valid)
    cardVal(valid, turn)
    max=0
    maxC = ''
    for card in valid:
        if valid[card]>max:
            max=valid[card]
            maxC = card
    return maxC