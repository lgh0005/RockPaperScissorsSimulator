import pygame
from Header.GameManager import _CONSTANT
from Header.OptionManager import _LOG
from Images.Images import G_BUTTON, G_BUTTON_VOLUME, G_BUTTON_CHOOSE

class RenderText:
    def __init__(self, x, y, size, color, outlineColor, thickness, alpha, align : str, text : str):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.outlineColor = outlineColor
        self.thickness = thickness
        self.alpha = alpha
        self.align = align
        self.text = text
        self.textCache = {}

    def renderFont(self):
        cache_key = (self.text, self.size, self.color, self.outlineColor, self.thickness, self.alpha)
        if cache_key in self.textCache:
            return self.textCache[cache_key]
        
        font = pygame.font.Font("minecraft_font.ttf", self.size)
        textSurface = font.render(self.text, True, self.color).convert_alpha()

        width = textSurface.get_width() + 2 * self.thickness
        height = font.get_height() + 2 * self.thickness
        thisSurf = pygame.Surface((width, height), pygame.SRCALPHA)

        for dx in range(-self.thickness, self.thickness + 1):
            for dy in range(-self.thickness, self.thickness + 1):
                if dx*dx + dy*dy <= self.thickness*self.thickness:
                    outlineSurface = font.render(self.text, True, self.outlineColor).convert_alpha()
                    thisSurf.blit(outlineSurface, (dx + self.thickness, dy + self.thickness))

        thisSurf.blit(textSurface, (self.thickness, self.thickness))
        thisSurf.set_alpha(self.alpha)

        self.textCache[cache_key] = thisSurf
        return thisSurf
    
    def renderString(self, screen):
        objectString = self.renderFont()
        if self.align == 'Right':
            stringRect = objectString.get_rect(midright=(self.x, self.y))
        elif self.align == 'Center':
            stringRect = objectString.get_rect(center=(self.x, self.y))
        elif self.align == 'Left':
            stringRect = objectString.get_rect(midleft=(self.x, self.y))
        screen.blit(objectString, stringRect)


class Button: # Some Buttons are No used.
    def __init__(self, x, y, alpha, buttonName : str):
        self.x = x
        self.y = y
        self.buttonName = buttonName
        self.buttonDictionary = {'Play' : G_BUTTON[3], 'Option' : G_BUTTON[1], 'Quit' : G_BUTTON[4],\
                                 'Statistics' : G_BUTTON[5], 'Option_Mini' : G_BUTTON[2], 'Back' : G_BUTTON[0], \
                                 'Reset' : G_BUTTON[6], 'Howmany' : G_BUTTON[7], 'Speed_Up' : G_BUTTON[8], 'Speed_Down' : G_BUTTON[9], \
                                 'Reroll' : G_BUTTON[10], 'Ingame_BackToGame' : G_BUTTON[11], 'Ingame_Option' : G_BUTTON[12], 'Ingame_QuitToTitle' : G_BUTTON[13], \
                                 'X_Button' : G_BUTTON[14], 'Sound_Check' : G_BUTTON[15], 'Sound_No' : G_BUTTON[16], 'Ingame_Option_BackToGame' : G_BUTTON[11], \
                                 'Config' : G_BUTTON[17], 'Confirm' : G_BUTTON[18]}
        self.pos = (0, 0)
        self.state = 0
        self.clicked = False
        self.alpha = alpha

        self.image = self.buttonDictionary[self.buttonName][self.state].convert_alpha()
        self.rect = self.image.get_rect(center = (self.x, self.y))

    def MouseHoverButton(self):
        if self.rect.collidepoint(self.pos):
            self.state = 1
        else:
            self.state = 0
        self.image = self.buttonDictionary[self.buttonName][self.state].convert_alpha()
        self.image.set_alpha(self.alpha)

    def DrawButton(self, screen):
        screen.blit(self.image, self.rect)

    def Update(self):
        self.pos = pygame.mouse.get_pos()
        self.MouseHoverButton()
        self.DrawButton(_CONSTANT.SCREEN)     


