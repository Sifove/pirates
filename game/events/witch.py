from game import event
import random

class witch (Context, event.Event):
    def __init__ (self):
        super().__init__()
        self.name = "Witch"
        self.seagulls = 1
        self.verbs['choose'] = self
        self.result = {}
        self.go = False

def witch_verb (self, verb, cmd_list, nouns):
    if (verb = choose):
        self.go = True 
        r = random.randit (1,10)
        if (r < 6):
            self.result ["message"]
        
        
        
        
        #Make the witch have the player
        #Choose what color dice she is
        #Holding in her hand 
        #If the player gets it wrong 
        #They will take damage by 85%
        #They will have at least one more
        #try before everyone is killed