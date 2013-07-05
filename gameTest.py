'''
Created on May 20, 2013

@author: Jacky, Terry
'''
import unittest
from game import *

class Mock:
    def __init__(self):
        self.callInfo = {}

    def verify(self):
        if not all(count == 0 for  key, count in self.callInfo.iteritems()):
            raise Exception(self.callInfo)

    def whereToRetreat(self):
        if 'whereToRetreat' not in self.callInfo:
            raise Exception()
        self.callInfo['whereToRetreat'] -= 1
        return self.returnValue

    def whoToAttack(self):
        if 'whoToAttack' not in self.callInfo:
            raise Exception()
        self.callInfo['whoToAttack'] -= 1
        return self.returnValue

    def expectOneCall(self, fun):
        self.callInfo[fun] = 1
        return self

    def returnValue(self, value):
        self.returnValue = value

class TestGameRules(unittest.TestCase):


    def setUp(self):
        self.light = Mock()
        self.dark = Mock()
        self.game = Game(self.light, self.dark)

    def tearDown(self):
        self.light.verify()
        self.dark.verify()

    def test_player2_meet_player1_then_stronger_win(self):
        self.game.setSpawn(Spawns.Sam, "Moria")
        self.game.setSpawn(Spawns.Shelob, "MHollinoria")
        self.game.playerMove(Spawns.Shelob, "Moria")

        self.assertIn(Spawns.Shelob, self.game.spawnsAt("Moria"))
        self.assertNotIn(Spawns.Sam, self.game.spawnsAt("Moria"))

    def test_player2_meet_player1_then_both_die(self):
        self.game.setSpawn(Spawns.Sam, "Moria")
        self.game.setSpawn(Spawns.Warg, "Hollin")
        self.game.playerMove(Spawns.Warg, "Moria")

        self.assertNotIn(Spawns.Warg, self.game.spawnsAt("Moria"))
        self.assertNotIn(Spawns.Sam, self.game.spawnsAt("Moria"))

    def test_Merry_defeat_WitchKing_immediately(self):
        self.game.setSpawn(Spawns.Merry, "Moria")
        self.game.setSpawn(Spawns.WitchKing, "Hollin")
        self.game.playerMove(Spawns.WitchKing, "Moria")

        self.assertIn(Spawns.Merry, self.game.spawnsAt("Moria"))
        self.assertNotIn(Spawns.WitchKing, self.game.spawnsAt("Moria"))

    def test_Legolas_defeat_FlyingNazgul_immediately(self):
        self.game.setSpawn(Spawns.Legolas, "Moria")
        self.game.setSpawn(Spawns.FlyingNazgul, "Hollin")
        self.game.playerMove(Spawns.FlyingNazgul, "Moria")

        self.assertIn(Spawns.Legolas, self.game.spawnsAt("Moria"))
        self.assertNotIn(Spawns.FlyingNazgul, self.game.spawnsAt("Moria"))

    def test_Orc_defeat_Legolas_immediately(self):
        self.game.setSpawn(Spawns.Legolas, "Moria")
        self.game.setSpawn(Spawns.Orcs, "Hollin")
        self.game.playerMove(Spawns.Orcs, "Moria")

        self.assertIn(Spawns.Orcs, self.game.spawnsAt("Moria"))
        self.assertNotIn(Spawns.Legolas, self.game.spawnsAt("Moria"))

    def test_Legolas_attack_Orc_and_both_die(self):
        self.game.setSpawn(Spawns.Orcs, "Moria")
        self.game.setSpawn(Spawns.Legolas, "Hollin")
        self.game.playerMove(Spawns.Legolas, "Moria")

        self.assertNotIn(Spawns.Orcs, self.game.spawnsAt("Moria"))
        self.assertNotIn(Spawns.Legolas, self.game.spawnsAt("Moria"))

    def test_Warg_elimates_ability_of_opponent(self):
        self.game.setSpawn(Spawns.Frodo, "Moria")
        self.game.setSpawn(Spawns.Warg, "Hollin")
        self.game.playerMove(Spawns.Warg, "Moria")

        self.assertIn(Spawns.Warg, self.game.spawnsAt("Moria"))
        self.assertNotIn(Spawns.Frodo, self.game.spawnsAt("Moria"))

    def test_Frodo_can_retreat_when_attacked(self):
        self.game.setSpawn(Spawns.Frodo, "Moria")
        self.game.setSpawn(Spawns.Orcs, "Hollin")
        self.light.expectOneCall("whereToRetreat").returnValue("XXX")

        self.game.playerMove(Spawns.Orcs, "Moria")

        self.assertIn(Spawns.Orcs, self.game.spawnsAt("Moria"))
        self.assertIn(Spawns.Frodo, self.game.spawnsAt("XXX"))

    def test_Pippin_can_retreat_when_attacking(self):
        self.game.setSpawn(Spawns.Pippin, "Hollin")
        self.game.setSpawn(Spawns.Orcs, "Moria")
        self.light.expectOneCall("whereToRetreat").returnValue("XXX")

        self.game.playerMove(Spawns.Pippin, "Moria")

        self.assertIn(Spawns.Orcs, self.game.spawnsAt("Moria"))
        self.assertIn(Spawns.Pippin, self.game.spawnsAt("XXX"))


    def test_attacking_player_should_choose_one_to_fight_then_the_other(self):
        self.game.setSpawn(Spawns.Sam, "Moria")
        self.game.setSpawn(Spawns.Pippin, "Moria")
        self.game.setSpawn(Spawns.FlyingNazgul, "Hollin")
        self.dark.expectOneCall("whoToAttack").returnValue(Spawns.Sam)

        self.game.playerMove(Spawns.FlyingNazgul, "Moria", self.dark)

        self.assertIn(Spawns.FlyingNazgul, self.game.spawnsAt("Moria"))
        self.assertNotIn(Spawns.Sam, self.game.spawnsAt("Moria"))
        self.assertNotIn(Spawns.Pippin, self.game.spawnsAt("Moria"))

    def test_Sam_get_5_strength_to_beat_FlyingNazgul_when_standing_with_Frodo(self):
        self.game.setSpawn(Spawns.Sam, "Moria")
        self.game.setSpawn(Spawns.Frodo, "Moria")
        self.game.setSpawn(Spawns.FlyingNazgul, "Hollin")

        self.game.playerMove(Spawns.FlyingNazgul, "Moria", self.dark)

        self.assertNotIn(Spawns.FlyingNazgul, self.game.spawnsAt("Moria"))
        self.assertIn(Spawns.Sam, self.game.spawnsAt("Moria"))
        self.assertIn(Spawns.Frodo, self.game.spawnsAt("Moria"))

###TODO
### should validate if XXX can retreat to


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()