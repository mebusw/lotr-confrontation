'''
Created on May 20, 2013

@author: Jacky, Terry
'''

class Game(object):
    '''
    classdocs
    '''


    def __init__(self):
        self.spawns = {}

    def setSpawn(self, spawn, tile):
        self.spawns[spawn] = tile

    
    def player1Move(self, spawn, dest):
        self.spawns[spawn] = dest

    def spawnsAt(self, tile):
        return [spawn for spawn in self.spawns if self.spawns[spawn] == tile]

    def _getWeakSpawnsAt(self, spawns, tile):
        weaks = []
        if spawns[0].isStrongerThan(spawns[1]):
            weaks.append(spawns[1])
        if spawns[1].isStrongerThan(spawns[0]):
            weaks.append(spawns[0])
        return weaks

    def resolve(self, tile):
        spawns = self.spawnsAt(tile)
        for weak in self._getWeakSpawnsAt(spawns, tile):
            del self.spawns[weak]

class Spawn(object):
    def __init__(self, name, strengh, camp):
        self.name = name
        self.strengh = strengh
        self.camp = camp
                
    def isStrongerThan(self, other):
        return self.strengh >= other.strengh