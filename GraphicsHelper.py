#Class intended to return the pygame surface from the image path. Essentially converts the string path into an image the
#library can use.
import pygame

class GraphicsHelper:
    @staticmethod
    #Static method that obtains the actual image from the string path.
    def getImage(path):
        image = pygame.image.load(path)
        return image

#Car class
class carSprite(pygame.sprite.Sprite):
    def __init__(self, image, speed, direction, color, (posX, posY)):
        pygame.sprite.Sprite.__init__(self)

        #Rotates the image based on the direction of the car.
        if direction > 1:
            #Rotates the car 90 degrees if the car is going up or down. Otherwise leaves it be.
            self.image = pygame.transform.rotate(GraphicsHelper.getImage(image), 90)
        else:
            self.image = GraphicsHelper.getImage(image)

        #Sets the color of the sprite by filling the image.
        self.image.fill(color)
        #Sets the rect of the sprite, which is where the image is drawn.
        self.rect = self.image.get_rect()
        #Sets the position of the sprite itself.
        self.position = (posX, posY)
        #Sets the speed and the direction. The time is also set to zero, and sets the car to be moving.
        self.speed = speed
        self.direction = direction
        self.time = 0
        self.moving = True

    #Moves the sprite, and then updates the location of the image.
    def update(self, deltaTime):
        if self.moving:
            self.move()
        self.rect.center = self.position
        self.time += deltaTime

    def getTime(self):
        return self.time

    def move(self):
        #Sets the position of the sprite based on direction.
        posX, posY = self.position
        #Sets the x-component of the position vector.
        if self.direction == 0:
            posX += self.speed
        elif self.direction == 1:
            posX -= self.speed
        #Sets the y-component of the position vector.
        elif self.direction == 2:
            posY += self.speed
        elif self.direction == 3:
            posY -= self.speed

        #Sets the new position.
        self.position = posX, posY

    #Checks if a traffic light corresponding to the car's lane is red, and stops the car if so.
    def checkTrafficLightStops(self, lights):
        hasStopped = False
        #Creates the components of the position vector.
        posX = self.position[0]
        posY = self.position[1]

        #Checks for red traffic lights based on the direction.
        if self.direction == 0:
            #Chooses the corresponding traffic light based on the lane of the car.
            if posY == 175:
                #Checks for traffic lights based on the fact that the car is on the top lane and is moving right.
                hasStopped = self.checkStop(0, lights)
            else:
                #Otherwise the car is on the bottom lane, and checks accordingly.
                hasStopped = self.checkStop(1, lights)
        if self.direction == 1:
            if posY == 125:
                hasStopped = self.checkStop(2, lights)
            else:
                hasStopped = self.checkStop(3, lights)
        if self.direction == 2:
            if posX == 125:
                hasStopped = self.checkStop(4, lights)
            elif posX == 375:
                hasStopped = self.checkStop(5, lights)
            else:
                hasStopped = self.checkStop(6, lights)
        if self.direction == 3:
            if posX == 175:
                hasStopped = self.checkStop(7, lights)
            elif posX == 425:
                hasStopped = self.checkStop(8, lights)
            else:
                hasStopped = self.checkStop(9, lights)

        #If the car has NOT stopped, the car is set to move.
        if not hasStopped:
            self.moving = True

    #A more complicated method that checks whether a traffic light on a lane is within certain distance of the car.
    def checkStop(self, type, lights):
        posX = self.position[0]
        posY = self.position[1]
        for light in lights:
            if not light.go:
                #Sets the components of the light position.
                lPosX = light.position[0]
                lPosY = light.position[1]
                #The type in this method is actually the integer that corresponds to the lane AND the direction of the car.
                if type == 0:
                    #Top lane, right direction. Thus, the traffic light position must be on the lane.
                    if lPosY == 209 and (lPosX == 89 or lPosX == 341 or lPosX == 591) and lPosX - posX < 10 and posX < lPosX:
                        #Checks if the traffic lights on this lane are within a certain distance of the car. The car must also
                        #be behind the traffic light, not in front.
                        self.moving = False
                        return True
                if type == 1:
                    if lPosY == 511 and (lPosX == 89 or lPosX == 341 or lPosX == 591) and lPosX - posX < 10 and posX < lPosX:
                        self.moving = False
                        return True
                if type == 2:
                    if lPosY == 89 and (lPosX == 211 or lPosX == 463 or lPosX == 713) and posX - lPosX < 10 and posX > lPosX:
                        self.moving = False
                        return True
                if type == 3:
                    if lPosY == 391 and (lPosX == 211 or lPosX == 463 or lPosX == 713) and posX - lPosX < 10 and posX > lPosX:
                        self.moving = False
                        return True
                if type == 4:
                    if lPosX == 89 and (lPosY == 89 or lPosY == 391) and lPosY - posY < 10 and posY < lPosY:
                        self.moving = False
                        return True
                if type == 5:
                    if lPosX == 341 and (lPosY == 89 or lPosY == 391) and lPosY - posY < 10 and posY < lPosY:
                        self.moving = False
                        return True
                if type == 6:
                    if lPosX == 591 and (lPosY == 89 or lPosY == 391) and lPosY - posY < 10 and posY < lPosY:
                        self.moving = False
                        return True
                if type == 7:
                    if lPosX == 211 and (lPosY == 209 or lPosY == 511) and posY - lPosY < 10 and posY > lPosY:
                        self.moving = False
                        return True
                if type == 8:
                    if lPosX == 463 and (lPosY == 209 or lPosY == 511) and posY - lPosY < 10 and posY > lPosY:
                        self.moving = False
                        return True
                if type == 9:
                    if lPosX == 713 and (lPosY == 209 or lPosY == 511) and posY - lPosY < 10 and posY > lPosY:
                        self.moving = False
                        return True
        return False

    #Checks if a car is stopped in front of this car.
    def checkCarStop(self, carGroup):
        posX = self.position[0]
        posY = self.position[1]

        for car in carGroup:
            #Car position broken down into components.
            cPosX = car.position[0]
            cPosY = car.position[1]
            #Checks if the car is within the same lane, not moving, and is within a certain distance of this car.
            if self.direction == 0 and cPosY == posY and cPosX - posX < 50 and cPosX > posX and not car.moving:
                #If the car is moving to the right.
                self.moving = False
                return True
            if self.direction == 1 and cPosY == posY and posX - cPosX < 50 and cPosX < posX and not car.moving:
                self.moving = False
                return True
            if self.direction == 2 and cPosX == posX and cPosY - posY < 50 and cPosY > posY and not car.moving:
                self.moving = False
                return True
            if self.direction == 3 and cPosX == posX and posY - cPosY < 50 and cPosY < posY and not car.moving:
                self.moving = False
                return True

        self.moving = True
        return False

#Traffic light class
class trafficSprite(pygame.sprite.Sprite):
    def __init__(self, image, (posX, posY)):
        pygame.sprite.Sprite.__init__(self)
        self.position = (posX, posY)
        self.image = GraphicsHelper.getImage(image)
        self.rect = self.image.get_rect()
        self.rect.center = self.position
        self.go = True
        self.image.fill((0, 255, 0))

    #If click changes color, and changes interaction with cars.
    def changeColor(self):
        self.go = not self.go
        #Switches between the two colors and states.
        if self.go:
            self.image.fill((0, 255, 0))
        else:
            self.image.fill((255, 0, 0))

    #Detects and initiates the change if the user has clicked on the traffic light.
    def detectChange(self, mPos):
        if self.rect.collidepoint(mPos):
            self.changeColor()

    def getStop(self):
        return self.go

#Retry Button class
class retryButton(pygame.sprite.Sprite):
    def __init__(self, image, (posX, posY)):
        pygame.sprite.Sprite.__init__(self)
        self.position = (posX, posY)
        self.image = GraphicsHelper.getImage(image)
        self.rect = self.image.get_rect()
        self.rect.center = self.position

    def detectMouse(self, mPos):
        return self.rect.collidepoint(mPos)



