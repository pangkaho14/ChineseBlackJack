import random
import time
from decimal import Decimal, InvalidOperation, getcontext

"""
Chinese Blackjack game (1 human player vs 1 computer dealer)
"""

# Deck creation set up
suits = ("Spades", "Hearts", "Clubs", "Diamonds")
ranks = ("Ace", "Two", "Three", "Four", "Five", "Six", "Seven", \
        "Eight", "Nine", "Ten", "Jack", "Queen", "King")
values = {
    "Ace": [1, 11, 10], "Two": 2, "Three": 3, "Four" : 4, "Five" : 5, "Six" : 6, "Seven": 7, \
    "Eight" : 8, "Nine" : 9, "Ten" : 10, "Jack" : 10, "Queen" : 10, "King" : 10
}

# A card class has 3 attributes; rank, suit and value
# The value attribute is assigned based on the values dictionary
class Card():
    
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.value = values[rank]

    def __str__(self):
        return (f"{self.rank} of {self.suit} (Value: {self.value}).")

# A deck class that contains 52 unique card objects
# It has an all cards attribute that holds the 52 card objects
class Deck():

    def __init__(self):

        self.all_cards = []
        
        # For each suit in suit tuple
        for suit in suits:

            # For each rank in rank tuple
            for rank in ranks:

                # Create a card object with its rank and suit
                card = Card(rank, suit)

                # And append it to a deck list of cards
                self.all_cards.append(card)

    # Deck shuffles itself
    def shuffle(self):

        # The list of card objects is shuffled using the random module shuffle method
        # The list is shuffled in place
        random.shuffle(self.all_cards)

# Function takes in a hand (list of cards) and checks for an ace
def check_hand_for_ace(list_of_cards):
    
    # For each card in hand (list of cards)
    for card in list_of_cards:

        # If an ace is found
        if card.rank == "Ace":

            # Return true
            return True

    # Return false by default
    return False

# A player class that has attributes of a name, stack, list of hand objs, and hand values
class Player():

    def __init__(self, name, stack):
        self.name = name
        self.stack = stack
        self.hand = []
        self.hand_value = 0
        self.hand_value_with_ace = 0
        self.final_hand_value = 0

    # Draws a card from the shuffled deck obj
    def hit(self, deck_obj):

        # Pops the last item (top of the deck) off the shuffled deck obj
        drawn_card = deck_obj.all_cards.pop()

        # Append it to player's hand, which is a list
        self.hand.append(drawn_card)

    # Prints the player's current hand to the terminal
    def see_hand(self):

        print()
        print(f"Player {self.name}'s hand holdings are: ")
        print()

        time.sleep(0.5)

        # For each card in player instance's hand
        for card in self.hand:

            # Print out the card
            print(card)
            time.sleep(0.5)

    # Update hand values for the player instance
    def update_hand_values(self):

        # Reset player instance's hand values and check for ace
        self.hand_value = 0
        self.hand_value_with_ace = 0

        # Check if hand has an ace
        if check_hand_for_ace(self.hand):

            # If it does has an ace, check for the number of cards
            # If the number of cards in hand is 2, apply respective ace values (1,11)
            if len(self.hand) == 2:
                
                # For each card in hand
                for card in self.hand:

                    # If the card is an ace
                    if card.rank == "Ace":

                        # Update hand with ace value with the card value of 11
                        self.hand_value_with_ace += card.value[1]

                        # Update hand value with the card value of 1
                        self.hand_value += card.value[0]
                    
                    # Else the card is non-ace
                    else:

                        # Update hand value with the card value which holds ace value as 1
                        self.hand_value += card.value

                        # Update the second value which holds the ace value as 11
                        self.hand_value_with_ace += card.value

            # If the number of cards in hand is 3, apply respective ace values (1,10)
            elif len(self.hand) == 3:

                # For each card in hand
                for card in self.hand:

                    # If the card is an ace
                    if card.rank == "Ace":

                        # Update hand with ace value with the card value of 10
                        self.hand_value_with_ace += card.value[2]

                        # Update hand value with the card value of 1
                        self.hand_value += card.value[0]
                    
                    # Else the card is non-ace
                    else:

                        # Update hand value with the card value which holds ace value as 1
                        self.hand_value += card.value

                        # Update the second value which holds the ace value as 10
                        self.hand_value_with_ace += card.value

            # If the number of cards in hand is 3 or more, apply respective ace values (1)
            elif len(self.hand) > 3:

                # For each card in hand
                for card in self.hand:

                    # If the card is an ace
                    if card.rank == "Ace":

                        # Update hand value with the card value of 1
                        self.hand_value += card.value[0]
                    
                    # Else the card is non-ace
                    else:

                        # Update hand value with the card value which holds ace value as 1
                        self.hand_value += card.value

        # Else there is no ace in hand
        else:

            # For each card in hand
            for card in self.hand:

                # Update hand value with the card's value
                self.hand_value += card.value

    # Method chooses a legal hand (above 15 value) between 2 hand values
    def stand(self):

        hand_values = [self.hand_value, self.hand_value_with_ace]

        # Filters legal hand values and returns a list of legal hands
        # A hand is legal if it is 16 and above but 21 and below
        legal_hands = list(filter(lambda hand_value: 16 <= hand_value <= 21, hand_values))

        # If there is no legal hands:
        if len(legal_hands) == 0:

            # Return false; ask user to continue drawing
            return False

        # Else if there is only 1 legal hand
        elif len(legal_hands) == 1:

            # Set player instance final hand value attribute to be that legal hand value
            self.final_hand_value = legal_hands[0]
            return True

        # Else if there is 2 legal hands
        else:

            # Set instance attribute to have the higher value of the 2
            if legal_hands[0] > legal_hands[1]:

                self.final_hand_value = legal_hands[0]
                return True

            else:

                self.final_hand_value = legal_hands[1]
                return True

    # Allows user to bet an amount, no min, max is all in
    def bet(self, amount):

            # Deduct the bet amount from the user's stack
            self.stack -= amount
        
    # Shows how much user has left in his stack
    def __str__(self):
        return f"Player {self.name} has a total of ${self.stack} dollars remaining."

