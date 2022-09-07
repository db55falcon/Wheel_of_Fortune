import random
import time
import string
import csv


not_allowed = string.punctuation + string.digits  # characters the user cannot use for guess


class Player:  # create the player class
    def __init__(self, name):
        self.name = name
        self.score = 0  # auto initialize score attribute to zero for every player instance

    def update_score(self, num):  # simple method allowing for score to be updated
        if num >= 0:
            self.score += num
        else:
            self.score = 0


def select_category():  # selects a random category from below files
    categories = ["Elements.txt", "Animals.txt", "Countries.txt"]
    category = random.choice(categories)
    return category


def openfile(filename):  # uses the randomly selected category to generate a list from the category
    with open(filename, "r") as fileObj:
        data = fileObj.read()
        random_list = data.split("\n")  # use the split method to generate a list from string
        return random_list


def player_names():  # creates a list of player instances/objects
    while True:
        try:
            num_of_players = int(input("How many players are there? "))
            list_of_names = input("Enter the player names , separate with comma >>: ").split(",")
            if len(list_of_names) <= 3:
                players_list = []
                for i in range(num_of_players):
                    name = random.choice(list_of_names)
                    players_list.append(Player(name))
                    list_of_names.remove(name)
                return players_list
            else:
                print("Max of three players")
                continue
        except Exception as e:
            print("\n===============================================")
            print(e)
            print("===============================================\n")