class ChooseButton:
    def __init__(self, x, y, buttonName : str):
        self.x = x
        self.y = y
        self.buttonName = buttonName
        self.buttonDictionary = {'Scissors' : G_BUTTON_CHOOSE[0], 'Rock' : G_BUTTON_CHOOSE[1], \
                                 'Paper' : G_BUTTON_CHOOSE[2], 'Random' : G_BUTTON_CHOOSE[3]}

        self.pos = (0, 0)
        self.clicked = False

        self.rangeSurface = pygame.Surface((160, 160))
        self.rangeSurface.fill('black')
        self.rangeSurface.set_alpha(100)

        self.image = self.buttonDictionary[self.buttonName].convert_alpha()
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.Hovered = 100
        self.scale = 1.0

    def MouseHoverButton(self):
        if self.rect.collidepoint(self.pos):
            self.Hovered = 255
            self.scale = min(self.scale + 0.05, 1.1)
        else:
            self.Hovered = 100
            self.scale = max(self.scale - 0.05, 1.0)

    def DrawButton(self, screen):
        originalCenter = self.rect.center

        self.image = pygame.transform.rotozoom(self.buttonDictionary[self.buttonName], 0, self.scale).convert_alpha()
        self.rect = self.image.get_rect(center = originalCenter)

        rangeSurfaceRect = self.rangeSurface.get_rect(center=self.rect.center)
        screen.blit(self.rangeSurface, rangeSurfaceRect)
        screen.blit(self.image, self.rect)

    def Update(self):
        self.pos = pygame.mouse.get_pos()
        self.MouseHoverButton()
        self.DrawButton(_CONSTANT.SCREEN)


class OptionVolumeUI:
    def __init__(self, x, y=_CONSTANT.OPTION_SCROLLER_POS_Y):

        # Bar Setting
        self.pos = (0, 0)
        self.state = 0
        self.image = G_BUTTON_VOLUME[0][self.state].convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.volumeRate = round((x - 60)/276 * 100, 1)

    def SetVolumeValue(self):
        _LOG.SetOption('volume', round(self.volumeRate/100, 3))

    def MouseHoverBar(self):
        if self.rect.collidepoint(self.pos):
            self.state = 1
        else:
            self.state = 0
        self.image = G_BUTTON_VOLUME[0][self.state].convert_alpha()

    def BlitScroller(self):
        self.optionBar = G_BUTTON_VOLUME[1].convert_alpha()
        self.optionBarRect = self.optionBar.get_rect(center=(_CONSTANT.OPTION_SCROLLER_POS_X, _CONSTANT.OPTION_SCROLLER_POS_Y))
        _CONSTANT.SCREEN.blit(self.optionBar, self.optionBarRect)

    def DrawBar(self, screen):
        screen.blit(self.image, self.rect)
        
    def Update(self):
        self.pos = pygame.mouse.get_pos()
        self.volumeRate = round((self.rect.x - 60)/276 * 100, 1)
        self.SetVolumeValue()
        self.MouseHoverBar()
        self.BlitScroller()
        self.DrawBar(_CONSTANT.SCREEN)


