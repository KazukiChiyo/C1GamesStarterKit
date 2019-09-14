import gamelib
import random
import math
import warnings
from sys import maxsize
import json
from attack import AttackStrategy

"""
Most of the algo code you write will be in this file unless you create new
modules yourself. Start by modifying the 'on_turn' function.

Advanced strategy tips: 

  - You can analyze action frames by modifying on_action_frame function

  - The GameState.map object can be manually manipulated to create hypothetical 
  board states. Though, we recommended making a copy of the map to preserve 
  the actual current map state.
"""

class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        seed = random.randrange(maxsize)
        random.seed(seed)
        gamelib.debug_write('Random seed: {}'.format(seed))

    def on_game_start(self, config):
        """ 
        Read in config and perform any initial setup here 
        """
        gamelib.debug_write('Configuring your custom algo strategy...')
        self.config = config
        global FILTER, ENCRYPTOR, DESTRUCTOR, PING, EMP, SCRAMBLER
        FILTER = config["unitInformation"][0]["shorthand"]
        ENCRYPTOR = config["unitInformation"][1]["shorthand"]
        DESTRUCTOR = config["unitInformation"][2]["shorthand"]
        PING = config["unitInformation"][3]["shorthand"]
        EMP = config["unitInformation"][4]["shorthand"]
        SCRAMBLER = config["unitInformation"][5]["shorthand"]
        # This is a good place to do initial setup
        self.scored_on_locations = []
        self.UnitDict = dict()  # key is ID, [0] is spawned at, [1] is unit type, [2] is owner

        self.Scrambler_at = []
        self.Damage = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.Breach = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.Breach_Coef = 20
        self.Score = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.Score_Forget =0.8
        

    def on_turn(self, turn_state):
        """
        This function is called every turn with the game state wrapper as
        an argument. The wrapper stores the state of the arena and has methods
        for querying its state, allocating your current resources as planned
        unit deployments, and transmitting your intended deployments to the
        game engine.
        """

        state = json.loads(turn_string)
        events = state["events"]

        gamelib.debug_write(events)
        for attack in events["attack"]:
            if attack[6] == 2 and attack[3] == 5:  # enemy Scrambler
                ID = attack[5]
                if ID not in self.UnitDict.keys():
                    for spawn in events["spawn"]:
                        if spawn[2] == ID:
                            self.UnitDict[ID] = [0,0,0]
                            self.UnitDict[ID][0] = spawn[0]
                            self.UnitDict[ID][1] = spawn[1]
                            self.UnitDict[ID][2] = spawn[3]
                        break
                if self.UnitDict[ID][0] == 3 or self.UnitDict[ID][0] == 4:
                    self.Scrambler_at.append(attack[0])


            if attack[3] == 3 or attack[3] ==4: # PING or EMP
                if attack[6] == 1:   # MINE
                    ID = attack[5]
                if ID not in self.UnitDict.keys():
                    for spawn in events["spawn"]:
                        if spawn[2] == ID:
                            self.UnitDict[ID] = [0,0,0]
                            self.UnitDict[ID][0] = spawn[0]
                            self.UnitDict[ID][1] = spawn[1]
                            self.UnitDict[ID][2] = spawn[3]
                        break
            self.Damage[self.UnitDict[ID][0]]+=attack[2]   #add the damage done into damage list

        for breach in events["breach"]:
            if breach[4] == 1: #I breached!!
                ID = breach[3]
                if ID not in self.UnitDict.keys():
                    for spawn in events["spawn"]:
                        if spawn[2] == ID:
                            self.UnitDict[ID] = [0,0,0]
                            self.UnitDict[ID][0] = spawn[0]
                            self.UnitDict[ID][1] = spawn[1]
                            self.UnitDict[ID][2] = spawn[3]
                        break
                self.Breach[self.UnitDict[ID][0]]+=1 # add 1 breach to the starting point

        gamelib.debug_write(self.UnitDict)

        for i in range(28):
            self.Score[i] = self.Score[i]*self.Score_forget
            self.Score[i] += self.Damage[i] + self.Breach[i]*self.Breach_Coef



        game_state = gamelib.GameState(self.config, turn_state)
        game_state.suppress_warnings(True)  #Comment or remove this line to enable warnings.


        Strategy = AttackStrategy()
        Strategy.spawn_attackers(game_state, self.Scrambler_at, self.Score, risk_level)


        game_state.submit_turn()


    """
    NOTE: All the methods after this point are part of the sample starter-algo
    strategy and can safely be replaced for your custom algo.
    """


    def on_action_frame(self, turn_string):
        """
        This is the action frame of the game. This function could be called 
        hundreds of times per turn and could slow the algo down so avoid putting slow code here.
        Processing the action frames is complicated so we only suggest it if you have time and experience.
        Full doc on format of a game frame at: https://docs.c1games.com/json-docs.html
        """
        # Let's record at what position we get scored on


if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
