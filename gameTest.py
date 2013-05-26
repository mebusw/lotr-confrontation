'''
Created on May 20, 2013

@author: Jacky, Terry
'''
import unittest
from game import *

class Test(unittest.TestCase):


    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_player1_move_spawn(self):
        game = Game()
        spawn = Spawn('Frodo',1 , 'Expedit') 
        game.setSpawn(spawn, "Hollin")
        game.player1Move(spawn, dest = "Moria")

        self.assertIn(spawn, game.spawnsAt("Moria"))
        self.assertNotIn(spawn, game.spawnsAt("Hollin"))


    def test_player2_meet_player1_then_stronger_win(self):
        game = Game()
        spawn1 = Spawn('Sam', 2, 'Expedit')
        spawn2 = Spawn('Shelob', 5, 'Sauron')
        game.setSpawn(spawn1, "Moria")
        game.setSpawn(spawn2, "Moria")
        game.resolve("Moria")

        self.assertIn(spawn2, game.spawnsAt("Moria"))
        self.assertNotIn(spawn1, game.spawnsAt("Moria"))

    def test_player2_meet_player1_then_both_die(self):
        game = Game()
        spawn1 = Spawn('Sam', 2, 'Expedit')
        spawn2 = Spawn('Warg', 2, 'Sauron')
        game.setSpawn(spawn1, "Moria")
        game.setSpawn(spawn2, "Moria")
        game.resolve("Moria")

        self.assertNotIn(spawn2, game.spawnsAt("Moria"))
        self.assertNotIn(spawn1, game.spawnsAt("Moria"))

        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()