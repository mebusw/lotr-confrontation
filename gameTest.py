'''
Created on May 20, 2013

@author: Jacky, Terry
'''
import unittest
from game import *



class TestGameRules(unittest.TestCase):


    def setUp(self):
        self.game = Game()

    def tearDown(self):
        pass


    def test_player2_meet_player1_then_stronger_win(self):
        self.game.setSpawn(Spawns.Sam, "Moria")
        self.game.setSpawn(Spawns.Shelob, "MHollinoria")
        self.game.player1Move(Spawns.Shelob, "Moria")

        self.assertIn(Spawns.Shelob, self.game.spawnsAt("Moria"))
        self.assertNotIn(Spawns.Sam, self.game.spawnsAt("Moria"))

    def test_player2_meet_player1_then_both_die(self):
        self.game.setSpawn(Spawns.Sam, "Moria")
        self.game.setSpawn(Spawns.Warg, "Hollin")
        self.game.player1Move(Spawns.Warg, "Moria")

        self.assertNotIn(Spawns.Warg, self.game.spawnsAt("Moria"))
        self.assertNotIn(Spawns.Sam, self.game.spawnsAt("Moria"))

    def test_Merry_defeat_WitchKing_immediately(self):
        self.game.setSpawn(Spawns.Merry, "Moria")
        self.game.setSpawn(Spawns.WitchKing, "Hollin")
        self.game.player1Move(Spawns.WitchKing, "Moria")

        self.assertIn(Spawns.Merry, self.game.spawnsAt("Moria"))
        self.assertIn(Spawns.WitchKing, self.game.spawnsAt("Moria"))

    def test_Legolas_defeat_FlyingNazgul_immediately(self):
        self.game.setSpawn(Spawns.Legolas, "Moria")
        self.game.setSpawn(Spawns.FlyingNazgul, "Hollin")
        self.game.player1Move(Spawns.FlyingNazgul, "Moria")

        self.assertIn(Spawns.Legolas, self.game.spawnsAt("Moria"))
        self.assertNotIn(Spawns.FlyingNazgul, self.game.spawnsAt("Moria"))

    def test_Orc_defeat_Legolas_immediately(self):
        self.game.setSpawn(Spawns.Legolas, "Moria")
        self.game.setSpawn(Spawns.Orcs, "Hollin")
        self.game.player1Move(Spawns.Orcs, "Moria")

        self.assertIn(Spawns.Orcs, self.game.spawnsAt("Moria"))
        self.assertNotIn(Spawns.Legolas, self.game.spawnsAt("Moria"))

    def test_Legolas_attack_Orc_and_both_die(self):
        self.game.setSpawn(Spawns.Orcs, "Moria")
        self.game.setSpawn(Spawns.Legolas, "Hollin")
        self.game.player1Move(Spawns.Legolas, "Moria")

        self.assertNotIn(Spawns.Orcs, self.game.spawnsAt("Moria"))
        self.assertNotIn(Spawns.Legolas, self.game.spawnsAt("Moria"))

    def test_Warg_elimates_ability_of_opponent(self):
        self.game.setSpawn(Spawns.Frodo, "Moria")
        self.game.setSpawn(Spawns.Warg, "Hollin")
        self.game.player1Move(Spawns.Warg, "Moria")

        self.assertIn(Spawns.Warg, self.game.spawnsAt("Moria"))
        self.assertNotIn(Spawns.Frodo, self.game.spawnsAt("Moria"))

    def test_Frodo_can_retreat_when_attacked(self):
        self.game.setSpawn(Spawns.Frodo, "Moria")
        self.game.setSpawn(Spawns.Orcs, "Hollin")
        self.game.player1Move(Spawns.Orcs, "Moria")

        self.assertEqual(self.game.getState(), "if_retreat_s")

    def test_Pippin_can_retreat_when_attacking(self):
        self.game.setSpawn(Spawns.Pippin, "Hollin")
        self.game.setSpawn(Spawns.Orcs, "Moria")
        self.game.player1Move(Spawns.Pippin, "Moria")

        self.assertEqual(self.game.getState(), "if_retreat_s")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()