def main():  # game begins here
    print("""
$$\      $$\ $$\                           $$\        $$$$$$\   $$$$$$\        $$$$$$$$\                  $$\                                  
$$ | $\  $$ |$$ |                          $$ |      $$  __$$\ $$  __$$\       $$  _____|                 $$ |                                 
$$ |$$$\ $$ |$$$$$$$\   $$$$$$\   $$$$$$\  $$ |      $$ /  $$ |$$ /  \__|      $$ |    $$$$$$\   $$$$$$\$$$$$$\  $$\   $$\ $$$$$$$\   $$$$$$\  
$$ $$ $$\$$ |$$  __$$\ $$  __$$\ $$  __$$\ $$ |      $$ |  $$ |$$$$\           $$$$$\ $$  __$$\ $$  __$$\_$$  _| $$ |  $$ |$$  __$$\ $$  __$$\ 
$$$$  _$$$$ |$$ |  $$ |$$$$$$$$ |$$$$$$$$ |$$ |      $$ |  $$ |$$  _|          $$  __|$$ /  $$ |$$ |  \__|$$ |   $$ |  $$ |$$ |  $$ |$$$$$$$$ |
$$$  / \$$$ |$$ |  $$ |$$   ____|$$   ____|$$ |      $$ |  $$ |$$ |            $$ |   $$ |  $$ |$$ |      $$ |$$\$$ |  $$ |$$ |  $$ |$$   ____|
$$  /   \$$ |$$ |  $$ |\$$$$$$$\ \$$$$$$$\ $$ |       $$$$$$  |$$ |            $$ |   \$$$$$$  |$$ |      \$$$$  \$$$$$$  |$$ |  $$ |\$$$$$$$\ 
\__/     \__|\__|  \__| \_______| \_______|\__|       \______/ \__|            \__|    \______/ \__|       \____/ \______/ \__|  \__| \_______|
                                                                                                                                               
                                                                                                                                               
                                                                                                                                               
""")
    players_list = player_names()
    for i in players_list:  # welcome the players by attribute name
        print(f"welcome {i.name}")
    # below are all the prizes on wheel (-1 represents bankrupt, -2 represents lost turn)
    wheel_spin = [-1, 250, 300, 350, 400, 450, 500, 500, 500, 550, 600, 650, 700, 750, 800, 850, 1000, 5000, -2, 20000]

    category = select_category()  # calling category function
    random_list = openfile(category)  # passing category into openfile function
    game_words = random.sample(random_list, 1)  # generates the 3 words/rounds of the game
    while game_words:  # while words still reside in game_words list loop will run
        word_selection = random.choice(game_words)  # this is the word of the game/round
        print(word_selection)
        word_selection2 = word_selection  # this is for the full guess
        # below is the game word display with _ representing each corresponding character
        display_word = ["_"] * len(word_selection)
        game_words.remove(word_selection)  # this removes word from the games_word list
        if " " in word_selection:  # flipping the empty spaces in a word (like in real wheel of fortune)
            fix_space = word_selection.index(" ")
            display_word[fix_space] = " "
        while "_" in display_word:  # while loop runs until all _ are flipped (word has been successfully guessed)
            for player in players_list:  # for loop allows each player to take a turn
                while "_" in display_word:
                    print(*display_word)  # the * unpacks the list for visual purposes
                    print(f"\n Player: {player.name}")
                    print(f" Bank : ${player.score}")  # represent current player score
                    full_guess = input("would you like to guess the entire word? y/n: ")
                    if full_guess == "y":
                        full_word_guess = input("enter you guess: ")
                        if full_word_guess == word_selection2:
                            print("correct!\n")
                            player.update_score(25000)  # updating player score with full word prize
                            display_word = full_word_guess
                            break
                        else:
                            print("wrong answer!\n")
                            break
                    input("press enter to spin the wheel!")
                    print("spinning..... \u2638")
                    time.sleep(2)
                    spin_value = random.choice(wheel_spin)  # randomly select value from prize wheel
                    if spin_value == -1:
                        print("you went bankrupt!!! \n")
                        player.update_score(spin_value)  # update score accordingly
                        break  # move to next player
                    elif spin_value == -2:
                        print("you lost your turn!!! \n")
                        break  # move to next player
                    else:
                        print(f"You landed on ${spin_value}!!!")

                        while True:
                            global guess  # had to globalize guess to allow for loop break
                            guess = input("please pick a letter : ")
                            if len(guess) < 2:  # word must be less than two or loop continues to prompt player
                                if guess not in not_allowed:
                                    break  # all checks have been met, break next if statement
                            else:
                                print("can only guess one letter")
                        if guess in word_selection:
                            print("correct guess!!!!")
                            # below we flip the word by using for loop and changing the display
                            for index, value in enumerate(word_selection):
                                if guess == value:
                                    player.update_score(spin_value)
                                    display_word[index] = value
                        # below we replace the first instance of the guess to allow flipping the other instances
                                    word_selection.replace(value, "!", 1)
                        else:
                            print("Wrong guess")
                            break  # breaks to next player

    print()
    winner_dict = {}  # here we create a dictionary to calculate player scores and the winner
    for i in players_list:
        print(f"{i.name}'s bank is ${i.score}")
        winner_dict[i.name] = i.score  # appending the dictionary
    max_value = max(winner_dict.values())
    max_name = max(winner_dict, key=winner_dict.get)
    print(f"{max_name} is the winner with ${max_value}")
    print(f"Congrats {max_name} you are the winner! Welcome to the bonus round! \uE312")

    # bonus round begins
    winner_prizes = ["tesla model x", "mercedes benz G class", "lexus ux200", "polaris sling shot", "honda civic"]
    prize = random.choice(winner_prizes)
    with open("bonuswords.csv", "r") as f:  # open bonus round riddles
        reader = csv.reader(f)
        list_of_bonus_riddles = [i for i in reader]  # we must put riddles in list

    riddle = random.choice(list_of_bonus_riddles)  # select riddle (answer at index 0, riddle at index 1)

    print("spinning.... \u2638")
    time.sleep(2)
    print(f"you have landed on a {prize}, you have 3 tries to solve the riddle and win the prize")
    counter = 0
    display = ["_"] * len(riddle[0])
    while counter < 3:
        print(*display)
        question = input(f"{riddle[1]}: ")
        if question == riddle[0]:
            print(f"you have won the {prize} \U0001F697")
            break
        else:
            print("guess again")
            counter += 1


if __name__ == "__main__":
    main()

# art


