import pygame, random, time
from Header.SoundManager import _SOUND_MANAGER
from Header.OptionManager import _LOG
from Images.Images import G_SPRITE, ICON

class Constant:
    class ConstError(TypeError): pass

    def __init__(self):
        self.__dict__['FPS'] = 120
        self.__dict__['CLOCK'] = pygame.time.Clock()
        self.__dict__['SCREEN_WIDTH'] = 420
        self.__dict__['SCREEN_HEIGHT'] = 720
        self.__dict__['SCREEN'] = pygame.display.set_mode((self.__dict__['SCREEN_WIDTH'], self.__dict__['SCREEN_HEIGHT']))
        self.__dict__['CAPTION'] = pygame.display.set_caption("Rock Scissor Paper Simulator")
        self.__dict__['ICON'] = pygame.display.set_icon(random.choice(ICON))

        self.__dict__['OPTION_SCROLLER_POS_X'] = 210
        self.__dict__['OPTION_SCROLLER_POS_Y'] = 235

        self.__dict__['ADVANCE_SCROLLER_POS_X'] = 210
        self.__dict__['ADVANCE_SCROLLER_POS_Y'] = 395

        self.__dict__['BACKGROUND_POSITION'] = (0, 0)

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError(f"Can't reallocate constant value '{name}'.")
        self.__dict__[name] = value

    def __delattr__(self, name):
        if name in self.__dict__:
            raise self.ConstError(f"Can't delete constant value '{name}'.")


class Object(pygame.sprite.Sprite):
    def __init__(self, pos, direction, speed, objType : str):
        super().__init__()
        self.objectType = objType
        self.typeDictionary = {'Rock' : 0, 'Paper' : 1, 'Scissors' : 2}
        self.image = G_SPRITE[self.typeDictionary[self.objectType]].convert_alpha()
        self.pos = pos
        self.rect = self.image.get_rect(center = self.pos)

        self.Position = pygame.math.Vector2(self.rect.center)
        self.Direction = pygame.math.Vector2(direction)
        self.BaseMoveSpeed = speed
        self.MoveSpeed = speed

        self.MoveFlag = True
        self.LastTime = time.time()
        self.SoundDelay = 0.55

    def moveObject(self, dt):
        if self.MoveFlag:
            self.Position += self.Direction * self.MoveSpeed * dt
            self.rect.center = round(self.Position.x), round(self.Position.y)
        
    def reflectObjectDirection(self):
        if self.rect.centerx < 8:
            self.rect.centerx = 8
            self.Direction.x *= -1
        elif self.rect.centerx > 412:
            self.rect.centerx = 412
            self.Direction.x *= -1

        if self.rect.centery < 8:
            self.rect.centery = 8
            self.Direction.y *= -1
        elif self.rect.centery > 712:
            self.rect.centery = 712
            self.Direction.y *= -1

    def PlayCollisionSound(self, sound_name):
        currentTime = time.time()
        if currentTime - self.LastTime > self.SoundDelay:
             _SOUND_MANAGER.PlaySound(sound_name)
             self.LastTime = currentTime

    def changeObjectType(self, collidewith):
        if self.MoveFlag:
            if self.objectType == 'Rock' and collidewith == 'Paper':
                self.objectType = 'Paper'
                self.PlayCollisionSound('SOUND_PAPER')
                _STAGE_MANAGER.ObjectSpawnerRock.thisObjectCount -= 1
                _STAGE_MANAGER.ObjectSpawnerPaper.thisObjectCount += 1

            elif self.objectType == 'Paper' and collidewith == 'Scissors':
                self.objectType = 'Scissors'
                self.PlayCollisionSound('SOUND_SCISSORS')
                _STAGE_MANAGER.ObjectSpawnerPaper.thisObjectCount -= 1
                _STAGE_MANAGER.ObjectSpawnerScissors.thisObjectCount += 1

            elif self.objectType == 'Scissors' and collidewith == 'Rock':
                self.objectType = 'Rock'
                self.PlayCollisionSound('SOUND_ROCK')
                _STAGE_MANAGER.ObjectSpawnerScissors.thisObjectCount -= 1
                _STAGE_MANAGER.ObjectSpawnerRock.thisObjectCount += 1
            
            self.image = G_SPRITE[self.typeDictionary[self.objectType]].convert_alpha()
            self.rect = self.image.get_rect(center=self.rect.center)

    def detectCollision(self):
        for obj2 in ObjectGroup:
            if self != obj2 and self.rect.colliderect(obj2.rect):
                if self.objectType == 'Rock' and obj2.objectType == 'Paper':
                    self.changeObjectType('Paper')
                if self.objectType == 'Paper' and obj2.objectType == 'Scissors':
                    self.changeObjectType('Scissors')
                if self.objectType == 'Scissors' and obj2.objectType == 'Rock':
                    self.changeObjectType('Rock')

    def update(self, dt):
        self.moveObject(dt)
        self.detectCollision()
        self.reflectObjectDirection()