class OptionSoundButton:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pos = (0, 0)
        self.state = 0
        self.buttonName = _LOG._CONFIG['sound']
        self.buttonDictionary = {'Sound_Check' : G_BUTTON[15], 'Sound_No' : G_BUTTON[16]}
        self.clicked = False
        self.setImage = _LOG._CONFIG['sound_flag']

        self.image = self.buttonDictionary[self.buttonName][self.state].convert_alpha()
        self.rect = self.image.get_rect(center = (self.x, self.y))

    def SetSound(self):
        if self.buttonName == 'Sound_Check': 
            _LOG.SetOption('sound_volume', 0.3)
        if self.buttonName == 'Sound_No': 
            _LOG.SetOption('sound_volume', 0)

    def MouseHoverButton(self):
        if self.rect.collidepoint(self.pos):
            self.state = 1
        else:
            self.state = 0
        self.image = self.buttonDictionary[self.buttonName][self.state].convert_alpha()
        self.rect = self.image.get_rect(center = (self.x, self.y))

    def MouseClickButton(self):
        if self.setImage == 1:
            self.buttonName = 'Sound_No'
            _LOG.SetOption('sound', "Sound_No")
            _LOG.SetOption("sound_flag", 1)
        elif self.setImage == -1:
            self.buttonName = 'Sound_Check'
            _LOG.SetOption('sound', "Sound_Check")
            _LOG.SetOption("sound_flag", -1)
        self.image = self.buttonDictionary[self.buttonName][self.state].convert_alpha()
        self.rect = self.image.get_rect(center = (self.x, self.y))

    def DrawButton(self, screen):
        screen.blit(self.image, self.rect)

    def Update(self):
        self.pos = pygame.mouse.get_pos()
        self.SetSound()
        self.MouseHoverButton()
        self.MouseClickButton()
        self.DrawButton(_CONSTANT.SCREEN) 


class MaximumObjectUI:
    def __init__(self, x, y=_CONSTANT.OPTION_SCROLLER_POS_Y):

        # Bar Setting
        self.pos = (0, 0)
        self.state = 0
        self.image = G_BUTTON_VOLUME[0][self.state].convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.maxValue = max(1, int((x - 60)/138*100))

    def SetMaxValue(self):
        _LOG.SetOption('max_value', self.maxValue)

    def MouseHoverBar(self):
        if self.rect.collidepoint(self.pos):
            self.state = 1
        else:
            self.state = 0
        self.image = G_BUTTON_VOLUME[0][self.state].convert_alpha()

    def BlitScroller(self):
        self.optionBar = G_BUTTON_VOLUME[1].convert_alpha()
        self.optionBarRect = self.optionBar.get_rect(center=(_CONSTANT.OPTION_SCROLLER_POS_X, _CONSTANT.OPTION_SCROLLER_POS_Y))
        _CONSTANT.SCREEN.blit(self.optionBar, self.optionBarRect)

    def DrawBar(self, screen):
        screen.blit(self.image, self.rect)
        
    def Update(self):
        self.pos = pygame.mouse.get_pos()
        self.maxValue = max(1, int((self.rect.x - 60)/138*100))
        self.SetMaxValue()
        self.MouseHoverBar()
        self.BlitScroller()
        self.DrawBar(_CONSTANT.SCREEN)


class MinimumObjectUI:
    def __init__(self, x, y=_CONSTANT.ADVANCE_SCROLLER_POS_Y):

        # Bar Setting
        self.pos = (0, 0)
        self.state = 0
        self.image = G_BUTTON_VOLUME[0][self.state].convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.minValue = max(1, int((x - 60)/138*100))

    def SetMaxValue(self):
        _LOG.SetOption('min_value', self.minValue)

    def MouseHoverBar(self):
        if self.rect.collidepoint(self.pos):
            self.state = 1
        else:
            self.state = 0
        self.image = G_BUTTON_VOLUME[0][self.state].convert_alpha()

    def BlitScroller(self):
        self.optionBar = G_BUTTON_VOLUME[1].convert_alpha()
        self.optionBarRect = self.optionBar.get_rect(center=(_CONSTANT.ADVANCE_SCROLLER_POS_X, _CONSTANT.ADVANCE_SCROLLER_POS_Y))
        _CONSTANT.SCREEN.blit(self.optionBar, self.optionBarRect)

    def DrawBar(self, screen):
        screen.blit(self.image, self.rect)
        
    def Update(self):
        self.pos = pygame.mouse.get_pos()
        self.minValue = max(1, int((self.rect.x - 60)/138*100))
        self.SetMaxValue()
        self.MouseHoverBar()
        self.BlitScroller()
        self.DrawBar(_CONSTANT.SCREEN)

