import pygame
import CarHandler

#Class responsible for the drawing and periodic updating of sprites
class Main():
    #DELAY is the unique ID necessary to poll the reset background event.
    DELAY = 20

    def __init__(self):
        #Creates the objects necessary for running the game
        pygame.init()
        #Canvas where the sprites and the background are drawn
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Traffic Director")
        #This clock sets the frames per second at which the game runs
        self.clock = pygame.time.Clock()
        #This object handles the creation of every sprite.
        self.handler = CarHandler.CarHandler(self)
        #This boolean is what keeps the program running. When set to true, the program halts.
        self.closed = False
        self.FPS = 60
        #Starts the loop that runs the program.
        self.runGame()

    def runGame(self):
        #This while loop is what runs the game, and only stops when the program is closed by the user.
        while not self.closed:
            #Gets the time in between the ticks of the clock, which should roughly be 1/60th of a second.
            deltaTime = self.clock.tick(self.FPS)
            #Polls the game for events, such as mouse movement or clicks.
            for event in pygame.event.get():
                #Polls to see if the user has closed the game.
                if event.type == pygame.QUIT:
                    self.closed = True
                #Polls to see if the user has clicked the mouse.
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handler.checkClicked(pygame.mouse.get_pos())
                #Polls to see if the user has moved the mouse.
                elif event.type == pygame.MOUSEMOTION:
                    self.handler.checkHover(pygame.mouse.get_pos())
                #Polls to see if the program should reset the background
                elif event.type == self.DELAY:
                    self.handler.resetBackground()

            #Clears the screen, to draw NEW sprites. If the screen is not cleared, old images will remain, clogging the screen.
            self.screen.fill((0, 0, 0))
            #Updates all the sprites.
            self.handler.update(deltaTime)
            #Creates the background
            background = self.handler.getBackground()
            #Creates the group of sprites.
            group = self.handler.getSprites()
            #Draws the background.
            self.screen.blit(background, background.get_rect())
            #Draws and updates the sprites.
            group.update(deltaTime)
            group.draw(self.screen)
            #Checks to see whether to display the lose grame.
            if self.handler.lost:
                self.showLoseScreen()
            pygame.display.update()

        #CLoses the program
        pygame.quit()
        quit()

    #Deletes the current sprite storage class and creates another, effectively restarting the program.
    def restartGame(self):
        del self.handler
        self.handler = CarHandler.CarHandler(self)

    #Displays all objects relevant to the lose screen.
    def showLoseScreen(self):
        self.screen.blit(self.handler.loseGame, (260, 200))
        self.screen.blit(self.handler.retry, (345, 480))

    #Delays the resetting of the background after the screen flash is set to the background to emulate a screen flash.
    def delayResetBackground(self):
        pygame.time.set_timer(self.DELAY, 200)

#Begins the program.
Main()