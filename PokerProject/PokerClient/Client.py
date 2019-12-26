__author__ = 'Jonas Fockstedt, Ema Krcic'

import socket
import random
from collections import Counter

import ClientBase

# IP address and port
TCP_IP = '127.0.0.1'
TCP_PORT = 5000
BUFFER_SIZE = 1024

# Agent
POKER_CLIENT_NAME = 'Agent16'
CURRENT_HAND = []

cardRanks = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7,
             "8": 8, "9": 9, "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
handRanks = {"High cards": 0, "One pair": 1, "Two pairs": 2, "Three of a kind": 3, "Straight": 4,
             "Flush": 5, "Full house": 6, "Four of a kind": 7, "Straight flush": 8}


class pokerGames(object):
    def __init__(self):
        self.PlayerName = POKER_CLIENT_NAME
        self.Chips = 0
        self.CurrentHand = []
        self.Ante = 0
        self.playersCurrentBet = 0
        self.handStrength = 0
        self.handRank = ''
        self.importantCards = []

    def returnSuit(self, card):
        '''
        Specifically called when the hand needs to be sorted after suits.
        '''
        return card[1]

    def sortHand(self):
        '''
        Sorts hand in ascending order, based on both rank and suit.
        '''
        self.CurrentHand.sort()
        # Sorts cards in alphabetical suit order.
        self.CurrentHand.sort(key=self.returnSuit)

    def calculateHand(self):
        strength = 0

        self.checkPairs()
        self.checkStraight()
        # print('Rank order of first two cards:')
        # print(self.CurrentHand[0][0], self.CurrentHand[1][0])
        if self.handRank == '':
            self.handRank = 'High cards'

        print('Hand rank of agent:')
        print(self.handRank)

        for card in self.CurrentHand:
            strength += cardRanks[card[0]]
        self.handStrength = strength

        print('Strength of hand is: ' + str(self.handStrength))

    def checkStraight(self):
        '''
        Checks whether the agent has a straight or straight flush.
        '''
        self.checkFlush()
        # Check if hand is a flush, then determine if it is a straight flush, or regular flush.
        if cardRanks[self.CurrentHand[0][0]]+1 == cardRanks[self.CurrentHand[1][0]] and cardRanks[self.CurrentHand[1][0]]+1 == cardRanks[self.CurrentHand[2][0]] \
                and cardRanks[self.CurrentHand[2][0]]+1 == cardRanks[self.CurrentHand[3][0]] and cardRanks[self.CurrentHand[3][0]]+1 == cardRanks[self.CurrentHand[4][0]]:
            if self.handRank == 'Flush':
                # Assign value to agents hand rank.
                print('********STRAIGHT FLUSH!!!!********')
                self.handRank = 'Straight flush'
            else:
                print('********STRAIGHT!!!!********')
                # Assign value to agents hand rank.
                self.handRank = 'Straight'

    def checkFlush(self):
        '''
        Check whether the agent has a flush.
        '''
        if self.CurrentHand[0][1] == self.CurrentHand[1][1] == self.CurrentHand[2][1] == self.CurrentHand[3][1] == self.CurrentHand[4][1]:
            print('********FLUSH!!!!********')
            # Assign value to agents hand rank.
            self.handRank = 'Flush'

    def checkPairs(self):
        '''
        Checks whether the agent has one pair, two pairs, three of a kind, four of a kind or full house.
        '''
        rankOccurences = {}
        numberOfPairs = 1
        # To check if agent has two pairs.
        twoPairs = False
        # To check if agent has three pairs.
        threePairs = False
        # Reset hand rank.
        self.handRank = ''

        # card[0] corresponds to rank of first card.
        for card in self.CurrentHand:
            if card[0] in rankOccurences:
                # Increase number of occurences.
                rankOccurences[card[0]] += 1
            else:
                # If first occurence.
                rankOccurences[card[0]] = 1

        # Convert the dictionary to a list.
        listOfDict = list(rankOccurences.items())
        for occurence in listOfDict:
            # occurence[1] corresponds to the value from the dictionary.
            if occurence[1] > numberOfPairs:
                numberOfPairs = occurence[1]

        # Revisit this at some point.
            for rank in listOfDict:
                # Index 1 corresponds to the number of occurences of a given card.
                # If a rank has occured two times.
                if rank[1] == 2:
                    twoPairs = True
                # If a rank has occured three times.
                elif rank[1] == 3:
                    threePairs = True

        if threePairs and twoPairs:
            print('********FULL HOUSE!!!!********')
            # Assign value to agents hand rank.
            self.handRank == 'Full house'
        elif twoPairs and not numberOfPairs == 2:
            print('Two pairs!!!')
            # Assign value to agents hand rank.
            self.handRank = 'Two pairs'
        # Check if one pair.
        elif numberOfPairs == 2:
            # Assign value to agents hand rank.
            self.handRank = 'One pair'
        # Check if two pairs.
        elif numberOfPairs == 3:
            # Assign value to agents hand rank.
            self.handRank = 'Three of a kind'
        elif numberOfPairs == 4:
            # Assign value to agents hand rank.
            self.handRank = 'Four of a kind'

        print('Number of occurences:')
        print(rankOccurences)

    def checkImportantCards(self):
        '''
        If an agent has any number of pairs, this function is used to determine which cards can not be thrown away.
        '''
        # Reset important cards.
        self.importantCards = []

        for card in self.CurrentHand:
            for secondCard in self.CurrentHand[self.CurrentHand.index(card)+1::]:
                if card[0] == secondCard[0]:
                    self.importantCards.append(card)
                    self.importantCards.append(secondCard)

        print('IMPORTANT CARDS: ', self.importantCards)

    def checkForNearbyStraight(self, direction):
        '''
        Determine if last or first card in hand needs to be thrown.\n
        direction - a string determining which direction to search. "forwards" and "backwards" are the two options.
        '''
        closeToStraight = True
        self.CurrentHand.sort()

        if direction == 'forwards':
            # Iterate through the hand, and keep a counter with enumerate(). Not iterating through last two elements in hand.
            for index, card in enumerate(self.CurrentHand[:-2]):
                # Check if next card is NOT in ascending order of current card.
                if str(cardRanks[card[0]]+1) is not self.CurrentHand[index+1][0]:
                    closeToStraight = False
                    break

        elif direction == 'backwards':
            # Iterate through the hand, and keep a counter with enumerate(). Not iterating through first 3 elements in hand.
            for index, card in enumerate(reversed(self.CurrentHand[-3:])):
                # Check if "previous" card is NOT in descending order of current card.
                if str(cardRanks[card[0]]-1) is not self.CurrentHand[len(self.CurrentHand) - 2 - index][0]:
                    closeToStraight = False
                    break

        self.sortHand()
        return closeToStraight

    def checkForNearbyFlush(self, direction):
        '''
        Determine if last or first card in hand needs to be thrown.\n
        direction - a string determining which direction to search. "forwards" and "backwards" are the two options.
        '''
        closeToFlush = True

        if direction == 'forwards':
            # Iterate through the hand, and keep a counter with enumerate(). Not iterating through last two elements in hand.
            for index, card in enumerate(self.CurrentHand[:-2]):
                # Check if next card is NOT of same suit.
                if card[1] is not self.CurrentHand[index+1][1]:
                    closeToFlush = False
                    break

        elif direction == 'backwards':
            # Iterate through the hand, and keep a counter with enumerate(). Not iterating through first 3 elements in hand.
            for index, card in enumerate(reversed(self.CurrentHand[-3:])):
                # Check if "previus" card is NOT of same suit.
                if card[1] is not self.CurrentHand[len(self.CurrentHand) - 2 - index][1]:
                    closeToFlush = False
                    break

        return closeToFlush

    def queryPlayerName(self, _name):
        '''
        Gets the name of the player.\n
        return - The name of the player as a single word without space. <code>null</code> is not a valid answer.
        '''
        if _name is None:
            _name = POKER_CLIENT_NAME
        return _name

    def queryOpenAction(self, _minimumPotAfterOpen, _playersCurrentBet, _playersRemainingChips):
        '''
        Modify queryOpenAction() and add your strategy here\n
        Called during the betting phases of the game when the player needs to decide what open
        action to choose.\n
        minimumPotAfterOpen - the total minimum amount of chips to put into the pot if the answer action is
        {@link BettingAnswer#ACTION_OPEN}.\n
        playersCurrentBet - the amount of chips the player has already put into the pot (due to the forced bet).\n
        playersRemainingChips - the number of chips the player has not yet put into the pot.\n
        return - An answer to the open query. The answer action must be one of {@link BettingAnswer#ACTION_OPEN}, 
        {@link BettingAnswer#ACTION_ALLIN} or {@link BettingAnswer#ACTION_CHECK }. 
        If the action is open, the answers amount of chips in the anser must be between 
        <code>minimumPotAfterOpen</code> and the players total amount of chips (the amount of chips alrady put into
        pot plus the remaining amount of chips).
        '''
        print("Player requested to choose an opening action.")

        self.sortHand()
        self.calculateHand()

        def chooseOpenOrCheck(self):
            if _playersCurrentBet + _playersRemainingChips > _minimumPotAfterOpen:

                # Go all-in if agent has a straight flush
                if self.handRank == 'Straight flush':
                    return ClientBase.BettingAnswer.ACTION_OPEN, ClientBase.BettingAnswer.ACTION_ALLIN

                elif self.handRank == 'Four of a kind':
                    return ClientBase.BettingAnswer.ACTION_OPEN, int(_playersRemainingChips/2) + _minimumPotAfterOpen

                elif self.handRank == 'Full house':
                    return ClientBase.BettingAnswer.ACTION_OPEN, int(_playersRemainingChips/3) + _minimumPotAfterOpen

                elif self.handRank == 'Flush':
                    return ClientBase.BettingAnswer.ACTION_OPEN, int(_playersRemainingChips/4) + _minimumPotAfterOpen

                elif self.handRank == 'Straight':
                    return ClientBase.BettingAnswer.ACTION_OPEN, int(_playersRemainingChips/5) + _minimumPotAfterOpen

                elif self.handRank == 'Three of a kind':
                    return ClientBase.BettingAnswer.ACTION_OPEN, int(_playersRemainingChips/6) + _minimumPotAfterOpen

                elif self.handRank == 'Two pairs':
                    return ClientBase.BettingAnswer.ACTION_OPEN, int(_playersRemainingChips/7) + _minimumPotAfterOpen

                elif self.handRank == 'One pair':
                    return ClientBase.BettingAnswer.ACTION_OPEN, _minimumPotAfterOpen

                elif self.handRank == 'High cards':
                    # If close to straight.
                    if self.checkForNearbyStraight('forwards') or self.checkForNearbyStraight('backwards'):
                        return ClientBase.BettingAnswer.ACTION_OPEN, _minimumPotAfterOpen + 10 + _minimumPotAfterOpen
                    elif self.checkForNearbyFlush('forwards') or self.checkForNearbyFlush('backwards'):
                        return ClientBase.BettingAnswer.ACTION_OPEN, _minimumPotAfterOpen + _playersRemainingChips/3 + _minimumPotAfterOpen
                    # If hand is too weak, fold.
                    elif self.handStrength <= 10:
                        return ClientBase.BettingAnswer.ACTION_CHECK
                    # Else-statement for cases not covered by previous if-statements.
                    else:
                        return ClientBase.BettingAnswer.ACTION_CHECK

                # return ClientBase.BettingAnswer.ACTION_OPEN,  iOpenBet
                # return ClientBase.BettingAnswer.ACTION_OPEN,  (random.randint(0, 10) + _minimumPotAfterOpen) if _playersCurrentBet + _playersRemainingChips + 10 > _minimumPotAfterOpen else _minimumPotAfterOpen
            else:
                return ClientBase.BettingAnswer.ACTION_CHECK

        return chooseOpenOrCheck(self)
        # return {
        #     0: ClientBase.BettingAnswer.ACTION_CHECK,
        #     1: ClientBase.BettingAnswer.ACTION_ALLIN,
        # }.get(random.randint(0, 2), chooseOpenOrCheck())

    def queryCallRaiseAction(self, _maximumBet, _minimumAmountToRaiseTo, _playersCurrentBet, _playersRemainingChips):
        '''
        Modify queryCallRaiseAction() and add your strategy here.\n
        Called during the betting phases of the game when the player needs to decide what call/raise
        action to choose.\n
        maximumBet - the maximum number of chips one player has already put into the pot.\n
        minimumAmountToRaiseTo - the minimum amount of chips to bet if the returned answer is {@link BettingAnswer#ACTION_RAISE}.\n
        playersCurrentBet - the number of chips the player has already put into the pot.\n
        playersRemainingChips - the number of chips the player has not yet put into the pot.\n
        return - An answer to the call or raise query. The answer action must be one of
        {@link BettingAnswer#ACTION_FOLD}, {@link BettingAnswer#ACTION_CALL},
        {@link BettingAnswer#ACTION_RAISE} or {@link BettingAnswer#ACTION_ALLIN}.
        If the players number of remaining chips is less than the maximum bet and
        the players current bet, the call action is not available. If the players
        number of remaining chips plus the players current bet is less than the minimum
        amount of chips to raise to, the raise action is not available. If the action
        is raise, the answers amount of chips is the total amount of chips the player
        puts into the pot and must be between <code>minimumAmountToRaiseTo</code> and
        <code>playersCurrentBet+playersRemainingChips</code>.
        '''
        print("Player requested to choose a call/raise action.")
        self.sortHand()
        self.calculateHand()

        def chooseRaiseOrFold(self):
            # Check if agent can afford to join the next round.
            if _playersCurrentBet + _playersRemainingChips > _minimumAmountToRaiseTo:
                # Go all-in if agent has a straight flush
                if self.handRank == 'Straight flush':
                    return ClientBase.BettingAnswer.ACTION_RAISE, ClientBase.BettingAnswer.ACTION_ALLIN

                elif self.handRank == 'Four of a kind':
                    return ClientBase.BettingAnswer.ACTION_RAISE, int(_playersRemainingChips/2) + _minimumAmountToRaiseTo

                elif self.handRank == 'Full house':
                    return ClientBase.BettingAnswer.ACTION_RAISE, int(_playersRemainingChips/3) + _minimumAmountToRaiseTo

                elif self.handRank == 'Flush':
                    return ClientBase.BettingAnswer.ACTION_RAISE, int(_playersRemainingChips/4) + _minimumAmountToRaiseTo

                elif self.handRank == 'Straight':
                    return ClientBase.BettingAnswer.ACTION_RAISE, int(_playersRemainingChips/5) + _minimumAmountToRaiseTo

                elif self.handRank == 'Three of a kind':
                    return ClientBase.BettingAnswer.ACTION_RAISE, int(_playersRemainingChips/6) + _minimumAmountToRaiseTo

                elif self.handRank == 'Two pairs':
                    return ClientBase.BettingAnswer.ACTION_RAISE, int(_playersRemainingChips/7) + _minimumAmountToRaiseTo

                elif self.handRank == 'One pair':
                    return ClientBase.BettingAnswer.ACTION_RAISE, _minimumAmountToRaiseTo

                elif self.handRank == 'High cards':
                    # If close to straight.
                    if self.checkForNearbyStraight('forwards') or self.checkForNearbyStraight('backwards'):
                        return ClientBase.BettingAnswer.ACTION_RAISE, _minimumAmountToRaiseTo + 10
                    elif self.checkForNearbyFlush('forwards') or self.checkForNearbyFlush('backwards'):
                        return ClientBase.BettingAnswer.ACTION_RAISE, _minimumAmountToRaiseTo + _playersRemainingChips/2
                    # If hand is too weak, fold.
                    elif self.handStrength <= 10:
                        return ClientBase.BettingAnswer.ACTION_FOLD
                    # Else-statement to handle cases not covered.
                    else:
                        return ClientBase.BettingAnswer.ACTION_FOLD
                # return ClientBase.BettingAnswer.ACTION_RAISE,  (random.randint(0, 10) + _minimumAmountToRaiseTo) if _playersCurrentBet + _playersRemainingChips + 10 > _minimumAmountToRaiseTo else _minimumAmountToRaiseTo
            elif self.CurrentHand == 'Straight flush' or 'Four of a kind' and _playersCurrentBet + _playersRemainingChips > _minimumAmountToRaiseTo:
                return ClientBase.BettingAnswer.ACTION_CALL
            else:
                return ClientBase.BettingAnswer.ACTION_FOLD

        return chooseRaiseOrFold(self)
        # return {
        #     0: ClientBase.BettingAnswer.ACTION_FOLD,
        #     1: ClientBase.BettingAnswer.ACTION_ALLIN,
        #     2: ClientBase.BettingAnswer.ACTION_CALL if _playersCurrentBet + _playersRemainingChips > _maximumBet else ClientBase.BettingAnswer.ACTION_FOLD
        # }.get(random.randint(0, 3), chooseRaiseOrFold(self))

    def queryCardsToThrow(self, _hand):
        '''
        Modify queryCardsToThrow() and add your strategy to throw cards\n
        Called during the draw phase of the game when the player is offered to throw away some
        (possibly all) of the cards on hand in exchange for new.\n
        return - An array of the cards on hand that should be thrown away in exchange for new, or 
        <code>null</code> or an empty array to keep all cards.\n
        @see     #infoCardsInHand(ca.ualberta.cs.poker.Hand)
        '''
        cardsToThrow = []
        print("Requested information about what cards to throw")
        print(_hand)
        self.checkImportantCards()
        if self.handRank == 'High cards':
            # Check if last card needs to be thrown in order to get a straight.
            if self.checkForNearbyStraight('backwards'):
                print('First card has to be thrown away')
                return ''.join(self.CurrentHand[0])
            # Check if first card needs to be thrown in order to get a straight.
            elif self.checkForNearbyStraight('forwards'):
                print('Last card has to be thrown away')
                return ''.join(self.CurrentHand[4])
            # Throws whole hand if strength of cards is too weak.
            elif self.handStrength <= 10:
                print('THROWING WHOLE HAND')
                return ' '.join(_hand)
        # If agent has some kind of pairs, throw the other cards.
        elif self.handRank == 'One pair' or 'Two pairs' or 'Three of a kind' or 'Four of a kind':
            for card in self.CurrentHand:
                if card not in self.importantCards:
                    cardsToThrow.append(card)
            # Joins list elements and separates them with a space since the server demands this format.
            return ' '.join(cardsToThrow)

        # Do not throw anything since Straight, Flush, Full house and Straight flush are considered good hands.
        elif self.handRank == 'Straight' or 'Flush' or 'Full house' or 'Straight flush':
            return ' '

        return _hand[random.randint(0, 4)] + ' '

    # InfoFunction:

    def infoNewRound(self, _round):
        '''
        Called when a new round begins.\n
        round - the round number (increased for each new round).
        '''
        #_nrTimeRaised = 0
        print('Starting Round: ' + _round)

    def infoGameOver(self):
        '''
        Called when the poker server informs that the game is completed.
        '''
        print('The game is over.')

    def infoPlayerChips(self, _playerName, _chips):
        '''
        Called when the server informs the players how many chips a player has.\n
        playerName - the name of a player.\n
        chips - the amount of chips the player has.
        '''
        print('The player ' + _playerName + ' has ' + _chips + 'chips')

    def infoAnteChanged(self, _ante):
        '''
        Called when the ante has changed.\n
        ante - the new value of the ante.
        '''
        print('The ante is: ' + _ante)

    def infoForcedBet(self, _playerName, _forcedBet):
        '''
        Called when a player had to do a forced bet (putting the ante in the pot).\n
        playerName - the name of the player forced to do the bet.\n
        forcedBet - the number of chips forced to bet.
        '''
        print("Player " + _playerName +
              " made a forced bet of " + _forcedBet + " chips.")

    def infoPlayerOpen(self, _playerName, _openBet):
        '''
        Called when a player opens a betting round.\n
        playerName - the name of the player that opens.\n
        openBet - the amount of chips the player has put into the pot.
        '''
        print("Player " + _playerName + " opened, has put " +
              _openBet + " chips into the pot.")

    def infoPlayerCheck(self, _playerName):
        '''
        Called when a player checks.\n
        playerName - the name of the player that checks.
        '''
        print("Player " + _playerName + " checked.")

    def infoPlayerRise(self, _playerName, _amountRaisedTo):
        '''
        Called when a player raises.\n
        playerName - the name of the player that raises.\n
        amountRaisedTo - the amount of chips the player raised to.
        '''
        print("Player "+_playerName + " raised to " +
              _amountRaisedTo + " chips.")

    def infoPlayerCall(self, _playerName):
        '''
        Called when a player calls.\n
        playerName - the name of the player that calls.
        '''
        print("Player "+_playerName + " called.")

    def infoPlayerFold(self, _playerName):
        '''
        Called when a player folds.\n
        playerName - the name of the player that folds.
        '''
        print("Player " + _playerName + " folded.")

    def infoPlayerAllIn(self, _playerName, _allInChipCount):
        '''
        Called when a player goes all-in.\n
        playerName - the name of the player that goes all-in.\n
        allInChipCount - the amount of chips the player has in the pot and goes all-in with.
        '''
        print("Player "+_playerName + " goes all-in with a pot of " +
              _allInChipCount+" chips.")

    def infoPlayerDraw(self, _playerName, _cardCount):
        '''
        Called when a player has exchanged (thrown away and drawn new) cards.\n
        playerName - the name of the player that has exchanged cards.\n
        cardCount - the number of cards exchanged.
        '''
        print("Player " + _playerName + " exchanged " + _cardCount + " cards.")

    def infoPlayerHand(self, _playerName, _hand):
        '''
        Called during the showdown when a player shows his hand.\n
        playerName - the name of the player whose hand is shown.\n
        hand - the players hand.
        '''
        self.sortHand()
        # self.CurrentHand.sort()
        # self.CurrentHand.sort(key=self.returnSuit)
        print("Player " + _playerName + " hand " + str(_hand))

    def infoRoundUndisputedWin(self, _playerName, _winAmount):
        '''
        Called during the showdown when a players undisputed win is reported.\n
        playerName - the name of the player whose undisputed win is anounced.\n
        winAmount - the amount of chips the player won.
        '''
        print("Player " + _playerName + " won " +
              _winAmount + " chips undisputed.")

    def infoRoundResult(self, _playerName, _winAmount):
        '''
        Called during the showdown when a players win is reported. If a player does not win anything,
        this method is not called.\n
        playerName - the name of the player whose win is anounced.\n
        winAmount - the amount of chips the player won.
        '''
        print("Player " + _playerName + " won " + _winAmount + " chips.")