# Function takes in a list of 2 card objs and check if both have the attribute "rank" of "Ace"
def check_hand_for_aces(list_of_cards):

    # Check through the list of cards
    for card in list_of_cards:
        
        # If a non Ace card is found, break out of for loop and return false
        if card.rank != "Ace":
            break

    # Else if loop completed normally
    else:
        
        # Return true
        return True

    # Return false by default
    return False

# Function takes in a list of card objs and check if there is exactly 3 cards with the "Seven" "rank"
def check_hand_for_777(list_of_cards):

    if len(list_of_cards) == 3:

        # Check through the list of cards
        for card in list_of_cards:
            
            # If a non Seven card is found, break out of for loop and return false
            if card.rank != "Seven":
                break

        # Else if loop completed normally
        else:
            
            # Return true
            return True

        # Return false otherwise
        return False

    # Return false by default
    return False

# Ask user if they want to replay the game or not
def replay():
    
    # Possible options
    yes = ["Y", "YES"]
    no = ["N", "NO"]

    to_play = None

    # Validate user input
    while to_play not in yes or to_play not in no:

        # Asking if user wants to play again
        to_play = input("Do you wish to replay the game? (Y/N) ")

        # If user wants to play the game
        if to_play.upper() in yes:

            # Restart the game
            return True

        # Else quit the game
        elif to_play.upper() in no:

            # Quit the game
            return False

        # Inform user if they entered an invalid option
        else:
            print()
            print("You did not enter a valid option!")
            print()