class Spawner:
    def __init__(self, obj, amount, midPosition : tuple, widthRange : int, heightRange : int, group : pygame.sprite.Group):
        self.midPosition = midPosition
        self.widthRange = widthRange
        self.heightRange = heightRange
        self.ObjectType = obj
        self.SpawnAmount = amount
        self.SpawnCheck = True
        self.group = group

        self.thisObjectCount = 0

    def SpawnObjects(self):
        if self.SpawnCheck:
            for _ in range(self.SpawnAmount):
                randomWidth = random.randint(self.midPosition[0] - self.widthRange, self.midPosition[0] + self.widthRange)
                randomHeight = random.randint(self.midPosition[1] - self.heightRange, self.midPosition[1] + self.heightRange)
                randomDirection= [random.uniform(-1.2, 1.2), random.uniform(-1.2, 1.2)]
                randomSpeed = random.randint(28, 40)

                if self.ObjectType == 'Rock': 
                    newObject = Object((randomWidth, randomHeight), randomDirection, randomSpeed, self.ObjectType)
                    newObject.MoveFlag = False
                    self.thisObjectCount += 1
                    self.group.add(newObject)

                if self.ObjectType == 'Paper':
                    newObject = Object((randomWidth, randomHeight), randomDirection, randomSpeed, self.ObjectType)
                    newObject.MoveFlag = False
                    self.thisObjectCount += 1
                    self.group.add(newObject)

                if self.ObjectType == 'Scissors':
                    newObject = Object((randomWidth, randomHeight), randomDirection, randomSpeed, self.ObjectType)
                    newObject.MoveFlag = False
                    self.thisObjectCount += 1
                    self.group.add(newObject)
            
            self.SpawnCheck = False
    
    def OnMoveFlag(self):
        for obj in self.group:
            obj.MoveFlag = True


class RandomGenerator:
    def __init__(self):
        self.Reload()

    def Reload(self):

        # Paper
        self._PAPER_AMOUNT = random.randint(_LOG._CONFIG['min_value'], _LOG._CONFIG['max_value'])
        self._PAPER_MIDPOSITION_X = random.randint(0, 420)
        self._PAPER_MIDPOSITION_Y = random.randint(0, 720)
        self._PAPER_WIDTH_RANGE = random.randint(20, 200)
        self._PAPER_HEIGHT_RANGE = random.randint(20, 200)

        # Rock
        self._ROCK_AMOUNT = random.randint(_LOG._CONFIG['min_value'], _LOG._CONFIG['max_value'])
        self._ROCK_MIDPOSITION_X = random.randint(0, 420)
        self._ROCK_MIDPOSITION_Y = random.randint(0, 720)
        self._ROCK_WIDTH_RANGE = random.randint(20, 200)
        self._ROCK_HEIGHT_RANGE = random.randint(20, 200)

        # Scissors
        self._SCISSORS_AMOUNT = random.randint(_LOG._CONFIG['min_value'], _LOG._CONFIG['max_value'])
        self._SCISSORS_MIDPOSITION_X = random.randint(0, 420)
        self._SCISSORS_MIDPOSITION_Y = random.randint(0, 720)
        self._SCISSORS_WIDTH_RANGE = random.randint(20, 200)
        self._SCISSORS_HEIGHT_RANGE = random.randint(20, 200)


