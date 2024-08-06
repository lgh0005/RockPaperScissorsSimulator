import sys, pygame, random, time
from Images.Images import *
from Header.GameManager import _CONSTANT, _STAGE_MANAGER, ObjectGroup
from Header.UIManager import _TEXT, _BUTTON, RenderText
from Header.SoundManager import _SOUND_MANAGER, _MUSIC_MANAGER, SoundManagerUpdate
from Header.OptionManager import _LOG

class GameRunner:
    # --- CheckEvent For Scene : MainMenu
    def CheckEvent_MainMenu(self, button1, button2, button3): # button1 : 'ChooseRockScissorPaper', button2 : 'Option', button3 : 'Quit'
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _SCENE.exiter = True
                _SCENE.Exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                # Button : ChooseRockScissorPaper
                if button1.rect.collidepoint(button1.pos) and pygame.mouse.get_pressed()[0]:
                    if not button1.clicked:
                        button1.clicked = True
                        _SOUND_MANAGER.PlaySound('SOUND_CLICK')
                        button1.clicked = False
                        _SCENE.ChooseRockScissorPaper()   
                else:
                    button1.clicked = False

                # Button : Option
                if button2.rect.collidepoint(button2.pos) and pygame.mouse.get_pressed()[0]:
                    if not button2.clicked:
                        button2.clicked = True
                        _SOUND_MANAGER.PlaySound('SOUND_CLICK')
                        _SCENE.AccessFlag = True
                        button2.clicked = False
                        _SCENE.Option()
                else:
                    button2.clicked = False

                # Button : Quit
                if button3.rect.collidepoint(button3.pos) and pygame.mouse.get_pressed()[0]:
                    if not button2.clicked:
                        button3.clicked = True
                        _SOUND_MANAGER.PlaySound('SOUND_CLICK')
                        button3.clicked = False
                        _SCENE.exiter = True
                        _SCENE.Exit()
                else:
                    button3.clicked = False

    # --- CheckEvent For Scene : ChooseRockScissorPaper
    def CheckEvent_ChooseRockScissorPaper(self, button1, button2, button3, button4, button5): # button1 : 'Back', button2 : 'Scissors', button3 : 'Rock', button4 : 'Paper', button5 : 'Random'
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _SCENE.exiter = True
                _SCENE.Exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                # Button : Back
                if button1.rect.collidepoint(button1.pos) and pygame.mouse.get_pressed()[0]:
                    if not button1.clicked:
                        button1.clicked = True
                        _SOUND_MANAGER.PlaySound('SOUND_CLICK')
                        button1.clicked = False
                        _SCENE.MainMenu()
                else:
                    button1.clicked = False

                # Button : Scissors
                if button2.rect.collidepoint(button2.pos) and pygame.mouse.get_pressed()[0]:
                    if not button2.clicked:
                        button2.clicked = True
                        _SOUND_MANAGER.PlaySound('SOUND_CLICK')
                        button2.clicked = False
                        _STAGE_MANAGER.PlayerSelect = 0
                        _STAGE_MANAGER.PredictWinner()
                        _SCENE.Playground()
                else:
                    button2.clicked = False

                # Button : Rock
                if button3.rect.collidepoint(button3.pos) and pygame.mouse.get_pressed()[0]:
                    if not button3.clicked:
                        button3.clicked = True
                        _SOUND_MANAGER.PlaySound('SOUND_CLICK')
                        button3.clicked = False
                        _STAGE_MANAGER.PlayerSelect = 1
                        _STAGE_MANAGER.PredictWinner()
                        _SCENE.Playground()
                else:
                    button3.clicked = False

                # Button : Paper
                if button4.rect.collidepoint(button4.pos) and pygame.mouse.get_pressed()[0]:
                    if not button4.clicked:
                        button4.clicked = True
                        _SOUND_MANAGER.PlaySound('SOUND_CLICK')
                        button4.clicked = False
                        _STAGE_MANAGER.PlayerSelect = 2
                        _STAGE_MANAGER.PredictWinner()
                        _SCENE.Playground()
                else:
                    button4.clicked = False

                # Button : Random
                if button5.rect.collidepoint(button5.pos) and pygame.mouse.get_pressed()[0]:
                    if not button5.clicked:
                        button5.clicked = True
                        _SOUND_MANAGER.PlaySound('SOUND_CLICK')
                        button5.clicked = False
                        _STAGE_MANAGER.PlayerSelect = random.randint(0, 2)
                        _STAGE_MANAGER.PredictWinner()
                        _SCENE.Playground()
                else:
                    button5.clicked = False
    
    # --- CheckEvent For Scene : Statistics
    def CheckEvent_Statistics(self, button1): # button1 : 'Back'
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _SCENE.exiter = True
                _SCENE.Exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                # Button : Back
                if button1.rect.collidepoint(button1.pos) and pygame.mouse.get_pressed()[0]:
                    if not button1.clicked:
                        button1.clicked = True
                        _SOUND_MANAGER.PlaySound('SOUND_CLICK')
                        button1.clicked = False
                        _SCENE.Option()
                else:
                    button1.clicked = False
    # -------------------------------------

    # --- CheckEvent For Scene : Option
    def CheckEvent_Option(self, button1, button2, button3, button4, button5, button6): # button1 : 'Back', button2 : 'Statistics', button3 : 'Reset', button4 : 'Volume Bar', button5 : 'Option_Checker', button6 : 'Config : Advanced'
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _SCENE.exiter = True
                _SCENE.Exit()

            # Move Volume Bar
            if event.type == pygame.MOUSEMOTION:
                if button3.rect.collidepoint(button3.pos):
                    if not _SCENE.MouseHoverSoundPlayed:
                        _SOUND_MANAGER.PlaySound('SOUND_RESET_WARNING')
                        _SCENE.MouseHoverSoundPlayed = True
                else:
                    if _SCENE.MouseHoverSoundPlayed:
                        _SOUND_MANAGER.StopSound('SOUND_RESET_WARNING')
                        _SCENE.MouseHoverSoundPlayed = False

                if button4.rect.collidepoint(button4.pos) and pygame.mouse.get_pressed()[0]:
                    button4.rect.x = pygame.mouse.get_pos()[0]
                    if button4.rect.x <= 60: button4.rect.x = 60
                    if button4.rect.x >= 336: button4.rect.x = 336

            # Button Click Event
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Button : Back
                if button1.rect.collidepoint(button1.pos) and pygame.mouse.get_pressed()[0]:
                    if not button1.clicked:
                        button1.clicked = True
                        _SOUND_MANAGER.PlaySound('SOUND_CLICK')
                        _LOG.SaveConfig()
                        button1.clicked = False
                        _SCENE.MainMenu()       
                else:
                    button1.clicked = False

                # Button : Statistics
                if button2.rect.collidepoint(button2.pos) and pygame.mouse.get_pressed()[0]:
                    if not button2.clicked:
                        button2.clicked = True
                        _SOUND_MANAGER.PlaySound('SOUND_CLICK')
                        button2.clicked = False
                        _SCENE.Statics()       
                else:
                    button2.clicked = False

                # Button : Reset
                if button3.rect.collidepoint(button3.pos) and pygame.mouse.get_pressed()[0]:
                    if not button3.clicked:
                        button3.clicked = True
                        _SOUND_MANAGER.PlaySound('SOUND_RESET')
                        button3.clicked = False 
                        _LOG._CONFIG['Count_Play'] = 0
                        _LOG._CONFIG['Count_Win'] = 0
                        _LOG._CONFIG['Count_Lose'] = 0
                        _LOG._CONFIG['Count_Draw'] = 0
                        _LOG.SaveConfig()
                else:
                    button3.clicked = False

                # Button : Sound Checker -> O or X
                if button5.rect.collidepoint(button5.pos) and pygame.mouse.get_pressed()[0]:
                    if not button5.clicked:
                        button5.clicked = True
                        _SOUND_MANAGER.PlaySound('SOUND_CLICK')
                        button5.setImage *= -1
                        button5.clicked = False
                else:
                    button5.clicked = False    

                # Button : Config : Advanced
                if button6.rect.collidepoint(button6.pos) and pygame.mouse.get_pressed()[0]:
                    if not button6.clicked:
                        button6.clicked = True
                        _SOUND_MANAGER.PlaySound('SOUND_CLICK')
                        button6.clicked = False
                        _SCENE.Advance()
                else:
                    button6.clicked = False 
    # -------------------------------------

    # --- CheckEvent For Scene : Advance
    def CheckEvent_Advance(self, button1, button2, button3): # button1 : 'Back' , button2 : 'Max Range Bar', button3 : 'Min Range Bar'
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if _LOG._CONFIG['max_value'] >= _LOG._CONFIG['min_value']:
                    _SCENE.exiter = True
                    _SCENE.Exit()
                else:
                    _SOUND_MANAGER.PlaySound('SOUND_LOSE')

             # Move Volume Bar
            if event.type == pygame.MOUSEMOTION:
                if button2.rect.collidepoint(button2.pos) and pygame.mouse.get_pressed()[0]:
                    button2.rect.x = pygame.mouse.get_pos()[0]
                    if button2.rect.x <= 60: button2.rect.x = 60
                    if button2.rect.x >= 336: button2.rect.x = 336

                if button3.rect.collidepoint(button3.pos) and pygame.mouse.get_pressed()[0]:
                    button3.rect.x = pygame.mouse.get_pos()[0]
                    if button3.rect.x <= 60: button3.rect.x = 60
                    if button3.rect.x >= 336: button3.rect.x = 336

            if event.type == pygame.MOUSEBUTTONDOWN:

                # Button : Back
                if button1.rect.collidepoint(button1.pos) and pygame.mouse.get_pressed()[0]:
                    if not button1.clicked:
                        if _LOG._CONFIG['max_value'] >= _LOG._CONFIG['min_value']:
                            button1.clicked = True
                            _SOUND_MANAGER.PlaySound('SOUND_CLICK')
                            button1.clicked = False
                            _SCENE.FirstPlayed = False
                            _SCENE.Option()

                        else:
                            button1.clicked = True
                            _SOUND_MANAGER.PlaySound('SOUND_LOSE')
                            button1.clicked = False
                else:
                    button1.clicked = False

    # --- CheckEvent For Scene : Playground
    def CheckEvent_Playground(self, button1, button2, button3, button4, button5) : # button1 : 'Option_Mini', button2 : 'Howmany' button3 : 'Speed_Up', button4 : 'Speed_Down', button5 : 'Reroll'
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _SCENE.exiter = True
                _SCENE.Exit()

            # Howmany Button : Hover This Button
            if event.type == pygame.MOUSEMOTION:
                if button2.rect.collidepoint(button2.pos): _SCENE.Trigger = True
                else: _SCENE.Trigger = False

                if button3.rect.collidepoint(button3.pos) or button4.rect.collidepoint(button4.pos) : _SCENE.Trigger2 = True
                else: _SCENE.Trigger2 = False

            # Button Click Event
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Button : Reroll
                if button5.rect.collidepoint(button1.pos) and pygame.mouse.get_pressed()[0]:
                    if not button5.clicked:
                        button5.clicked = True
                        button5.clicked = False

                        _SCENE.BackgroundRandomIndex = random.randint(0, 11)
                        _SCENE.GameOverProcessed = False
                        _STAGE_MANAGER.ResetGame()
                        _STAGE_MANAGER.ObjectMultSpeed = 1
                        _SCENE.PressKeyLogo = -1
                        
                else: 
                    button5.clicked = False

                # Button : Option Mini Button
                if button1.rect.collidepoint(button1.pos) and pygame.mouse.get_pressed()[0]:
                    if not button1.clicked:
                        button1.clicked = True
                        button1.clicked = False
                        _SCENE.Pause()        
                else: 
                    button1.clicked = False

                # Button : Howmany Button
                if button2.rect.collidepoint(button2.pos) and pygame.mouse.get_pressed()[0]:
                    if not button2.clicked:
                        button2.clicked = True
                        _SCENE.TriggerClick *= -1
                        button2.clicked = False
                else:
                    button2.clicked = False

                # Button : Speed Up
                if button3.rect.collidepoint(button3.pos) and pygame.mouse.get_pressed()[0]:
                    if not button3.clicked:
                        button3.clicked = True
                        button3.clicked = False
                        _STAGE_MANAGER.GetObjectMultSpeedValue(True)
                else:
                    button3.clicked = False

                # Button : Speed Down
                if button4.rect.collidepoint(button4.pos) and pygame.mouse.get_pressed()[0]:
                    if not button4.clicked:
                        button4.clicked = True
                        button4.clicked = False
                        _STAGE_MANAGER.GetObjectMultSpeedValue(False)
                else:
                    button2.clicked = False

            # Start Game By Press 'z'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z and _SCENE.PressKeyLogo == -1:
                    _STAGE_MANAGER.ObjectSpawnerPaper.OnMoveFlag()
                    _STAGE_MANAGER.ObjectSpawnerRock.OnMoveFlag()
                    _STAGE_MANAGER.ObjectSpawnerScissors.OnMoveFlag()
                    _SCENE.PressKeyLogo *= -1
    # -------------------------------------

    # --- CheckEvent For Scene : Pause
    def CheckEvent_Pause(self, button1, button3): # button1 : 'Back To Game', button2 : 'Option_', button3 : 'Quit To Title'
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                _SCENE.exiter = True
                _SCENE.Exit()

            # Button Click Event
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Button : Back To Game
                if button1.rect.collidepoint(button1.pos) and pygame.mouse.get_pressed()[0]:
                    if not button1.clicked:
                        button1.clicked = True
                        _SOUND_MANAGER.PlaySound('SOUND_CLICK')
                        button1.clicked = False
                        _LOG._CONFIG['Count_Play'] -= 1
                        _SCENE.FirstPlayed = True
                        _SCENE.Playground()
                        
                else: 
                    button1.clicked = False

                # Button : Quit To Title
                if button3.rect.collidepoint(button3.pos) and pygame.mouse.get_pressed()[0]:
                    if not button3.clicked:
                        button3.clicked = True
                        _SOUND_MANAGER.PlaySound('SOUND_CLICK')
                        _MUSIC_MANAGER.StopMusic(_SCENE.CurrentMusic)
                        button3.clicked = False

                        # Initiate Game State
                        _SCENE.BackgroundRandomIndex = random.randint(0, 11)
                        _SCENE.PressKeyLogo = -1
                        _SCENE.TriggerClick = -1
                        _SCENE.Trigger = False
                        _SCENE.Trigger2 = False 
                        _STAGE_MANAGER.ResetGame()

                        # Back to Menu
                        _SCENE.MainMenu()
                        
                else: 
                    button1.clicked = False
    # -------------------------------------

    def Render(self):
        pygame.display.update()
        _CONSTANT.CLOCK.tick(_CONSTANT.FPS)