# Private Button Members
class Buttons: 
    def __init__(self):

        # Normal Buttons
        self._PLAY = Button(210, 380, 255, 'Play')
        self._OPTION = Button(108, 440, 255, 'Option')
        self._QUIT = Button(312, 440, 255, 'Quit')
        self._STATISTICS = Button(210, 592, 255, 'Statistics')

        # Back Buttons
        self._BACK_1 = Button(210, 664, 255, 'Back')
        self._BACK_2 = Button(210, 630, 255, 'Back')
        self._BACK_3 = Button(210, 650, 255, 'Back')
        self._BACK_5 = Button(210, 650, 255, 'Back')
        self._BACK_4 = Button(210, 630, 255, 'Ingame_Option_BackToGame')

        # Option Buttons
        self._RESET = Button(324, 320, 255, 'Reset')
        self._OPTION_BAR = OptionVolumeUI(round(276 * _LOG._CONFIG['volume'] + 72, 3))
        self._OPTION_SOUNDCHECKER = OptionSoundButton(324, 400)
        self._OPTION_ADVANCE = Button(210, 520, 255, 'Config')

        # Advance
        self._ADVANCE_MAX_BAR = MaximumObjectUI(round(1.38 * _LOG._CONFIG['max_value'] + 72, 3))
        self._ADVANCE_MIN_BAR = MinimumObjectUI(round(1.38 * _LOG._CONFIG['min_value'] + 72, 3))

        # Choose Buttons
        self._SCISSORS = ChooseButton(113, 280, 'Scissors')
        self._ROCK = ChooseButton(307, 280, 'Rock')
        self._PAPER = ChooseButton(113, 474, 'Paper')
        self._RANDOM = ChooseButton(307, 474, 'Random')

        # Playground Buttons
        self._PLAYGROUND_OPTION = Button(385, 35, 40, 'Option_Mini')
        self._PLAYGROUND_REROLL = Button(320, 35, 100, 'Reroll')
        self._PLAYGROUND_HOWMANY = Button(104, 35, 40, 'Howmany')
        self._PLAYGROUND_SPEED_UP = Button(35, 650, 40, 'Speed_Up')
        self._PLAYGROUND_SPEED_DOWN = Button(35, 695, 40, 'Speed_Down')

        # Pause Buttons
        self._PAUSE_BACKTOGAME = Button(210, 315, 255, 'Ingame_BackToGame')
        self._PAUSE_QUITTOTITLE = Button(210, 405, 255, 'Ingame_QuitToTitle')

