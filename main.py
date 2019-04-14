import random
import uno
import comp
import time

color={'r':'red', 'b':'blue', 'g':'green', 'y':'yellow'}

'''
This function returns a shuffled deck
'''
def shuffle(cards):
    deck=[]
    while sum(cards.values()) > 0:
        temp = random.choice(list(cards.keys()))
        if cards[temp] > 0:
            deck.append(temp)
            cards[temp]-=1
    return deck

'''
This function initializes the deck of cards
'''
def initCards():
    return {'r0':1, 'r1':2, 'r2':2, 'r3':2, 'r4':2, 'r5':2, 'r6':2, 'r7':2, 'r8':2, 'r9':2, 'r+2':2, 'rskip':2, 'rreverse':2
        , 'b0':1, 'b1':2, 'b2':2, 'b3':2, 'b4':2, 'b5':2, 'b6':2, 'b7':2, 'b8':2, 'b9':2, 'b+2':2, 'bskip':2, 'breverse':2
        , 'g0':1, 'g1':2, 'g2':2, 'g3':2, 'g4':2, 'g5':2, 'g6':2, 'g7':2, 'g8':2, 'g9':2, 'g+2':2, 'gskip':2, 'greverse':2
        , 'y0':1, 'y1':2, 'y2':2, 'y3':2, 'y4':2, 'y5':2, 'y6':2, 'y7':2, 'y8':2, 'y9':2, 'y+2':2, 'yskip':2, 'yreverse':2
        , 'wild':4, '+4':4}

'''
This function runs a player vs. computer game
'''
def pvc(playerNum):
    #set up game
    cards = initCards()
    deck=shuffle(cards)
    hand = []
    for i in range(playerNum):
        temp=[]
        while len(temp) < 7:
            temp.append(uno.draw(deck))
        hand.append(temp)
    discard=[uno.draw(deck)]

    #handle first card being wild
    if discard[-1] == 'wild' or discard[-1] == '+4':
        v=False
        while v==False:
            c=input('first card is wild, enter the desired color(r, b, g, or y)')
            if c=='r' or c=='b' or c=='g' or c=='y':
                v=True
            else: print('That is not a valid color')
    else: c=discard[-1][0]

    first=True
    special=False
    player = 0
    turn=0
    reverse=False

    while True:
        print()

        #handle special cards and player switch
        if first==False:
            if reverse==False:
                player+=1
                if player == playerNum:
                    player=0
            else:
                player-=1
                if player < 0:
                    player=playerNum-1

            if special==False:

                #handle reverse
                if discard[-1][1:]=='reverse':
                    print('reversing')
                    special=True
                    if reverse==False:
                        reverse=True
                        player-=2
                        if player<0:
                            player=playerNum+player
                    elif reverse==True:
                        reverse=False
                        player+=2
                        if player>=playerNum:
                            player=0+(player-playerNum)
                    if player == 0: print('player', player+1)
                    else: print('computer', player)

                if player==0:
                    print('player', player+1)
                else:
                    print('computer', player)

                #handle +2
                if discard[-1][1:]=='+2':
                    print('drawing 2 and skipping')
                    for i in range(2):
                        hand[player].append(uno.draw(deck))
                    special=True
                    continue

                #handle +4
                if discard[-1]=='+4':
                    print('drawing 4 and skipping')
                    for i in range(4):
                        hand[player].append(uno.draw(deck))
                    special=True
                    continue

                #handle skipping
                if discard[-1][1:]=='skip':
                    print('skipping')
                    special=True
                    continue
        first=False
        if player==0:
            print('card counts:')
            for i in range(playerNum):
                if i == 0:
                    print('player', i+1, ':', len(hand[i]))
                else:
                    print('computer', i, ':', len(hand[i]))
            print('your hand is:', hand[player])
            print('the top card is', discard[-1], 'color is', color[c])
            #checks move availability
            if uno.checkMoves(hand[player], discard[-1], c) == True:
                #when moves are available
                v=False
                while v==False:
                    card=input('which card do you want to play')
                    if card in hand[player] and uno.valid(card, discard[-1], c): v=True
                    else: print(card, 'is not a valid card')
                hand[player].remove(card)
                discard.append(card)
            else:
                #when player must draw
                while uno.checkMoves(hand[player], discard[-1], c) == False:
                    if len(deck)==0:
                        deck = discard[:-1]
                        discard = [discard[-1]]
                        random.shuffle(deck)
                    print('no valid moves, drawing.')
                    hand[player].append(uno.draw(deck))
                print('your hand is:', hand[player])
                print('the top card is', discard[-1], 'color is', color[c])
                v=False
                while v==False:
                    card=input('which card do you want to play')
                    if card in hand[player] and uno.valid(card, discard[-1], c): v=True
                    else: print(card, 'is not a valid card')
                hand[player].remove(card)
                discard.append(card)
            if len(hand[player])==0: break
            if discard[-1]=='wild' or discard[-1]=='+4':
                v=False
                while v==False:
                    c=input('what is your desired color(r, b, g, or y)')
                    if c=='r' or c=='b' or c=='g' or c=='y':
                        v=True
                    else: print('That is not a valid color')
            else: c=discard[-1][0]
            special=False

        #computer turn
        else:
            print('the top card is', discard[-1], 'color is', color[c])
            if uno.checkMoves(hand[player], discard[-1], c) == True:
                card=comp.cardChoice(hand[player], discard[-1], c, turn)
                print('Computer', player, 'plays', card)
                hand[player].remove(card)
                discard.append(card)
            else:
                #when player must draw
                while uno.checkMoves(hand[player], discard[-1], c) == False:
                    if len(deck)==0:
                        deck = discard[:-1]
                        discard = [discard[-1]]
                        random.shuffle(deck)
                    print('no valid moves, drawing.')
                    hand[player].append(uno.draw(deck))
                #play valid card if gotten from drawing
                for i in range(len(hand[player])):
                    if uno.valid(hand[player][i], discard[-1], c):
                        card=hand[player][i]
                        print('Computer', player, 'plays', card)
                        hand[player].remove(card)
                        discard.append(card)
                        break
            if len(hand[player])==0: break
            if discard[-1]=='wild' or discard[-1]=='+4':
               c=comp.color(hand[player])
               print('computer', player, 'chooses', c)
            else: c=discard[-1][0]
            special=False
            time.sleep(2)
        turn+=1
    if player == 0:
        print('player', player+1, 'wins!')
    else:
        print('computer', player, 'wins!')