# Chinese Blackjack game
def main():

    # # Testing purposes
    # ace = Card("Ace", "Diamonds")
    # test_hand = [Card("Ten", "Clubs"), Card("Ten", "Diamonds")]
    # test_hand2 = [Card("Ten", "Hearts"), Card("Nine", "Spades")]

    # Set floating decimal precision to 2
    getcontext().prec = 2

    # Welcome message
    print()
    print("Welcome to Chinese BlackJack! (Ban Luck)")
    print()

    # Game rule message
    print("Game rules:")
    print("1. You will be playing against a single computer dealer player.")
    print("2. The minimum bet per round is $1 and there is no maximum bet.")
    print("3. Wu Long, Ban Luck, Ban Ban and Triple Seven multiplier rules applies.")
    print("4. A card from the dealer is shown to the player.")
    print()

    # Request user name
    name = input("Please enter your name: ")

    stack = None
    # While user input is not a number or if it is outside acceptable range
    while type(stack) != Decimal or stack <= 0:

        stack = input("Please enter a dollar number for your starting stack: ")
        
        # Try to convert user input into a Decimal class
        # Decimal class used to support floating point bets
        try:
            stack = Decimal(stack)

        # If user input is not a number, continue asking for user input
        except InvalidOperation:
            print("Please enter a valid number!")
            continue

        # If user did not input a positive number
        if stack <= 0:
            print("You can't have a negative or zero stack!")
            print()
            continue

    # Create user player and computer dealer Player objects
    user = Player(name, stack)
    computer = Player("Computer dealer", stack)

    game_on = True
    turn = None

    # While game is ongoing, and both players still have a stack
    while game_on and (user.stack > 0 and computer.stack > 0):

        # Player goes first
        turn = "Player"

        # Reconstruct the deck after each round
        new_deck = Deck()

        # Shuffle the deck
        new_deck.shuffle()

        # Empty the player's and computer's hand
        user.hand = []
        computer.hand = []

        print()
        print("Starting a new hand!")
        time.sleep(1)

        print("Dealing cards...")
        time.sleep(1)

        print()
        print(computer)
        time.sleep(1)
        print(user)
        time.sleep(1)

        # Deal 2 cards to the user and computer from deck
        for i in range(2):
            user.hit(new_deck)
            computer.hit(new_deck)

        # If it is player's turn
        while turn == "Player":

            # Ask for user's bet amount and deduct it from his stack
            bet_amt = 0

            # While user input is not a number or if it is outside acceptable range
            while type(bet_amt) != Decimal or bet_amt <= 0 or bet_amt > user.stack:

                bet_amt = input("Please enter a dollar number for your bet: ")
                
                # Try to convert user input into a Decimal class
                # Decimal class used to support floating point bets
                try:
                    bet_amt = Decimal(bet_amt)

                # If user input is not a number, continue asking for user input
                except InvalidOperation:
                    print("Please enter a valid number!")
                    continue

                # If user did not input a positive number
                if bet_amt <= 0:
                    print("You can't bet negative or zero dollars!")
                    continue

                if bet_amt > user.stack:

                    print("You don't have enough chips to bet that amount!")
                    print(f"You currently have ${user.stack} left.")
                    continue

            print(f"You have entered a bet of ${bet_amt}.")
            time.sleep(1)
            user.bet(bet_amt)
            print(f"You have ${user.stack} left.")
            time.sleep(1)

            # Testing
            # user.hand = test_hand
            # computer.hand = test_hand2

            # Show player one card from dealer
            print()
            print(f"The dealer's face up card is {computer.hand[0]}")
            time.sleep(1)

            # Show player hand
            user.see_hand()

            # Check to see if user has Aces
            if check_hand_for_aces(user.hand):

                print()
                print("BAN BAN! (Pocket Rockets)")
                time.sleep(1)

                # If computer also don't have aces, user wins 3x his bet
                if not check_hand_for_aces(computer.hand):

                    print()
                    print("You instantly win 3x your bet, congrats!")
                    time.sleep(1)

                    won_amt = bet_amt * 3

                    print(f"You win ${won_amt}.")
                    time.sleep(1)

                    # Update user stack
                    user.stack = user.stack + bet_amt + won_amt

                    # Update computer dealer stack
                    computer.stack -= won_amt
                    break

                # Else if computer also has aces, it is a draw
                elif check_hand_for_aces(computer.hand):

                    print()
                    print("Unlucky! The dealer also have Aces.")
                    time.sleep(1)
                    computer.see_hand()
                    print("It is a draw!")
                    time.sleep(1)

                    # Update user stack
                    user.stack += bet_amt
                    break
            
            # Else if computer has aces, player lost 3x his bet amount
            elif check_hand_for_aces(computer.hand):

                print()
                print("Unlucky! The dealer has aces!")
                time.sleep(1)
                computer.see_hand()
                print("You lost 3x your bet.")
                time.sleep(1)

                lost_amt = bet_amt * 3

                print(f"You lost ${lost_amt}.")
                time.sleep(1)

                # Update user stack
                user.stack = user.stack + bet_amt - lost_amt

                # Update computer dealer stack
                computer.stack += lost_amt
                break

            # Player instance method update hand value instance attributes
            user.update_hand_values()
            computer.update_hand_values()

            # If user has a Ban Luck
            if user.hand_value_with_ace == 21:

                print("Ban luck!")
                time.sleep(1)

                # If computer also has a ban luck
                if computer.hand_value_with_ace == 21:

                    print("Unlucky! The dealer also have Ban Luck.")
                    time.sleep(1)
                    computer.see_hand()
                    print("It is a draw!")
                    time.sleep(1)

                    # Update user stack
                    user.stack += bet_amt
                    break

                # Else computer don't have a ban luck
                else:

                    print()
                    print("You win 2x your bet, congrats!")
                    time.sleep(1)

                    won_amt = bet_amt * 2

                    print(f"You win ${won_amt}.")
                    time.sleep(1)

                    # Update user stack
                    user.stack = user.stack + bet_amt + won_amt

                    # Update computer dealer stack
                    computer.stack -= won_amt
                    break

            # Else if user don't have a ban luck
            else:
                
                # If computer has ban luck
                if computer.hand_value_with_ace == 21:

                    print("Unlucky! The dealer have Ban Luck!")
                    time.sleep(1)
                    computer.see_hand()

                    print("You lost 2x your bet.")
                    time.sleep(1)

                    lost_amt = bet_amt * 2

                    print(f"You lost ${lost_amt}.")
                    time.sleep(1)

                    # Update user stack
                    user.stack = user.stack + bet_amt - lost_amt

                    # Update computer dealer stack
                    computer.stack += lost_amt
                    break
                
                # Else both players don't have ban luck, it is a normal hand
                else:

                    # If no ace is encountered
                    if not check_hand_for_ace(user.hand):

                        # Print to the user his hand value
                        time.sleep(1)
                        print()
                        print(f"Your hand has a value of {user.hand_value}.")
                        print()

                    # Else ace is encountered
                    else:

                        # Print both possible values to the user
                        time.sleep(1)
                        print()
                        print(f"Your hand has an Ace, with either a value of {user.hand_value} \
or {user.hand_value_with_ace}.")
                        print()

            # While user's hand is not busted
            while user.hand_value <= 21:

                # After hitting and if user has a hand value of 21, end his turn
                if user.hand_value == 21:

                    user.stand()
                    turn = "Computer"
                    break

                # Ask the user if the user wants to hit or to stand
                action = input("Hit or stand?: ")
                
                # Clean user input
                action = action.lower()

                # Validate user input
                if action not in ["hit", "stand", "h", "s"]:
                    print("""Sorry I don't understand!, Please enter either "hit" or "stand".""")
                    continue

                # Else if the user wants to draw a card
                elif action in ["hit", "h"]:

                    # Player instance method appends a card obj to player instance's hand (list)
                    user.hit(new_deck)

                    # Testing
                    # test_card = Card("Six", "Spades")
                    # user.hand.append(test_card)

                    # Print the drawn card
                    time.sleep(1)
                    print()
                    print("Your drawn card is: ")
                    time.sleep(1)
                    print(f"{user.hand[-1]}")
                    time.sleep(1)
                    user.see_hand()

                    # Checking for 777 instant victory condition
                    if check_hand_for_777(user.hand):

                        print()
                        print("SEVEN SEVEN SEVEN")
                        time.sleep(1)
                        print("7 7 7!")
                        time.sleep(1)
                        print()
                        print("Super lucky! You win 7x your bet, congrats!")
                        time.sleep(1)

                        won_amt = bet_amt * 7

                        print(f"You win ${won_amt}.")
                        time.sleep(1)

                        # Update user stack
                        user.stack = user.stack + bet_amt + won_amt

                        # Update computer dealer stack
                        computer.stack -= won_amt

                        # Reset game
                        turn = None
                        break

                    # Player method updates instance attributes that holds hand values
                    user.update_hand_values()

                    # If no ace is encountered in the hand
                    if not check_hand_for_ace(user.hand):

                        # Print to the user his hand value
                        time.sleep(1)
                        print()
                        print(f"Your hand has a value of {user.hand_value}.")
                        print()

                    # Else if an ace is encountered
                    else:

                        if len(user.hand) > 3:

                            # Print to the user his hand value
                            time.sleep(1)
                            print()
                            print(f"Your hand has a value of {user.hand_value}.")
                            print()

                        else:

                            # Print both possible values to the user
                            time.sleep(1)
                            print()
                            print(f"Your hand has an Ace, with either a value of {user.hand_value} \
or {user.hand_value_with_ace}.")
                            print()

                    # If user has a busted Wu Long
                    if len(user.hand) == 5 and user.hand_value > 21:

                        time.sleep(1)
                        print("Busted Wu Long!")
                        time.sleep(1)
                        print("Unlucky, you lost 2x your bet.")
                        time.sleep(1)

                        lost_amt = bet_amt * 2

                        # Update user stack
                        user.stack = user.stack + bet_amt - lost_amt

                        # Update computer dealer stack
                        computer.stack += lost_amt

                        # Reset hand
                        turn = None
                        break

                    # If user has a Wu Long
                    elif len(user.hand) == 5 and user.hand_value <= 21:

                        time.sleep(1)
                        print("Wu Long!")
                        time.sleep(1)
                        print("You win 2x your bet, congrats!")
                        time.sleep(1)

                        won_amt = bet_amt * 2

                        print(f"You win ${won_amt}.")

                        # Update user stack
                        user.stack = user.stack + bet_amt + won_amt

                        # Update computer dealer stack
                        computer.stack -= won_amt

                        # Reset hand
                        turn = None
                        break

                    # Else if user hand is busted
                    elif user.hand_value > 21:

                        time.sleep(1)
                        print("Your hand value exceeds 21. Your hand is busted!")
                        time.sleep(1)

                        user.final_hand_value = user.hand_value

                        turn = "Computer"
                        break

                elif action in ["stand", "s"]:

                    # If user tries to stand a hand that is not legal in value
                    # Inform user
                    # Ask user for action again
                    if not user.stand():

                        # Go through loop and ask user to hit and draw
                        time.sleep(1)
                        print("You don't have a hand value that is legal!")
                        time.sleep(1)
                        print("The minimum point to stand is 16.")
                        time.sleep(1)
                        print("Please hit and draw until your hand is legal.")
                        continue

                    else:

                        time.sleep(1)
                        print(f"Your hand's value is {user.final_hand_value}.")
                        time.sleep(1)

                        # Change turn to user
                        turn = "Computer"
                        break

        # While it is computer's turn
        while turn == "Computer":

            print()
            time.sleep(1)
            print("It is the computer dealer's turn!")

            # while dealer's hand is not legal, draw till legal
            while not computer.stand():

                computer.hit(new_deck)
                time.sleep(1)
                print("Computer dealer draws...")
                computer.update_hand_values()

                # If hand busts, set attribute and exit loop
                if computer.hand_value > 21:

                    computer.final_hand_value = computer.hand_value
                    break

                # If computer dealer has a Wu Long hand, set attribute and exit loop
                if len(computer.hand) == 5:

                    # This covers the corner case where the computer has a Wu Long hand
                    # But fails to have a legal hand
                    computer.final_hand_value = computer.hand_value
                    break

            # testing
            # computer.hand = test_hand2
            # computer.update_hand_values()
            # computer.stand()

            print()
            time.sleep(1)
            print("Showdown!")
            time.sleep(1)
            computer.see_hand()
            time.sleep(1)
            print(f"The computer dealer's hand value is {computer.final_hand_value}.")
            time.sleep(1)

            # Checking for 777 instant victory conditions
            if check_hand_for_777(computer.hand):

                print()
                print("SEVEN SEVEN SEVEN")
                time.sleep(1)
                print("7 7 7!")
                time.sleep(1)
                print("The dealer has 777")
                print()
                print("Super unlucky! You lost 7x your bet.")
                time.sleep(1)

                lost_amt = bet_amt * 7

                print(f"You lost ${lost_amt}.")
                time.sleep(1)

                # Update user stack
                user.stack = user.stack + bet_amt - lost_amt

                # Update computer dealer stack
                computer.stack += lost_amt

                # Reset game
                turn = None
                break

            # Check for computer's Wu Long victory and lose conditions
            if len(computer.hand) == 5:

                # If computer has a busted Wu Long
                if computer.hand_value > 21:

                    time.sleep(1)
                    print("Busted Wu Long!")
                    time.sleep(1)
                    print("Lucky! You win 2x your bet.")
                    time.sleep(1)

                    won_amt = bet_amt * 2

                    print(f"You win ${won_amt}.")

                    # Update user stack
                    user.stack = user.stack + bet_amt + won_amt

                    # Update computer dealer stack
                    computer.stack -= won_amt

                    # Reset hand
                    turn = None
                    break

                # Else if the dealer has a valid Wu Long
                else:

                    print("The dealer has Wu Long!")
                    time.sleep(1)
                    print("Unlucky, you lost 2x your bet.")
                    time.sleep(1)

                    lost_amt = bet_amt * 2

                    print(f"You lost ${lost_amt}.")

                    # Update user stack
                    user.stack = user.stack + bet_amt - lost_amt

                    # Update computer dealer stack
                    computer.stack += lost_amt

                    # Reset hand
                    turn = None
                    break

            # If the computer's hand busts
            if computer.final_hand_value > 21:

                print("The computer's hand is busted!")
                time.sleep(1)

                user.see_hand()
                print(f"Your hand value is {user.final_hand_value}.")
                time.sleep(1)

                # If the user's hand also busts
                if user.final_hand_value > 21:

                    print("Your hand is also busted!")
                    time.sleep(1)
                    print("It is a draw.")

                    # Reset stack
                    user.stack += bet_amt

                    # Reset game
                    turn = None
                    break

                # Else if the user's hand is legal
                else:

                    print("You win the hand!")
                    time.sleep(1)

                    print(f"You win ${bet_amt}.")

                    # Update stack
                    user.stack += bet_amt + bet_amt
                    computer.stack -= bet_amt

                    # Reset game
                    turn = None
                    break

            # Else the computer's hand is not busted
            else:

                user.see_hand()
                print(f"Your hand value is {user.final_hand_value}.")
                time.sleep(1)

                # If the user's hand busts
                if user.final_hand_value > 21:

                    print("Your hand is busted!")
                    time.sleep(1)
                    print("You lost the hand.")
                    time.sleep(1)
                    print(f"You lost ${bet_amt}.")

                    # Update stacks
                    computer.stack += bet_amt

                    # Reset game
                    turn = None
                    break

                # Else if the user's hand is also not busted
                else:

                    # Compare hand values
                    # If user wins
                    if user.final_hand_value > computer.final_hand_value:

                        print("You win the hand!")
                        time.sleep(1)

                        print(f"You win ${bet_amt}.")
                        time.sleep(1)

                        # Update stack
                        user.stack += bet_amt + bet_amt
                        computer.stack -= bet_amt

                        # Reset game
                        turn = None
                        break

                    # Else if user loses
                    elif user.final_hand_value < computer.final_hand_value:

                        print("You lost the hand.")
                        time.sleep(1)

                        print(f"You lost ${bet_amt}.")
                        time.sleep(1)

                        # Update stack
                        computer.stack += bet_amt

                        # Reset game
                        turn = None
                        break

                    # Else if both final hand values are equal
                    else:

                        print("It is a draw!")
                        time.sleep(1)

                        # Update stack
                        user.stack += bet_amt

                        # Reset game
                        turn = None
                        break

        # If user lost all of his money
        if user.stack <= 0:

            print(user)
            time.sleep(1)
            print("You have lost all of your stack!")
            time.sleep(1)

            # If user wants to play the game again, re-run the program
            if replay():
                main()

            else:
                game_on = False
                print("Thank you for playing!")
                break

        # If computer lost all of his money
        if computer.stack <= 0:

            print(computer)
            time.sleep(1)
            print("The computer dealer has lost all of his stack!")
            time.sleep(1)
            print("Congratulations, you win the game.")
            time.sleep(1)

            # If user wants to play the game again, re-run the program
            if replay():
                main()

            else:
                game_on = False
                print("Thank you for playing!")
                break

# If this module is run under Python interpreter, __name__ is set '__main__' by the Python interpreter.
# tldr: If this script is ran from this script, call the main function
if __name__ == "__main__":
    main()
