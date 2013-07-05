'''
Created on May 20, 2013

@author: Jacky, Terry
'''

class Game(object):
    '''
    classdocs
    '''


    def __init__(self, light, dark):
        self.spawns = {}
        self.light = light
        self.dark = dark

    def setSpawn(self, spawn, tile):
        self.spawns[spawn] = tile

    
    def playerMove(self, spawn, dest):
        self.spawns[spawn] = dest
        self.resolve(dest, spawn)

    def spawnsAt(self, tile):
        return [spawn for spawn in self.spawns if self.spawns[spawn] == tile]

    def _getWeakSpawns(self, spawns):
        weaks = []
        if spawns[0].isStrongerThan(spawns[1]):
            weaks.append(spawns[1])
        if spawns[1].isStrongerThan(spawns[0]):
            weaks.append(spawns[0])
        return weaks

    def resolve(self, tile, attacker):
        fightingSpawns = self.spawnsAt(tile)
        if len(fightingSpawns) > 2:
            defenser = self.dark.whoToAttack()

        if attacker != Spawns.Warg:

            if Spawns.Pippin in fightingSpawns and attacker == Spawns.Pippin:
                retreatDest = self.light.whereToRetreat()
                self.setSpawn(Spawns.Pippin, retreatDest)
                return

            if Spawns.Frodo in fightingSpawns and attacker != Spawns.Frodo:
                retreatDest = self.light.whereToRetreat()
                self.setSpawn(Spawns.Frodo, retreatDest)
                return

            for rule in [self.rule_Orc_kills_Legolas_immediately, 
                            self.rule_Merry_kills_WitchKing_immediately,
                            self.rule_Legolas_kills_FlyingNazgul_immediately,
                            ]:
                victims = rule(fightingSpawns, attacker)
                if victims:
                    for victim in victims:
                        del self.spawns[victim]
                    return

        for victim in self.rule_basic(fightingSpawns):
            del self.spawns[victim]

    def rule_basic(self, fightingSpawns, attacker=None):
        return self._getWeakSpawns(fightingSpawns)  

    def rule_Merry_kills_WitchKing_immediately(self, fightingSpawns, attacker=None):
        if Spawns.Merry in fightingSpawns and Spawns.WitchKing in fightingSpawns:
            return [Spawns.WitchKing]


    def rule_Legolas_kills_FlyingNazgul_immediately(self, fightingSpawns, attacker=None):
        if Spawns.Legolas in fightingSpawns and Spawns.FlyingNazgul in fightingSpawns:
            return [Spawns.FlyingNazgul]

    def rule_Orc_kills_Legolas_immediately(self, fightingSpawns, attacker=None):
        if Spawns.Legolas in fightingSpawns and \
            Spawns.Orcs in fightingSpawns and attacker == Spawns.Orcs:
            return [Spawns.Legolas]

    def getState(self):
        return self._state


class Spawn(object):
    def __init__(self, name, strengh, camp):
        self.name = name
        self.strengh = strengh
        self.camp = camp
                
    def isStrongerThan(self, other):
        return self.strengh >= other.strengh

    def __str__(self):
        return self.name


class Spawns:
    Frodo = Spawn('Frodo',1 , 'Light')
    Sam = Spawn('Sam', 2, 'Light')
    Merry = Spawn('Merry', 2, 'Light')
    Legolas = Spawn('Legolas', 3, 'Light')
    Pippin = Spawn('Pippin', 1, 'Light')

    Shelob = Spawn('Shelob', 5, 'Dark')
    Warg = Spawn('Warg', 2, 'Dark')
    WitchKing = Spawn('WitchKing', 5, 'Dark')
    FlyingNazgul = Spawn('FlyingNazgul', 3, 'Dark')
    Orcs = Spawn('Orcs', 3, 'Dark')   