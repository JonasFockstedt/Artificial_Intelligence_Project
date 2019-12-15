__author__ = 'fyt'

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

cardRanks = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14}
possibleHands = {}

class pokerGames(object):
    def __init__(self):
        self.PlayerName = POKER_CLIENT_NAME
        self.Chips = 0
        self.CurrentHand = []
        self.Ante = 0
        self.playersCurrentBet = 0
        self.handStrength = 0
        self.handRank = ''


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
            strength+=cardRanks[card[0]]
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
                print('********STRAIGHT FLUSH!!!!********') # Assign value to agents hand rank.
                self.handRank = 'Straight flush'
            else:
                print('********STRAIGHT!!!!********')
                self.handRank = 'Straight'                  # Assign value to agents hand rank.
        
    
    def checkFlush(self):
        '''
        Check whether the agent has a flush.
        '''
        if self.CurrentHand[0][1] == self.CurrentHand[1][1] == self.CurrentHand[2][1] == self.CurrentHand[3][1] == self.CurrentHand[4][1]:
            print('********FLUSH!!!!********')
            self.handRank = 'Flush'                         # Assign value to agents hand rank.


    def checkPairs(self):
        '''
        Checks whether the agent has one pair, two pairs, three of a kind, four of a kind or full house.
        '''
        rankOccurences = {}
        numberOfPairs = 1
        twoPairs = False                                        # To check if agent has two pairs.
        threePairs = False                                      # To check if agent has three pairs.
        self.handRank = ''                                      # Reset hand rank.

        # card[0] corresponds to rank of first card.
        for card in self.CurrentHand:
            if card[0] in rankOccurences:
                rankOccurences[card[0]]+=1                      # Increase number of occurences.
            else:
                rankOccurences[card[0]] = 1                     # If first occurence.


        listOfDict = list(rankOccurences.items())               # Convert the dictionary to a list.
        for occurence in listOfDict:
            if occurence[1] > numberOfPairs:
                numberOfPairs = occurence[1]


        # Revisit this at some point.
            for rank in listOfDict:
                # Index 1 corresponds to the number of occurences of a given card.
                if rank[1] == 2:                                # If a rank has occured two times.
                    twoPairs = True
                elif rank[1] == 3:                              # If a rank has occured three times.
                    threePairs = True
            
            
        if threePairs and twoPairs:
            print('********FULL HOUSE!!!!********')
            self.handRank == 'Full house.'                      # Assign value to agents hand rank.
        elif twoPairs:
            print('Two pairs!!!')
            self.handRank = 'Two pairs'                         # Assign value to agents hand rank.
        # Check if one pair.
        if numberOfPairs == 2:
            self.handRank = 'One Pair'                          # Assign value to agents hand rank.
        # Check if two pairs.
        elif numberOfPairs == 3:
            self.handRank = 'Three of a kind'                   # Assign value to agents hand rank.
        elif numberOfPairs == 4:
            self.handRank = 'Four of a kind'                    # Assign value to agents hand rank.
        
            

        print('Number of occurences:')
        print(rankOccurences)
        

    def queryPlayerName(self,_name):
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
        playersCurrentBet - the amount of chips the player has already put into the pot (dure to the forced bet).\n
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

        # If hand is too weak, check.
        if self.handStrength <= 10:
            return ClientBase.BettingAnswer.ACTION_CHECK
    
        # Random Open Action
        def chooseOpenOrCheck():
            if _playersCurrentBet + _playersRemainingChips > _minimumPotAfterOpen:
                #return ClientBase.BettingAnswer.ACTION_OPEN,  iOpenBet
                return ClientBase.BettingAnswer.ACTION_OPEN,  (random.randint(0, 10) + _minimumPotAfterOpen) if _playersCurrentBet + _playersRemainingChips + 10> _minimumPotAfterOpen else _minimumPotAfterOpen
            else:
                return ClientBase.BettingAnswer.ACTION_CHECK

        return {
            0: ClientBase.BettingAnswer.ACTION_CHECK,
            1: ClientBase.BettingAnswer.ACTION_ALLIN,
        }.get(random.randint(0, 2), chooseOpenOrCheck())

    
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
        self.calculateHand()
        # Random Open Action
        def chooseRaiseOrFold(self):
            if  _playersCurrentBet + _playersRemainingChips > _minimumAmountToRaiseTo:
                return ClientBase.BettingAnswer.ACTION_RAISE,  (random.randint(0, 10) + _minimumAmountToRaiseTo) if _playersCurrentBet+ _playersRemainingChips + 10 > _minimumAmountToRaiseTo else _minimumAmountToRaiseTo
            else:
                return ClientBase.BettingAnswer.ACTION_FOLD
        return {
            0: ClientBase.BettingAnswer.ACTION_FOLD,
            1: ClientBase.BettingAnswer.ACTION_ALLIN,
            2: ClientBase.BettingAnswer.ACTION_CALL if _playersCurrentBet + _playersRemainingChips > _maximumBet else ClientBase.BettingAnswer.ACTION_FOLD
        }.get(random.randint(0, 3), chooseRaiseOrFold(self))

    
    def queryCardsToThrow(self, _hand):
        '''
        Modify queryCardsToThrow() and add your strategy to throw cards
        Called during the draw phase of the game when the player is offered to throw away some
        (possibly all) of the cards on hand in exchange for new.
        return - An array of the cards on hand that should be thrown away in exchange for new, or 
        <code>null</code> or an empty array to keep all cards.\n
        @see     #infoCardsInHand(ca.ualberta.cs.poker.Hand)
        '''
        print("Requested information about what cards to throw")
        print(_hand)
        return _hand[random.randint(0,4)] + ' '

    # InfoFunction:

    
    def infoNewRound(self, _round):
        '''
        Called when a new round begins.\n
        round - the round number (increased for each new round).
        '''
        #_nrTimeRaised = 0
        print('Starting Round: ' + _round )

        
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
        print("Player "+ _playerName +" made a forced bet of "+ _forcedBet + " chips.")


    
    def infoPlayerOpen(self, _playerName, _openBet):
        '''
        Called when a player opens a betting round.\n
        playerName - the name of the player that opens.\n
        openBet - the amount of chips the player has put into the pot.
        '''
        print("Player "+ _playerName + " opened, has put "+ _openBet +" chips into the pot.")

    
    def infoPlayerCheck(self, _playerName):
        '''
        Called when a player checks.\n
        playerName - the name of the player that checks.
        '''
        print("Player "+ _playerName +" checked.")

    
    def infoPlayerRise(self, _playerName, _amountRaisedTo):
        '''
        Called when a player raises.\n
        playerName - the name of the player that raises.\n
        amountRaisedTo - the amount of chips the player raised to.
        '''
        print("Player "+_playerName +" raised to "+ _amountRaisedTo+ " chips.")

    
    def infoPlayerCall(self, _playerName):
        '''
        Called when a player calls.\n
        playerName - the name of the player that calls.
        '''
        print("Player "+_playerName +" called.")

    
    def infoPlayerFold(self, _playerName):
        '''
        Called when a player folds.\n
        playerName - the name of the player that folds.
        '''
        print("Player "+ _playerName +" folded.")

    
    def infoPlayerAllIn(self, _playerName, _allInChipCount):
        '''
        Called when a player goes all-in.\n
        playerName - the name of the player that goes all-in.\n
        allInChipCount - the amount of chips the player has in the pot and goes all-in with.
        '''
        print("Player "+_playerName +" goes all-in with a pot of "+_allInChipCount+" chips.")

    
    def infoPlayerDraw(self, _playerName, _cardCount):
        '''
        Called when a player has exchanged (thrown away and drawn new) cards.\n
        playerName - the name of the player that has exchanged cards.\n
        cardCount - the number of cards exchanged.
        '''
        print("Player "+ _playerName + " exchanged "+ _cardCount +" cards.")

    
    def infoPlayerHand(self, _playerName, _hand):
        '''
        Called during the showdown when a player shows his hand.\n
        playerName - the name of the player whose hand is shown.\n
        hand - the players hand.
        '''
        self.sortHand()
        #self.CurrentHand.sort()
        #self.CurrentHand.sort(key=self.returnSuit)
        print("Player "+ _playerName +" hand " + str(_hand))

    
    def infoRoundUndisputedWin(self, _playerName, _winAmount):
        '''
        Called during the showdown when a players undisputed win is reported.\n
        playerName - the name of the player whose undisputed win is anounced.\n
        winAmount - the amount of chips the player won.
        '''
        print("Player "+ _playerName +" won "+ _winAmount +" chips undisputed.")

    
    def infoRoundResult(self, _playerName, _winAmount):
        '''
        Called during the showdown when a players win is reported. If a player does not win anything,
        this method is not called.\n
        playerName - the name of the player whose win is anounced.\n
        winAmount - the amount of chips the player won.
        '''
        print("Player "+ _playerName +" won " + _winAmount + " chips.")