'''
This function runs a player vs. player game
'''
def pvp(playerNum):
    #set up game
    cards = initCards()
    deck=shuffle(cards)
    hand = []
    for i in range(playerNum):
        temp=[]
        while len(temp) < 7:
            temp.append(uno.draw(deck))
        hand.append(temp)
    discard=[uno.draw(deck)]

    #handle first card being wild
    if discard[-1] == 'wild' or discard[-1] == '+4':
        v=False
        while v==False:
            c=input('first card is wild, enter the desired color(r, b, g, or y)')
            if c=='r' or c=='b' or c=='g' or c=='y':
                v=True
            else: print('That is not a valid color')
    else: c=discard[-1][0]

    first=True
    special=False
    player = 0
    reverse=False

    print('player', player+1)
    while True:
        print()
        #handle special cards and player switch
        if first==False:
            print('switching players')
            if reverse==False:
                player+=1
                if player == playerNum:
                    player=0
            else:
                player-=1
                if player < 0:
                    player=playerNum-1
            print('player', player+1)
            if special==False:

                #handle reverse
                if discard[-1][1:]=='reverse':
                    print('reversing')
                    special=True
                    if reverse==False:
                        reverse=True
                        player-=2
                        if player<0:
                            player=playerNum+player
                    elif reverse==True:
                        reverse=False
                        player+=2
                        if player>=playerNum:
                            player=0+(player-playerNum)
                    print('player is now', player+1)

                #handle +2
                if discard[-1][1:]=='+2':
                    print('drawing 2 and skipping')
                    for i in range(2):
                        hand[player].append(uno.draw(deck))
                    special=True
                    continue

                #handle +4
                if discard[-1]=='+4':
                    print('drawing 4 and skipping')
                    for i in range(4):
                        hand[player].append(uno.draw(deck))
                    special=True
                    continue

                #handle skipping
                if discard[-1][1:]=='skip':
                    print('skipping')
                    special=True
                    continue

        first=False

        print('your hand is:', hand[player])
        print('the top card is', discard[-1], 'color is', color[c])
        if uno.checkMoves(hand[player], discard[-1], c) == True:
            #when moves are available
            v=False
            while v==False:
                card=input('which card do you want to play')
                if card in hand[player] and uno.valid(card, discard[-1], c): v=True
                else: print(card, 'is not a valid card')
            hand[player].remove(card)
            discard.append(card)
        else:
            #when player must draw
            while uno.checkMoves(hand[player], discard[-1], c) == False:
                if len(deck)==0:
                    deck = discard[:-1]
                    discard = [discard[-1]]
                    random.shuffle(deck)
                print('no valid moves, drawing.')
                hand[player].append(uno.draw(deck))
            print('your hand is:', hand[player])
            print('the top card is', discard[-1], 'color is', color[c])
            v=False
            while v==False:
                card=input('which card do you want to play')
                if card in hand[player] and uno.valid(card, discard[-1], c): v=True
                else: print(card, 'is not a valid card')
            hand[player].remove(card)
            discard.append(card)
        if len(hand[player])==0: break
        if discard[-1]=='wild' or discard[-1]=='+4':
            v=False
            while v==False:
                c=input('what is your desired color(r, b, g, or y)')
                if c=='r' or c=='b' or c=='g' or c=='y':
                    v=True
                else: print('That is not a valid color')
        else: c=discard[-1][0]
        special=False

    for i in range(playerNum):
        if len(hand[i])==0: print('Player', i+1, 'wins!')

#gather input for gamemode and player count
v = False
while v==False:
    game=input('select game mode (pvp or pvc)')
    if game=='pvp' or game=='pvc': v=True
    else: print('That\'s not a valid game mode')

v=False
while v==False:
    playerNum=input('How many players(max of 6)')
    try:
        int(playerNum)
    except:
        print('That is not a valid input')
        continue
    if 2 < int(playerNum) < 7: v=True
    else: print('That is not a valid number of players')

if game=='pvp': pvp(int(playerNum))
if game=='pvc': pvc(int(playerNum))