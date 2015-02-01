import GraphicsHelper
import pygame
import random

class CarHandler:

    #Creates all the sprites and initializes all controller variables.
    def __init__(self, main):
        #Creates the list and tuple that contains the car sprites and traffic sprites respectively.
        self.carGroup = []
        self.trafficLights = ()
        #Time relevant variables which are used to track time, and by extension execute events after a certain amount of time.
        self.time = 0
        self.checkInterval = 0
        #Max number of cars on the screen
        self.maxCars = 15
        self.speed = 1.5
        #Amount of mistakes the uer can make
        self.chances = 3
        #Creates all the traffic light sprites.
        self.createTrafficLights()
        #These are textures (not sprites) used for the game.
        self.background = GraphicsHelper.GraphicsHelper.getImage("Resources/screen.bmp")
        self.retryButton = GraphicsHelper.retryButton("Resources/retrybutton.bmp", (400, 500))
        #Initialization of fonts that are used in the game.
        font = pygame.font.Font("Resources/OptimusPrinceps.ttf", 72)
        font2 = pygame.font.Font("Resources/OptimusPrinceps.ttf", 36)
        self.loseGame = font.render("You Lost", 1, (255, 0, 0))
        self.retry = font2.render("Retry?", 1, (0, 255, 0))
        #Boolean which detects whether the game should be running, or show the lose screen.
        self.lost = False
        #Main class used purely for switching rendering between the game itself and the lose screen.
        self.main = main

    def getBackground(self):
        return self.background

    #Creates the traffic light sprites.
    def createTrafficLights(self):
        image = "Resources/light.bmp"
        #Creates a traffic light with the image from the resources folder. The Tuple is the position of the sprite.
        light = GraphicsHelper.trafficSprite(image, (89, 89))
        self.trafficLights += (light,)
        light = GraphicsHelper.trafficSprite(image, (211, 89))
        self.trafficLights += (light,)
        light = GraphicsHelper.trafficSprite(image, (341, 89))
        self.trafficLights += (light,)
        light = GraphicsHelper.trafficSprite(image, (463, 89))
        self.trafficLights += (light,)
        light = GraphicsHelper.trafficSprite(image, (591, 89))
        self.trafficLights += (light,)
        light = GraphicsHelper.trafficSprite(image, (713, 89))
        self.trafficLights += (light,)

        light = GraphicsHelper.trafficSprite(image, (89, 209))
        self.trafficLights += (light,)
        light = GraphicsHelper.trafficSprite(image, (211, 209))
        self.trafficLights += (light,)
        light = GraphicsHelper.trafficSprite(image, (341, 209))
        self.trafficLights += (light,)
        light = GraphicsHelper.trafficSprite(image, (463, 209))
        self.trafficLights += (light,)
        light = GraphicsHelper.trafficSprite(image, (591, 209))
        self.trafficLights += (light,)
        light = GraphicsHelper.trafficSprite(image, (713, 209))
        self.trafficLights += (light,)

        light = GraphicsHelper.trafficSprite(image, (89, 391))
        self.trafficLights += (light,)
        light = GraphicsHelper.trafficSprite(image, (211, 391))
        self.trafficLights += (light,)
        light = GraphicsHelper.trafficSprite(image, (341, 391))
        self.trafficLights += (light,)
        light = GraphicsHelper.trafficSprite(image, (463, 391))
        self.trafficLights += (light,)
        light = GraphicsHelper.trafficSprite(image, (591, 391))
        self.trafficLights += (light,)
        light = GraphicsHelper.trafficSprite(image, (713, 391))
        self.trafficLights += (light,)

        light = GraphicsHelper.trafficSprite(image, (89, 511))
        self.trafficLights += (light,)
        light = GraphicsHelper.trafficSprite(image, (211, 511))
        self.trafficLights += (light,)
        light = GraphicsHelper.trafficSprite(image, (341, 511))
        self.trafficLights += (light,)
        light = GraphicsHelper.trafficSprite(image, (463, 511))
        self.trafficLights += (light,)
        light = GraphicsHelper.trafficSprite(image, (591, 511))
        self.trafficLights += (light,)
        light = GraphicsHelper.trafficSprite(image, (713, 511))
        self.trafficLights += (light,)

    #Returns all the sprite necessary for rendering, depending on the state of the game.
    def getSprites(self):
        if not self.lost:
            #Game is still running.
            return pygame.sprite.RenderPlain((self.carGroup, self.trafficLights))
        else:
            #Game is lost.
            return pygame.sprite.RenderPlain(self.retryButton)

    #If a mistake is made, flashes the screen red.
    def flashScreen(self):
        #Texture that is the flash on the screen is set to the background.
        self.background = GraphicsHelper.GraphicsHelper.getImage("Resources/mistake.bmp")
        oldTime = pygame.time.get_ticks()
        #Delays the reset of the background so it appears as a flash.
        self.main.delayResetBackground()

    #Set the background back to normal.
    def resetBackground(self):
        if self.chances > 0:
            #If the user still has some chances left.
            self.background = GraphicsHelper.GraphicsHelper.getImage("Resources/screen.bmp")
        else:
            #If the user has no chances left, the game recognizes the user has lost.
            self.lost = True
            self.background = GraphicsHelper.GraphicsHelper.getImage("Resources/losegamescreen.bmp")


    #Updates the game.
    def update(self, deltaTime):
        #Increase the time by the period that has elasped since the last update so that the current time is obtained.
        self.time += deltaTime
        self.checkInterval += deltaTime
        #If the user has not lost, all the sprites are updated and routinely checked.
        if not self.lost:
            self.checkAdd()
            self.checkDelete()
            self.checkStop()
            self.checkCollision()

    #Based on how much time has passed, the game checks whether to add a new car sprite.
    def checkAdd(self):
        if self.checkInterval / 1000 > 1 and len(self.carGroup) < self.maxCars:
            #Resets the interval so an additional one second is required to start the next check.
            self.checkInterval = 0
            #Gets a random direction to set the car in.
            direction = self.getRandomDirection()
            #Creates a new car with a set speed, image, a random color, and a random location based off the direction.
            car = GraphicsHelper.carSprite("Resources/car.bmp", self.speed, direction, self.getRandomColor(), self.getLocation(direction))
            #Adds the car to the rendering group.
            self.carGroup.append(car)

    #Checks whether a car should be deleted.
    def checkDelete(self):
        for car in self.carGroup:
            #These two if statements check whether the car is out of bounds of the screen (outside of it).
            if car.position[0] > 800 or car.position[0] < 0:
                self.carGroup.remove(car)
            if car.position[1] > 600 or car.position[1] < 0:
                self.carGroup.remove(car)
            #This if statement checks that if a car has stayed in the screen for more than 15 seconds, the car is deleted. This
            #is to ensure that the user cannot simply indefinitely stop a car. This is counted as a mistake.
            if (car.getTime() / 1000 > 15):
                self.carGroup.remove(car)
                self.chances -= 1
                self.flashScreen()

    #Checks whether the car should stop at a stop sign, or whether the car should stop because a car in front of it on the same
    #lane has stopped.
    def checkStop(self):
        for car in self.carGroup:
            if not car.checkCarStop(self.carGroup):
                car.checkTrafficLightStops(self.trafficLights)

    #Checks whether a sprites bounds contains another, and if so, deletes that sprite and removes a chance.
    def checkCollision(self):
        group = pygame.sprite.RenderPlain(self.carGroup)
        for car in self.carGroup:
            group.remove(car)
            if pygame.sprite.spritecollide(car, group, True):
                self.carGroup.remove(car)
                self.chances -= 1
                self.flashScreen()

    #Checks whether a sprite contains a mouse click.
    def checkClicked(self, mPos):
        for light in self.trafficLights:
            #For the traffic light.
            light.detectChange(mPos)
        if self.retryButton.detectMouse(mPos) and self.lost:
            #For the retry button.
            self.main.restartGame()

    #Checks whether the user is hovering over the button, so that it is highlighted while he/she is doing so.
    def checkHover(self, mPos):
        if self.retryButton.detectMouse(mPos) and self.lost:
            #Highlights the button.
            self.retryButton = GraphicsHelper.retryButton("Resources/retrybuttonhighlighted.bmp", (400, 500))
        else:
            #Unhighlights the button
            self.retryButton = GraphicsHelper.retryButton("Resources/retrybutton.bmp", (400, 500))

    def getRandomColor(self):
        #Creates a random color by getting three random color elements from 0 to 255.
        red = random.randint(0, 255)
        blue = random.randint(0, 255)
        green = random.randint(0, 255)
        color = pygame.Color(red)
        color.r = red
        color.g = green
        color.b = blue
        return color

    def getRandomDirection(self):
        return random.randint(0, 3)

    #Based on the direction, creates a location.
    def getLocation(self, direction):
        #Since each direction has different locations, creates the range of randomness based on the direction.
        if (direction < 2):
            position = random.randint(0, 1)
        else:
            position = random.randint(0, 2)

        if direction == 0:
            #Right, on the top lane.
            if position == 0:
                return 0, 175
            if position == 1:
            #Right, on the bottom lane.
                return 0, 475
        if direction == 1:
            if position == 0:
                return 800, 125
            if position == 1:
                return 800, 425
        if direction == 2:
            if position == 0:
                return 125, 0
            if position == 1:
                return 375, 0
            if position == 2:
                return 625, 0
        if direction == 3:
            if position == 0:
                return 175, 600
            if position == 1:
                return 425, 600
            if position == 2:
                return 675, 600