# Private Text Members
class Text:
    def __init__(self):

        # Main Menu
        self._MAINMENU_LOGO_1 = RenderText(210, 80, 50, 'white', 'black', 3, 255, 'Center', "Rock")
        self._MAINMENU_LOGO_2 = RenderText(210, 150, 50, 'white', 'black', 3, 255, 'Center', "Paper")
        self._MAINMENU_LOGO_3 = RenderText(210, 220, 50, 'white', 'black', 3, 255, 'Center', "Scissors!")

        # Choose Menu
        self._CHOOSEMENU_LOGO_1 = RenderText(210, 80, 40, 'white', 'black', 3, 255, 'Center', "Which")
        self._CHOOSEMENU_LOGO_2 = RenderText(210, 150, 40, 'white', 'black', 3, 255, 'Center', "Is Gonna Win?")

        # Option
        self._OPTION_LOGO_1 = RenderText(210, 80, 50, 'white', 'black', 3, 255, 'Center', "Option")
        self._OPTION_LOGO_2 = RenderText(45, 160, 30, 'white', 'black', 3, 255, 'Left', "Volume")
        self._OPTION_LOGO_3 = RenderText(45, 320, 30, 'white', 'black', 3, 255, 'Left', "Reset")
        self._OPTION_LOGO_4 = RenderText(45, 400, 30, 'white', 'black', 3, 255, 'Left', "Sound")
        self._OPTION_LOGO_WARNING_1 = RenderText(210, 380, 18, 'white', 'black', 3, 255, 'Center', "If you click Reset,")
        self._OPTION_LOGO_WARNING_2 = RenderText(210, 405, 18, 'white', 'black', 3, 255, 'Center', "You can't restore the Statistics!")
        self._OPTION_LOGO_WARNING_3 = RenderText(210, 438, 20, 'red', 'black', 3, 255, 'Center', "WITH NO WARNINGS!")

        # Advance
        self._ADVANCE_LOGO_1 = RenderText(210, 80, 50, 'white', 'black', 3, 255, 'Center', "Configure")
        self._ADVANCE_LOGO_2 = RenderText(45, 160, 30, 'white', 'black', 3, 255, 'Left', "Max Range")
        self._ADVANCE_LOGO_3 = RenderText(45, 320, 30, 'white', 'black', 3, 255, 'Left', "Min Range")

        self._ADVANCE_LOGO_WARNING_1 = RenderText(210, 470, 20, 'Red', 'black', 3, 255, 'Center', "WARNING!") 
        self._ADVANCE_LOGO_WARNING_2 = RenderText(210, 503, 18, 'white', 'black', 3, 255, 'Center', "Min Range can't exceed Max Range!")
        self._ADVANCE_LOGO_WARNING_3 = RenderText(210, 528, 18, 'white', 'black', 3, 255, 'Center', "Please try again with an")
        self._ADVANCE_LOGO_WARNING_4 = RenderText(210, 553, 18, 'white', 'black', 3, 255, 'Center', "appropriate Min Range value.")

        # Statistics
        self._STATISTICS_LOGO_1 = RenderText(210, 80, 50, 'white', 'black', 3, 255, 'Center', "Statistics")
        self._STATISTICS_LOGO_2 = RenderText(60, 180, 30, 'Green', 'black', 3, 255, 'Left', "Win :")
        self._STATISTICS_LOGO_3 = RenderText(60, 280, 30, 'Red', 'black', 3, 255, 'Left', "Lose :")
        self._STATISTICS_LOGO_4 = RenderText(60, 400, 30, 'white', 'black', 3, 255, 'Left', "Rate :")

        # Playground
        self._PLAYGROUND_LOGO_1 = RenderText(210, 250, 50, 'white', 'black', 3, 255, 'Center', "Press")
        self._PLAYGROUND_LOGO_2 = RenderText(210, 330, 50, 'white', 'black', 3, 255, 'Center', "'Z' Key")
        self._PLAYGROUND_LOGO_3 = RenderText(210, 410, 50, 'white', 'black', 3, 255, 'Center', "to Start!")

        self._PLAYGROUND_LOGO_WINNER_C = RenderText(210, 330, 50, 'white', 'black', 3, 255, 'Center', "Computer")
        self._PLAYGROUND_LOGO_WINNER_P = RenderText(210, 330, 50, 'white', 'black', 3, 255, 'Center', "Player")
        self._PLAYGROUND_LOGO_WINNER_1 = RenderText(210, 410, 50, 'white', 'black', 3, 255, 'Center', "Win!")
        self._PLAYGROUND_LOGO_WINNER_2 = RenderText(210, 360, 50, 'white', 'black', 3, 255, 'Center', "Draw!")

    def CalculateWinRate(self):
        try:
            return round(_LOG._CONFIG['Count_Win'] / (_LOG._CONFIG['Count_Play'] - _LOG._CONFIG['Count_Draw']) * 100, 1)
        except ZeroDivisionError:
            return 0.0

# UI Classes
_TEXT = Text()
_BUTTON = Buttons()