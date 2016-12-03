"""Pokemon Capture Simulator

Simulate pokemon capture, base level module

"""

from random import randint, choice
from time import sleep
import json
from src.image import draw_ascii
from src.pokemon_names import GEN_ONE

# Not all pokemon have catch rates, as they all cannot be caught in the wild.
with open('src/pokemon.json') as open_file:
    CATCH_RATE = json.load(open_file)


def get_ball_val(ball):
    """Pokeball random value

    Gets the Pokeball random value N for the Pokeball type

    Args:
        ball: String of the pokeball type

    Returns:
        Integer value from 0 to 255, 0 to 150 if the Pokeball is incorrect
    """
    return {
        'poke': randint(0, 255),
        'great': randint(0, 200),
        'master': 255
    }.get(ball, randint(0, 150))


class Ailment(object):
    """The Ailment of a Pokemon

    Randomly generates values for Pokemon condition

    Attributes:
        ailment: string effect on the Pokemon
        catch_thresh: capture threshold integer value
    """

    def __init__(self):
        status_roll = randint(0, 3)
        if status_roll == 0:
            self.ailment = choice(['asleep', 'frozen'])
            self.catch_thresh = 25
        elif status_roll == 1:
            self.ailment = choice(['paralyzed', 'burned', 'poisoned'])
            self.catch_thresh = 12
        else:
            self.ailment = 'healthy'
            self.catch_thresh = 0

    def get_ailment(self):
        """Getter: Ailment
        Returns:
            String ailment
        """
        return self.ailment

    def get_thresh(self):
        """Getter: Capture Threshold
        Returns:
            Integer capture threshold
        """
        return self.catch_thresh


class Conditions(object):
    """Condition of a Pokemon

    The overall condition for capture

    Attributes:
        health: int, 1 to 100
        ailment: string, Pokemon ailment
        name: string, Pokemon name
        capture_rate: capture rate per the Pokemon
    """
    def __init__(self, pokemon):
        self.health = randint(1, 100)
        self.ailment = Ailment().get_ailment()
        self.name = pokemon
        self.capture_rate = CATCH_RATE.get(pokemon, 100)

    def print_conditions(self):
        """Print Conditions

        Used to relay information to use about pokemon condition
        """
        print('Health is at {}'.format(self.health))
        print('Opponent is currently {}'
              .format(self.ailment
                      if self.ailment != 'none'
                      else 'Opponent has no status ailments.'))


class Inventory(object):
    """The Player's Inventory

    Based on the skill level of the player

    Attributes:
        masterball: int masterball amount
        pokeball: int pokeball amount
        greatball: int greatball amount
        ultraball: int ultraball amount
    """
    def __init__(self, difficulty):
        if difficulty == 'easy':
            # make array in the next iteration
            self.masterball = 1
            self.pokeball = 20
            self.greatball = 20
            self.ultraball = 20
        else:
            self.masterball = 0
            self.pokeball = 5
            self.greatball = 5
            self.ultraball = 5

    def print_inventory(self):
        """Prints Pokeball inventory"""
        print('{}: {}: ({})'.format(1, 'masterball', self.masterball))
        print('{}: {}: ({})'.format(2, 'pokeball', self.pokeball))
        print('{}: {}: ({})'.format(3, 'greatball', self.greatball))
        print('{}: {}: ({})'.format(4, 'ultraball', self.ultraball))

    def get_ball_amount(self, value):
        """Retrieves Pokeball amounts

        Returns:
            dict with ball amounts
        """
        return {
            1: self.masterball,
            2: self.pokeball,
            3: self.greatball,
            4: self.ultraball
        }.get(value)

    def use_ball(self, ball_choice):
        """Use ball and update inventory
        Args:
            choice: int, ball choice
        """
        if ball_choice == 1:
            print('Ash threw a Masterball!')
            self.masterball -= 1
        elif ball_choice == 2:
            print('Ash threw a pokeball!')
            self.pokeball -= 1
        elif ball_choice == 3:
            print('Ash threw a greatball!')
            self.greatball -= 1
        elif ball_choice == 4:
            print('Ash threw an ultraball!')
            self.ultraball -= 1
        else:
            print('how did you even let this happen?')
            exit(1)


def main():
    """Main event loop"""
    print('******************POKEMON CAPTURE SIMULATOR***********************')
    sleep(1)

    # correct_choice = False
    difficulty = 'easy'
    # while not correctChoice:
    # 	choice = raw_input("Easy, or hard? ").lower()
    # 	correctChoice = choice.find('easy') >= 0 or choice.find('hard') >= 0

    balls = Inventory(difficulty)

    balls.print_inventory()

    pokemon = GEN_ONE[randint(0, len(GEN_ONE) - 1)]
    # pokemon = catchRate.keys().pop(randint(0,len(catchRate)-1))
    print('{}\nA wild {} appeared!'
          .format(draw_ascii(GEN_ONE.index(pokemon) + 1),
                  pokemon))
    sleep(1)
    print('\n<battle ensues>')
    # for time in xrange(1,10):
    # 	sys.stdout.write('.')
    # 	sleep(.5)

    opponent = Conditions(pokemon)
    opponent.print_conditions()
    balls.print_inventory()

    choice_check = False
    ball_choice = 0
    while not choice_check:
        ball_choice = int(input('Select number of pokeball to throw! '))
        choice_check = ball_choice >= 1 and ball_choice <= 4 and \
            balls.get_ball_amount(ball_choice) > 0
        if not choice_check:
            print('Incorrect entry. Try again')

    balls.use_ball(ball_choice)

    if capture(opponent, ball_choice):
        print('Congratulations! you caught a {}!\n'.format(pokemon))
        choosy = int(input('Catch another?: '))
        if choosy == 1:
            main()
        else:
            exit(0)
    else:
        print('Fuck! {} broke free!'.format(pokemon))
        sleep(1)
        print('{} fled!'.format(pokemon))
        return


def capture(opponent, pokeball):
    """Capture of a Pokemon

    Here take into account the equation (TBD)

    Returns:
        Boolean if the Pokemon was captured or not
    """
    print(opponent.name)
    if pokeball == 1:
        # no computation needed for a master ball
        print('<shake left>')
        sleep(1)
        print('<shake right>')
        sleep(1)
        print('<shake left>')
        sleep(1)
        print('***click***')
        sleep(1)
        return True
    return False

if __name__ == "__main__":
    main()
