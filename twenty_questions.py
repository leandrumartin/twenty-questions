import json
from random import randint, choice


class TwentyQuestions:
    """A class to manage the game."""

    def __init__(self):
        """Initialize game variables."""
        with open('items.json') as f:
            self._items = json.load(f)

        self._stop_guessing = False
        self._turns = 0

        # Initialize which guessable items are possible
        self._possible = []
        for index in range(len(self._items)):
            self._possible.append(index)

        self._correct_item = {}
        self._guess_item = None
        self._guess_key = None
        self._guess_value = None

    def show_rules(self):
        """Prints the rules."""
        lines = ["Here's how to play:",
                 "\tThink of any object or noun at all.",
                 "\tI'm going to ask you yes or no questions about it and try to guess what it is.",
                 "\tAnswer based on whether your noun USUALLY, STEREOTYPICALLY, and SUBSTANTIALLY has that property.",
                 "\n",
                 "\tFor example, a pencil is usually and stereotypically yellow. It has a pink eraser, but it is not ",
                 "\t\tsubstantially pink enough for one to say that it is pink.",
                 "\n",
                 "\tIf you're unsure (such as if you're asked for a color, but the object can be multiple colors and",
                 "\t\thas no one stereotypical color, such as a car, or if the property is not applicable), answer no.",
                 "\n",
                 "\tIf I guess your object, I win!",
                 "\tBut if I ask twenty questions without guessing correctly, you win.",
                 "\n",
                 "\tEnter 'y' to answer yes or 'n' to answer no. Enter 'q' at any time to quit.",
                ]
        for line in lines:
            print(line)

    def play(self, ask_ready):
        """Ask the player if they're ready, and then play.

        ask_ready: Boolean; True if player should be asked if they're ready.
        """
        if ask_ready:
            self._ask_ready()
        self._main_game()

    def _ask_ready(self):
        """Ask the player if they're ready to play, and if so, play."""
        response = input("\nReady for the questions? ")
        if not response.lstrip().lower().startswith('y'):
            print("No worries! Just let me know when you're ready.")
            self._ask_ready()

    def ask_play_again(self):
        """Ask the player if they would like to play again."""
        response = input("\nWould you like to play again? ")
        if response.lstrip().lower().startswith('y'):
            print("Great!")
            # Reset game variables for new game
            self.__init__()
            return True
        else:
            return False

    def _main_game(self):
        """Play the game."""
        self._stop_guessing = False
        self._turns = 0
        while not self._stop_guessing:
            self._game_turn()

    def _game_turn(self):
        """The behavior for one turn of the game."""
        if len(self._possible) == 0:
            self._give_up()
        else:
            self._turns += 1
            self._ask()
            if self._turns == 20:
                self._stop_guessing = True

    def _ask(self):
        """Determines whether to make a guess, then either calls _guess() or asks about a key."""

        # Get the item to have in mind.
        self._guess_item = self._items[choice(self._possible)]

        # Get a list of possible keys to ask about.
        possible_keys = self._get_possible_keys()

        if possible_keys:
            # There are properties or keys we haven't asked about.
            if randint(1, len(self._possible)) == len(self._possible):
                # 1/len(self._possible) chance of making a guess about the object
                self._guess()
            else:
                # Get the property to ask about, and its value for the item we have in mind (self._guess_item)
                self._guess_key = choice(possible_keys)
                self._guess_value = self._guess_item[self._guess_key]

                # Ask about the property we just retrieved.
                answer = input(f"Is it {self._guess_key}? ")
                self._possible = self._process_answer(answer)
        else:
            # There are no properties we haven't asked about yet. We have to make a guess.
            self._guess()

    def _guess(self):
        """Guess what the object is."""
        # Determine whether to use "an" or "a" to refer to the object.
        vowels = ('a', 'e', 'i', 'o', 'u')
        if self._guess_item["name"][0] in vowels:
            article = 'an'
        else:
            article = 'a'

        answer = input(f"Is it {article} {self._guess_item['name']}? ")
        if answer.lstrip().lower().startswith('y'):
            self._win()
        else:
            self._possible.remove(self._items.index(self._guess_item))

    def _get_possible_keys(self):
        """Returns a list of possible keys to ask about."""
        possible_keys = []
        for key in self._guess_item:
            if key not in self._correct_item and not key == 'name':
                # Question has not been asked yet
                possible_keys.append(key)
        return possible_keys

    def _process_answer(self, answer):
        """Process the player's answer to a non-guess question.
        Returns a list of an updated version of self._possible.
        """
        if answer.lstrip().lower().startswith('q'):
            exit()

        check_value = answer.lstrip().lower().startswith('y')
        updated_possible = self._possible[:]

        # Remove as a possibility all objects for which the property doesn't match what the player said the object's
        #   property is.
        for item_index in self._possible:
            if not self._items[item_index][self._guess_key] == check_value:
                updated_possible.remove(item_index)

        # Now we know what the correct value is.
        self._correct_item[self._guess_key] = check_value

        return updated_possible

    def _win(self):
        """Display a message saying the CPU has won."""
        self._stop_guessing = True
        print(f"I won! I guessed what you were thinking of in {self._turns} turns.")

    def _lose(self):
        """Display a message saying the CPU has lost."""
        self._stop_guessing = True
        print("I lost. I couldn't guess what you were thinking of.")

    def _give_up(self):
        """Display a messages saying the CPU knows no objects matching what the player is thinking of, and gives up."""
        self._stop_guessing = True
        print("I give up! I don't know what you're thinking of.")


if __name__ == '__main__':
    print("Welcome to 20 Questions!\n")
    game = TwentyQuestions()
    game.show_rules()
    game.play(True)
    while game.ask_play_again():
        game.play(False)