class StageManager:
    def __init__(self):
        self.InitializeSpawners()
        self.ObjectMultSpeedValueMax = 5

        self.WinnerConfirm = False

        self.GameOverFlag = False
        self.ObjectMultSpeed = 1
        self.PlayerSelect = None
        self.ComputerSelect = None
        self.WinnerFlag = None
        self.WhoIsWinner = None

    def InitializeSpawners(self):
        self.ObjectSpawnerPaper = Spawner('Paper', _RANDOM._PAPER_AMOUNT, (_RANDOM._PAPER_MIDPOSITION_X, _RANDOM._PAPER_MIDPOSITION_Y), \
                                           _RANDOM._PAPER_WIDTH_RANGE, _RANDOM._PAPER_HEIGHT_RANGE, ObjectGroup)
        self.ObjectSpawnerRock = Spawner('Rock', _RANDOM._ROCK_AMOUNT, (_RANDOM._ROCK_MIDPOSITION_X, _RANDOM._ROCK_MIDPOSITION_Y), \
                                           _RANDOM._ROCK_WIDTH_RANGE, _RANDOM._ROCK_HEIGHT_RANGE, ObjectGroup)
        self.ObjectSpawnerScissors = Spawner('Scissors', _RANDOM._SCISSORS_AMOUNT, (_RANDOM._SCISSORS_MIDPOSITION_X, _RANDOM._SCISSORS_MIDPOSITION_Y), \
                                           _RANDOM._SCISSORS_WIDTH_RANGE, _RANDOM._SCISSORS_HEIGHT_RANGE, ObjectGroup)

    def PredictWinner(self): # 0 : Scissors, 1 : Rock, 2 : Paper
        if self.PlayerSelect == 0:
            self.ComputerSelect = random.choice([1, 2])
        elif self.PlayerSelect == 1:
            self.ComputerSelect = random.choice([0, 2])
        elif self.PlayerSelect == 2:
            self.ComputerSelect = random.choice([0, 1])

    def RemoveOutOfRangeObject(self):
        for obj in ObjectGroup.copy():
            if obj.rect.centerx < 8 or obj.rect.centerx > _CONSTANT.SCREEN_WIDTH - 8 or obj.rect.centery < 8 or obj.rect.centery > _CONSTANT.SCREEN_HEIGHT - 8:
                obj.kill()
                ObjectGroup.remove(obj)
                if obj.objectType == 'Paper':
                    self.ObjectSpawnerPaper.thisObjectCount -= 1
                elif obj.objectType == 'Rock':
                    self.ObjectSpawnerRock.thisObjectCount -= 1
                elif obj.objectType == 'Scissors':
                    self.ObjectSpawnerScissors.thisObjectCount -= 1

    def GetObjectMultSpeedValue(self, buttonType):
        if buttonType: 
            self.ObjectMultSpeed = min(self.ObjectMultSpeedValueMax, self.ObjectMultSpeed + 1)
            for obj in ObjectGroup:
                obj.MoveSpeed = obj.BaseMoveSpeed * self.ObjectMultSpeed
        else: 
            self.ObjectMultSpeed = max(1, self.ObjectMultSpeed - 1)
            for obj in ObjectGroup:
                obj.MoveSpeed = obj.BaseMoveSpeed * self.ObjectMultSpeed
        
    def GenerateStage(self):
        _LOG._CONFIG['Count_Play'] += 1
        self.ObjectSpawnerPaper.SpawnObjects()
        self.ObjectSpawnerRock.SpawnObjects()
        self.ObjectSpawnerScissors.SpawnObjects()
        self.RemoveOutOfRangeObject()

    def ResetWinner(self):
        self.GameOverFlag = False
        self.WinnerFlag = None
        self.WhoIsWinner = None

    def ResetGame(self):
        ObjectGroup.empty()
        self.WinnerConfirm = False
        self.ObjectSpawnerPaper.SpawnCheck = True
        self.ObjectSpawnerRock.SpawnCheck = True
        self.ObjectSpawnerScissors.SpawnCheck = True
        self.ObjectSpawnerPaper.thisObjectCount = 0
        self.ObjectSpawnerRock.thisObjectCount = 0
        self.ObjectSpawnerScissors.thisObjectCount = 0
        _RANDOM.Reload()
        self.InitializeSpawners()
        self.ResetWinner()
        self.GenerateStage()

    def JudgeWinner(self): # Winner : 0 : Computer, 1 : Player, 2 : Draw
        if self.WinnerFlag == self.ComputerSelect:
            self.WhoIsWinner = 0
        elif self.WinnerFlag == self.PlayerSelect:
            self.WhoIsWinner = 1
        else:
            self.WhoIsWinner = 2

    def BlitConfirmButton(self):
        if self.ObjectSpawnerScissors.thisObjectCount == 0 or self.ObjectSpawnerRock.thisObjectCount == 0 or\
            self.ObjectSpawnerPaper.thisObjectCount == 0:
            self.WinnerConfirm = True

    def ClickConfirmButton(self):
        if self.ObjectSpawnerScissors.thisObjectCount == 0 and self.ObjectSpawnerRock.thisObjectCount == 0 and\
            self.ObjectSpawnerPaper.thisObjectCount == 0:
            _LOG._CONFIG['Count_Draw'] += 1
            self.ResetGame()
        
        else:
            if self.ObjectSpawnerPaper.thisObjectCount == 0:
                if self.ComputerSelect == 1: _LOG._CONFIG['Count_Lose'] += 1
                elif self.PlayerSelect == 1: _LOG._CONFIG['Count_Win'] += 1
                else: _LOG._CONFIG['Count_Draw'] += 1
                self.ResetGame()

            if self.ObjectSpawnerPaper.thisObjectCount == 1:
                if self.ComputerSelect == 2: _LOG._CONFIG['Count_Lose'] += 1
                elif self.PlayerSelect == 2: _LOG._CONFIG['Count_Win'] += 1
                else: _LOG._CONFIG['Count_Draw'] += 1
                self.ResetGame()

            if self.ObjectSpawnerPaper.thisObjectCount == 2:
                if self.ComputerSelect == 0: _LOG._CONFIG['Count_Lose'] += 1
                elif self.PlayerSelect == 0: _LOG._CONFIG['Count_Win'] += 1
                else: _LOG._CONFIG['Count_Draw'] += 1
                self.ResetGame()


    def PrintWinner(self):
        if self.ObjectSpawnerScissors.thisObjectCount == 0 and self.ObjectSpawnerRock.thisObjectCount == 0 and\
            self.ObjectSpawnerPaper.thisObjectCount == 0:
            self.GameOverFlag = True
            self.WinnerFlag = 2

            if self.GameOverFlag:
                self.JudgeWinner()
        
        else:
            if self.ObjectSpawnerPaper.thisObjectCount == self.ObjectSpawnerRock.thisObjectCount == 0 and \
                self.ObjectSpawnerScissors.thisObjectCount != 0:
                    self.GameOverFlag = True
                    self.WinnerFlag = 0

            if self.ObjectSpawnerScissors.thisObjectCount == self.ObjectSpawnerPaper.thisObjectCount == 0 and \
                self.ObjectSpawnerRock.thisObjectCount != 0:
                    self.GameOverFlag = True
                    self.WinnerFlag = 1

            if self.ObjectSpawnerScissors.thisObjectCount == self.ObjectSpawnerRock.thisObjectCount == 0 and \
                self.ObjectSpawnerPaper.thisObjectCount != 0:
                    self.GameOverFlag = True
                    self.WinnerFlag = 2

            if self.GameOverFlag:
                self.JudgeWinner()

# Essential Data Classes
_CONSTANT = Constant()

# GameManaging Classes and Group
_RANDOM = RandomGenerator()
ObjectGroup = pygame.sprite.Group()
_STAGE_MANAGER = StageManager()