class Scene:
    def __init__(self):
        pygame.init()

        # Exit
        self.exiter = False

        # Background
        # --------------------- Main Menu
        self.mainMenuBackground = MAIN_MENU
        self.mainMenuBackgroundPosX = random.randint(-1500, 0)
        # -------------------------------

        # --------------------- Choosing Menu
        self.chooseMenuBackground = CHOOSE_MENU
        # -------------------------------

        # --------------------- Option
        self.BackToGame = False
        self.MouseHoverSoundPlayed = False
        self.OptionBackground = CHOOSE_MENU
        # -------------------------------

        # --------------------- Advanced
        self.AdvanceBackground = CHOOSE_MENU

        # --------------------- Statistics
        self.StatisticsBackground = CHOOSE_MENU
        self.UI_DIARY = G_UI[4]
        # -------------------------------

        # --------------------- Playground
        self.FirstPlayed = True
        self.ConfirmImage = G_BUTTON[18][0]
        self.ConfirmImage.set_alpha(40)
        self.GameOverProcessed = False
        self.MusicBox = ['MUSIC_BG_1', 'MUSIC_BG_2', 'MUSIC_BG_3', 'MUSIC_BG_4', 'MUSIC_BG_5', 'MUSIC_BG_6', 'MUSIC_BG_7', 'MUSIC_BG_8']
        self.CurrentMusic = random.choice(self.MusicBox)

        self.BackgroundRandomIndex = random.randint(0, 11)
        self.PressKeyLogo = -1
        self.TriggerClick = -1
        self.Trigger = False # For 'Howmany'
        self.Trigger2 = False # For 'Speed'

        self._SCISSOR_ICO = G_UI[8]
        self._SCISSOR_ICO.set_alpha(100)
        self._ROCK_ICO = G_UI[7]
        self._ROCK_ICO.set_alpha(100)
        self._PAPER_ICO = G_UI[6]
        self._PAPER_ICO.set_alpha(100)
        # -------------------------------

    def Exit(self): 
        if self.exiter:
            try:
                _MUSIC_MANAGER.Quit()
                _SOUND_MANAGER.Quit()
                pygame.quit()
                sys.exit()
            except Exception as e:
                print(f"Err Log : {e}")
                pygame.quit()
                sys.exit()

    def MainMenu(self):
        self.CurrentMusic = random.choice(self.MusicBox)
        while True:

            # Get Event
            _RUNGAME.CheckEvent_MainMenu(_BUTTON._PLAY, _BUTTON._OPTION, _BUTTON._QUIT)

            # Background and Window Settings
            _CONSTANT.SCREEN.blit(self.mainMenuBackground, (self.mainMenuBackgroundPosX, 0))

            # Blit Logo
            _TEXT._MAINMENU_LOGO_1.renderString(_CONSTANT.SCREEN)
            _TEXT._MAINMENU_LOGO_2.renderString(_CONSTANT.SCREEN)
            _TEXT._MAINMENU_LOGO_3.renderString(_CONSTANT.SCREEN)

            # Buttons
            _BUTTON._PLAY.Update()
            _BUTTON._OPTION.Update()
            _BUTTON._QUIT.Update()

            # Update Sound
            SoundManagerUpdate()

            # Update Window
            _RUNGAME.Render()

    def ChooseRockScissorPaper(self):
        while True:

            # Get Event
            _RUNGAME.CheckEvent_ChooseRockScissorPaper(_BUTTON._BACK_2, _BUTTON._SCISSORS, _BUTTON._ROCK, _BUTTON._PAPER, _BUTTON._RANDOM)

            # Background and Window Settings
            _CONSTANT.SCREEN.blit(self.chooseMenuBackground, (_CONSTANT.BACKGROUND_POSITION))

            # Blit Logo
            _TEXT._CHOOSEMENU_LOGO_1.renderString(_CONSTANT.SCREEN)
            _TEXT._CHOOSEMENU_LOGO_2.renderString(_CONSTANT.SCREEN)

            # Buttons
            _BUTTON._BACK_2.Update()
            _BUTTON._SCISSORS.Update()
            _BUTTON._ROCK.Update()
            _BUTTON._PAPER.Update()
            _BUTTON._RANDOM.Update()

            # Buttons Text
            CHOOSE_NAME_SCISSORS = RenderText(113, 280, 24, 'white', 'black', 3, _BUTTON._SCISSORS.Hovered, 'Center', 'Scissors')
            CHOOSE_NAME_ROCK = RenderText(307, 280, 24, 'white', 'black', 3, _BUTTON._ROCK.Hovered, 'Center', 'Rock')
            CHOOSE_NAME_PAPER = RenderText(113, 474, 24, 'white', 'black', 3, _BUTTON._PAPER.Hovered, 'Center', 'Paper')
            CHOOSE_NAME_RANDOM = RenderText(307, 474, 24, 'white', 'black', 3, _BUTTON._RANDOM.Hovered, 'Center', 'Random')

            CHOOSE_NAME_SCISSORS.renderString(_CONSTANT.SCREEN)
            CHOOSE_NAME_ROCK .renderString(_CONSTANT.SCREEN)
            CHOOSE_NAME_PAPER.renderString(_CONSTANT.SCREEN)
            CHOOSE_NAME_RANDOM.renderString(_CONSTANT.SCREEN)

            # Update Sound
            SoundManagerUpdate()

            # Update Window
            _RUNGAME.Render()

    def Option(self):
        while True:

            # Get Event
            _RUNGAME.CheckEvent_Option(_BUTTON._BACK_1, _BUTTON._STATISTICS, _BUTTON._RESET, _BUTTON._OPTION_BAR, _BUTTON._OPTION_SOUNDCHECKER, _BUTTON._OPTION_ADVANCE)

            # Background and Window Settings
            _CONSTANT.SCREEN.blit(self.OptionBackground, (_CONSTANT.BACKGROUND_POSITION))

            # Buttons
            _BUTTON._STATISTICS.Update()
            _BUTTON._OPTION_ADVANCE.Update()
            _BUTTON._BACK_1.Update()
            _BUTTON._RESET.Update()
            _BUTTON._OPTION_BAR.Update()

            # Blit Logo
            _TEXT._OPTION_LOGO_1.renderString(_CONSTANT.SCREEN)
            _TEXT._OPTION_LOGO_2.renderString(_CONSTANT.SCREEN)
            _TEXT._OPTION_LOGO_3.renderString(_CONSTANT.SCREEN)
            
            if _BUTTON._RESET.state == 1:
                _TEXT._OPTION_LOGO_WARNING_1.renderString(_CONSTANT.SCREEN)
                _TEXT._OPTION_LOGO_WARNING_2.renderString(_CONSTANT.SCREEN)
                _TEXT._OPTION_LOGO_WARNING_3.renderString(_CONSTANT.SCREEN)

            else:
                _TEXT._OPTION_LOGO_4.renderString(_CONSTANT.SCREEN)
                _BUTTON._OPTION_SOUNDCHECKER.Update()

            # Blit Volume Rate
            OPTION_LOGO_VOLUME_VALUE_1 = RenderText(210, 235, 20, 'white', 'white', 0, 255, 'Center', f"{_BUTTON._OPTION_BAR.volumeRate}%")
            OPTION_LOGO_VOLUME_VALUE_2 = RenderText(210, 235, 20, 'white', 'white', 0, 100, 'Center', "Mute")
            if _BUTTON._OPTION_BAR.rect.x > 60: OPTION_LOGO_VOLUME_VALUE_1.renderString(_CONSTANT.SCREEN)
            else : OPTION_LOGO_VOLUME_VALUE_2.renderString(_CONSTANT.SCREEN)

            # Update Sound
            SoundManagerUpdate()

            # Update Option
            _LOG.SaveConfig()

            # Update Window
            _RUNGAME.Render()

    def Advance(self):
        while True:

            # Get Event
            _RUNGAME.CheckEvent_Advance(_BUTTON._BACK_5, _BUTTON._ADVANCE_MAX_BAR, _BUTTON._ADVANCE_MIN_BAR)

            # Background and Window Settings
            _CONSTANT.SCREEN.blit(self.AdvanceBackground, (_CONSTANT.BACKGROUND_POSITION))

            # Buttons
            _BUTTON._BACK_5.Update()
            _BUTTON._ADVANCE_MAX_BAR.Update()
            _BUTTON._ADVANCE_MIN_BAR.Update()

            # Blit Logo
            _TEXT._ADVANCE_LOGO_1.renderString(_CONSTANT.SCREEN)
            _TEXT._ADVANCE_LOGO_2.renderString(_CONSTANT.SCREEN)
            _TEXT._ADVANCE_LOGO_3.renderString(_CONSTANT.SCREEN)
            MAX_RANGE_VALUE = RenderText(210, 235, 20, 'white', 'white', 0, 255, 'Center', f"{_LOG._CONFIG['max_value']}")
            MIN_RANGE_VALUE = RenderText(210, 395, 20, 'white', 'white', 0, 255, 'Center', f"{_LOG._CONFIG['min_value']}")
            MAX_RANGE_VALUE.renderString(_CONSTANT.SCREEN)
            MIN_RANGE_VALUE.renderString(_CONSTANT.SCREEN)

            if _LOG._CONFIG['max_value'] < _LOG._CONFIG['min_value']:
                _TEXT._ADVANCE_LOGO_WARNING_1.renderString(_CONSTANT.SCREEN)
                _TEXT._ADVANCE_LOGO_WARNING_2.renderString(_CONSTANT.SCREEN)
                _TEXT._ADVANCE_LOGO_WARNING_3.renderString(_CONSTANT.SCREEN)
                _TEXT._ADVANCE_LOGO_WARNING_4.renderString(_CONSTANT.SCREEN)

            # Update Sound
            SoundManagerUpdate()

            # Update Config
            _LOG.SaveConfig()

            # Update Window
            _RUNGAME.Render()

    def Statics(self):
        while True:

            _TEXT.CalculateWinRate()

            # Get Event
            _RUNGAME.CheckEvent_Statistics(_BUTTON._BACK_3)

            # Background and Window Settings
            _CONSTANT.SCREEN.blit(self.StatisticsBackground, _CONSTANT.BACKGROUND_POSITION)

            # Blit UI
            _CONSTANT.SCREEN.blit(self.UI_DIARY, (20, 126))

            # Blit Logo
            _TEXT._STATISTICS_LOGO_1.renderString(_CONSTANT.SCREEN)
            _TEXT._STATISTICS_LOGO_2.renderString(_CONSTANT.SCREEN)
            _TEXT._STATISTICS_LOGO_3.renderString(_CONSTANT.SCREEN)
            _TEXT._STATISTICS_LOGO_4.renderString(_CONSTANT.SCREEN)

            STATISTICS_LOGO_WIN = RenderText(360, 230, 30, 'Green', 'black', 3, 255, 'Right', f"{_LOG._CONFIG['Count_Win']}")
            STATISTICS_LOGO_LOSE = RenderText(360, 330, 30, 'Red', 'black', 3, 255, 'Right', f"{_LOG._CONFIG['Count_Lose']}")
            STATISTICS_LOGO_RATE = RenderText(210, 480, 60, 'White', 'black', 3, 255, 'Center', f"{_TEXT.CalculateWinRate()}%")

            STATISTICS_LOGO_WIN.renderString(_CONSTANT.SCREEN)
            STATISTICS_LOGO_LOSE.renderString(_CONSTANT.SCREEN)
            STATISTICS_LOGO_RATE.renderString(_CONSTANT.SCREEN)

            # Buttons
            _BUTTON._BACK_3.Update()

            # Update Sound
            SoundManagerUpdate()

            # Update Config
            _LOG.SaveConfig()

            # Update Window
            _RUNGAME.Render()

    def Playground(self):
        if self.FirstPlayed:
            _STAGE_MANAGER.GenerateStage()
            _MUSIC_MANAGER.PlayMusic(self.CurrentMusic)
            self.FirstPlayed = False
        else:
            _STAGE_MANAGER.ResetGame()
            _MUSIC_MANAGER.PlayMusic(self.CurrentMusic)

        PreviousTime = time.time()

        while True:
            DeltaTime = time.time() - PreviousTime
            PreviousTime = time.time()

            # Get Event
            _RUNGAME.CheckEvent_Playground(_BUTTON._PLAYGROUND_OPTION, _BUTTON._PLAYGROUND_HOWMANY, _BUTTON._PLAYGROUND_SPEED_UP, _BUTTON._PLAYGROUND_SPEED_DOWN,\
                                           _BUTTON._PLAYGROUND_REROLL)

            # Blit Background
            _CONSTANT.SCREEN.blit(G_BACKGROUND[self.BackgroundRandomIndex], _CONSTANT.BACKGROUND_POSITION)

            # Update Game Objects
            ObjectGroup.draw(_CONSTANT.SCREEN)
            ObjectGroup.update(DeltaTime)

            # Blit Buttons
            _BUTTON._PLAYGROUND_OPTION.Update()
            _BUTTON._PLAYGROUND_HOWMANY.Update()
            _BUTTON._PLAYGROUND_SPEED_UP.Update()
            _BUTTON._PLAYGROUND_SPEED_DOWN.Update()
            _BUTTON._PLAYGROUND_REROLL.Update()

            # Blit Computer's Prediction
            if _STAGE_MANAGER.ComputerSelect == 0:
                _CONSTANT.SCREEN.blit(self._SCISSOR_ICO , (5, 5))
            elif _STAGE_MANAGER.ComputerSelect == 1:
                _CONSTANT.SCREEN.blit(self._ROCK_ICO, (5, 5))
            elif _STAGE_MANAGER.ComputerSelect == 2:
                _CONSTANT.SCREEN.blit(self._PAPER_ICO, (5, 5))

            # Blit Object : Current Speed
            if self.Trigger2:
                CURRENT_SPEED = RenderText(130, 665, 40, 'white', 'black', 3, 100, 'Center', f"x{_STAGE_MANAGER.ObjectMultSpeed}")
                CURRENT_SPEED.renderString(_CONSTANT.SCREEN)

            # Blit Object : Howmany
            if self.Trigger or self.TriggerClick == 1:
                HOWMANY_ROCKS = RenderText(400, 550, 40, 'white', 'black', 3, 255, 'Right', f"{_STAGE_MANAGER.ObjectSpawnerRock.thisObjectCount}")
                HOWMANY_PAPAERS = RenderText(400, 610, 40, 'white', 'black', 3, 255, 'Right', f"{_STAGE_MANAGER.ObjectSpawnerPaper.thisObjectCount}")
                HOWMANY_SCISSORS = RenderText(400, 670, 40, 'white', 'black', 3, 255, 'Right', f"{_STAGE_MANAGER.ObjectSpawnerScissors.thisObjectCount}")
                ICON_ROCK = G_UI[0]
                ICON_PAPER = G_UI[1]
                ICON_SCISSORS = G_UI[2]
                ICON_ROCK.set_alpha(255)
                ICON_PAPER.set_alpha(255)
                ICON_SCISSORS.set_alpha(255)

                HOWMANY_ROCKS.renderString(_CONSTANT.SCREEN)
                HOWMANY_PAPAERS.renderString(_CONSTANT.SCREEN)
                HOWMANY_SCISSORS.renderString(_CONSTANT.SCREEN)

                _CONSTANT.SCREEN.blit(ICON_ROCK, (255, 530))
                _CONSTANT.SCREEN.blit(ICON_PAPER, (255, 593))
                _CONSTANT.SCREEN.blit(ICON_SCISSORS, (255, 652))

                # Blit Player's Prediction
                if _STAGE_MANAGER.PlayerSelect == 0:
                    _CONSTANT.SCREEN.blit(self._SCISSOR_ICO , (331, 461))
                elif _STAGE_MANAGER.PlayerSelect == 1:
                    _CONSTANT.SCREEN.blit(self._ROCK_ICO, (331, 461))
                elif _STAGE_MANAGER.PlayerSelect == 2:
                    _CONSTANT.SCREEN.blit(self._PAPER_ICO, (331, 461))

            # Blit Press Key Logo
            if self.PressKeyLogo == -1 and not _STAGE_MANAGER.GameOverFlag:
                _TEXT._PLAYGROUND_LOGO_1.renderString(_CONSTANT.SCREEN)
                _TEXT._PLAYGROUND_LOGO_2.renderString(_CONSTANT.SCREEN)
                _TEXT._PLAYGROUND_LOGO_3.renderString(_CONSTANT.SCREEN)

            # Judge Winner
            _STAGE_MANAGER.PrintWinner()
            if _STAGE_MANAGER.GameOverFlag:
                # Handle Game Over
                if not self.GameOverProcessed:
                    if _STAGE_MANAGER.WhoIsWinner == 0:
                        _LOG._CONFIG['Count_Lose'] += 1
                    elif _STAGE_MANAGER.WhoIsWinner == 1:
                        _LOG._CONFIG['Count_Win'] += 1
                    elif _STAGE_MANAGER.WhoIsWinner == 2:
                        _LOG._CONFIG['Count_Draw'] += 1

                    _LOG.SaveConfig()
                    self.GameOverProcessed = True

                # Render Winner Logo
                if _STAGE_MANAGER.WhoIsWinner == 0:
                    _TEXT._PLAYGROUND_LOGO_WINNER_C.renderString(_CONSTANT.SCREEN)
                    _TEXT._PLAYGROUND_LOGO_WINNER_1.renderString(_CONSTANT.SCREEN)

                elif _STAGE_MANAGER.WhoIsWinner == 1:
                    _TEXT._PLAYGROUND_LOGO_WINNER_P.renderString(_CONSTANT.SCREEN)
                    _TEXT._PLAYGROUND_LOGO_WINNER_1.renderString(_CONSTANT.SCREEN)

                elif _STAGE_MANAGER.WhoIsWinner == 2:
                    _TEXT._PLAYGROUND_LOGO_WINNER_2.renderString(_CONSTANT.SCREEN)

            # Update Sound
            SoundManagerUpdate()

            # # Update Config : Play, Win, Lose Count
            # _LOG.SaveConfig()
 
            # Update Window
            _RUNGAME.Render()

    def Pause(self):
        while True:

            # Get Event
            _RUNGAME.CheckEvent_Pause(_BUTTON._PAUSE_BACKTOGAME, _BUTTON._PAUSE_QUITTOTITLE)

            # Blit UI
            _CONSTANT.SCREEN.blit(G_UI[5], (5, 225))

            # Blit Buttons
            _BUTTON._PAUSE_BACKTOGAME.Update()
            _BUTTON._PAUSE_QUITTOTITLE.Update()

            # Update Sound
            SoundManagerUpdate()

            # Update Config
            _LOG.SaveConfig()

            # Update Window
            _RUNGAME.Render()

    


# Scene Manager and Rungame Class
_RUNGAME = GameRunner()
_SCENE = Scene()
