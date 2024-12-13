from game import location
import game.config as config
import game.display as display
from game.events import *
from game.items import Item
import random
import numpy
from game import event
from game.combat import Monster
import game.combat as combat
from game.display import menu
from game.items import Treasure



class BearIsland(location.Location):
    def __init__(self, x, y, w):
        super().__init__(x, y, w)
        self.name = "Bear Island"
        self.symbol = 'B'
        self.visitable = True

        # sub-locations
        self.locations = {}
        self.locations["cove"] = HiddenCove(self)
        self.locations["cliff"] = WhisperingCliff(self)
        self.locations["ruins"] = AncientRuins(self)
        self.locations["forest"] = EchoingForest(self)
        self.locations["lagoon"] = CrystalLagoon(self)

        self.starting_location = self.locations["cove"]

    def enter(self, ship):
        display.announce(
            "You have arrived at the Bear Island, shrouded in mist and filled with secrets.", pause=False
        )

class HiddenCove(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "Hidden Cove"
        self.verbs["north"] = self
        self.event_chance = 20  # Chance for a random treasure or trap
        self.events.append(Treasure())
    def enter(self):
        display.announce(
            "You find yourself in a secluded cove. The waves lap gently against the shore. Scattered chests lie ahead."
        )

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "north":
            config.the_player.next_loc = self.main_location.locations["cliff"]

class WhisperingCliff(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "Whispering Cliff"
        self.verbs["south"] = self
        self.puzzle_solved = False

        # Define the pool of riddles and answers
        self.riddles = {
            "I am not alive, but I can grow. I do not have lungs, but I need air. I do not have a mouth, yet water kills me.": "fire",
            "The more you take from me, the bigger I get. What am I?": "hole",
            "I speak without a mouth and hear without ears. I have no body, but I come alive with the wind. What am I?": "echo"
        }
        # Select a random riddle for this playthrough
        self.current_riddle, self.answer = random.choice(list(self.riddles.items()))

    def enter(self):
        if not self.puzzle_solved:
            display.announce(
                f"The cliff whispers riddles to you: {self.current_riddle}"
            )
        else:
            display.announce("You stand at the top of the cliff, overlooking the island.")

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "solve":
            if self.solve_puzzle(cmd_list):  # Attempt to solve the riddle
                self.puzzle_solved = True
                display.announce("You decipher the riddle and climb the cliff safely.")
            else:
                display.announce("The riddle confuses you. You slip, losing progress.")
        elif verb == "south":
            config.the_player.next_loc = self.main_location.locations["cove"]

    def solve_puzzle(self, cmd_list):
        # Check if the player's command contains the correct answer
        return self.answer in cmd_list

class AncientRuins(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "Ancient Ruins"
        self.verbs["west"] = self

    def enter(self):
        display.announce(
            "You step into ancient ruins. A ghostly guardian appears, challenging your wisdom."
        )
        if self.challenge_player():
            display.announce("The guardian vanishes, leaving a magical artifact.")
        else:
            display.announce("The guardian banishes you from the ruins.")

    def challenge_player(self):
        # Placeholder for a logic puzzle or mini-game
        return True  # Simulate success for now

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "west":
            config.the_player.next_loc = self.main_location.locations["forest"]

class EchoingForest(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "Echoing Forest"
        self.verbs["north"] = self
        self.verbs["south"] = self

        # Add treasure directly here
        self.treasure = Treasure(
            name="Ancient Gold Coin",
            description="A shiny, old gold coin with intricate engravings.",
            value=100  # Value for scoring purposes
        )

    def enter(self):
        if "Treasure Compass" in config.the_player.items:
            display.announce(
                "With the help of your Treasure Compass, you find a previously hidden trail leading deeper into the forest."
            )
        else:
            display.announce(
                "You stand in the Echoing Forest. The wind whispers through the trees, and strange sounds echo in the distance."
            )

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "north":
            config.the_player.next_loc = self.main_location.locations["whisperingCliff"]
        elif verb == "south":
            config.the_player.next_loc = self.main_location.locations["lagoon"]

class CrystalLagoon(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "Crystal Lagoon"
        self.verbs["north"] = self

    def enter(self):
        display.announce(
            "You reach a serene lagoon filled with glowing crystals. Harvesting them feels tempting yet wrong."
        )

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "harvest":
            display.announce(
                "You collect the crystals, but the lagoon's light dims. Have you made the right choice?"
            )
        elif verb == "north":
            config.the_player.next_loc = self.main_location.locations["forest"]

class LostExplorer(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "Lost Explorer"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["talk"] = self
        self.verbs["help"] = self
        self.explorer_helped = False

    def enter(self):
        if not self.explorer_helped:
            display.announce(
                "You find a lost explorer lying near a tree, seemingly injured. They look up at you with hope."
                "\n'Can you help me find my way back to the camp?'"
            )
        else:
            display.announce("The explorer smiles and thanks you for helping. They're now safely back at camp.")

    def process_verb(self, verb, cmd_list, nouns):
        if verb == "talk":
            self.talk_to_explorer()
        elif verb == "help":
            self.help_explorer()
        elif verb == "south":
            config.the_player.next_loc = self.main_location.locations["lagoon"]

    def talk_to_explorer(self):
        if not self.explorer_helped:
            display.announce(
                "'I was on an expedition and got lost. I heard rumors of treasure hidden on this island, but I can't find my way back.'"
            )
        else:
            display.announce("'Thank you again for helping me! I'll never forget your kindness.'")

    def help_explorer(self):
        if not self.explorer_helped:
            display.announce("You guide the explorer safely back to their camp. They offer you a reward in gratitude.")
            self.explorer_helped = True
            self.player_rewards()
        else:
            display.announce("The explorer no longer needs help, but they thank you again.")

    def player_rewards(self):
        # Reward the player with an item or other benefit
        display.announce("The explorer hands you a strange compass as a token of gratitude.")
        new_item = TreasureCompass()
        config.the_player.add_item(new_item)
        display.announce(f"You have received: {new_item.name}")

# Define the Treasure class
class Treasure:
    def __init__(self, name, description, value):
        self.name = name
        self.description = description
        self.value = value

    def use(self):
        
        display.announce(f"You use the {self.name}. It seems to have a special effect.")

class TreasureCompass:
    def __init__(self):
        self.name = "Treasure Compass"
        self.description = "A mysterious compass that points towards hidden treasure locations."
        self.use_effect = "Use it to find hidden treasure locations on the island."

    def use(self):
        
        display.announce("The compass begins to glow faintly, indicating a hidden treasure nearby.")
        

# Fixing treasure compass use
def use_compass(self):
    # Loop through potential treasure locations on the island
    for location in self.main_location.locations.values():
        if hasattr(location, "treasure") and location.treasure:
            display.announce(f"The compass points towards {location.name}, where treasure is hidden.")
            break
    else:
        display.announce("The compass doesn't seem to detect any nearby treasure.")
