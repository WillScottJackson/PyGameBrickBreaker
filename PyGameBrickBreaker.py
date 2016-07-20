import sys, pygame, random 

#--------------------- Variables ----------------------------------#
# Variables are used to store data in. We need to use variables to keep
# track of our game's parameters. These include the speed at which things run,
# the colours and size of the objects we use and may other things.
# When making your own variables, make sure you give them names that make sense
# Always keep your variables grouped together somewhere near the top of your code
# so you know where to find them if you need to change anything. 

# The highest score during the play session
highScore = 0 

# The current score during a particular round.
currentScore = 0 

# Speed of the paddle
paddleSpeed = 4 

# Boolean state to tell if the game is still running or not
running = True 
# Boolean state to tell if the player has lost the game
gameLost = False
# Boolean state to tell if the player has won the game
gameWon = False

# Tuple that defines the screen size
size = width, height = 500, 500 

# What is the point where the ball falls out of the playable area and becomes game over?
deathZone = height - 10 

# Tuples that defines the colours we want to use
blue = 0, 0, 255 
red = 255, 0, 0 
yellow = 255, 255, 0 
green = 0, 255, 0 
white = 255, 255, 255 

# Circle Radius
circleRadius = 15 

# List of x,y coordinates of the bricks. We could add as many of these as we could fit on our screen. 
brickPosList = [] 
brickPosList.append((50, 100)) 
brickPosList.append((200, 100)) 
brickPosList.append((350, 100)) 
brickPosList.append((50, 200)) 
brickPosList.append((200, 200)) 
brickPosList.append((350, 200)) 

#--------------------- Classes ----------------------------------#
# A class is a hierarchy of data structures and associated functions
# you can define yourself to represent a wide variety of possible
# ideas, concepts and things. For this project we are doing to  write
# a class to define a Paddle that the player uses to engage with the game.
# We're going to write a class to define the ball the player has to
# intercept. And we're going to write a class to represent the bricks
# we are trying to break. 

# Class that defines the attributes of the in game paddle
# The paddles have the following attributes:
# 1: Width, this is measured in pixels on your screen
# 2: Height, this too is also measured in pixels on your screen
# 3: Speed, this is measure in number of "pixels moved per frame"  this is why it is a good idea to lock the frame rate.
# 4: Colour, made up of three channels, red green and blue channels. These vary between 0-255
# 5: Paddle centre X coordinate, where the middle x coordinate is, helps us keep track of it's movement
# 6: Paddle centre Y coordinate, where the middle Y coordinate is. We only set this once to decide how far down the screen the paddle should be
class Paddle:
    def __init__(self, paddleWidth, paddleHeight, paddleSpeed, paddleColour):
        self.width = paddleWidth 
        self.height = paddleHeight 
        self.colour = paddleColour 
        self.speed = paddleSpeed 
        self.centreX = 0 
        self.centreY = 0 

# Class that defines the attributes of the ball (i.e. makes the creation of multiple balls possible if you want to go crazy)
# Ball objects have the following attriutes
# 1: Radius, measured in pixels
# 2: Colour, see the description of the paddle colour
# 3: Centre X, coordinate of the ball centre in the X Axis
# 4: Centre Y, coordiate of the ball centre in the Y axis
# 5: Speed X, horizontal speed of the ball
# 6: Speed Y, vertical speed of the ball
class Ball:
    def __init__(self, radius, colour):
        self.radius = radius 
        self.colour = colour 
        self.centreX = 0 
        self.centreY = 0 
        self.speedX = 0 
        self.speedY = 0 

    # Function to send the ball in a random direction, it's best to call this once at the start of the game
    def setRandomSpeed(self):
        speedRange = range(-4, -1) + range(1, 4) 
        self.speedX = random.choice(speedRange) 
        self.speedY = random.choice(speedRange) 

    # Function to set the position of the ball, use this to set the prelminary position of the ball
    def setPosition(self, x, y):
        self.centreX = x 
        self.centreY = y 

# Class that defines the attributes of the bricks
# A brick object has the following attributes
# 1: Width, similar to the width of a paddle
# 2: Height, similar to the height of a paddle
# 3: Colour, similar to the colour of a paddle
# 4: Hit points, a variable that represents how many times a brick can be hit before it disappears
# 5: X coordinate, x coordinate representing the corner of the brick
# 6: y Coorindate, y coordinate representing te corner of the brick
# 7: Existence, does the brick still exist in the game? (yes if it has > 0 HP  no if HP == 0)
class Brick:
    def __init__(self, brickWidth, brickHeight, colour, hitPoints, x, y):
        self.width = brickWidth 
        self.height = brickHeight 
        self.colour = colour 
        self.hitPoints = hitPoints 
        self.centreX = x 
        self.centreY = y 
        self.exist = True 
        self.rect = pygame.Rect(self.centreX, self.centreY, self.width, self.height) 

    def resetHP(self):
        self.hitPoints = 3 
        self.exist = True 

#--------------------- Functions ----------------------------------#
# Functions are blocks of code that we can write and call upon whenever
# we need them. This saves us from rewriting the same pieces of code over
# and over again. We are going to write some functions that will perform
# repetitive instructions for us, such as refreshing the screen and detecting
# collisions between objects. Functions are defined up here, but the code itself
# doesn't run until we ask it to later. Always define your functions close to the top
# of your code so that you don't try to call a function before you
# have defined it

# Helper function to initialise the game. 
def initGame():

    global currentScore
    currentScore = 0
    # Starting positions of the paddle
    paddle.centreX = width * 0.5 
    paddle.centreY = height * 0.8 

    # Current position of the ball
    ball.centreX = width * 0.5 
    ball.centreY = height * 0.5 

    # Initialise the "player character" as a rectangle of specified position and dimensions
    paddle.rect = pygame.Rect(paddle.centreX, paddle.centreY, paddle.width, paddle.height) 

    # Set the paddle to stationary 
    direction = 0 

    # send the ball in a random direction 
    ball.setRandomSpeed() 
    
# Helper function to update the screen after every frame update. 
def updateScreen():

    # First paint on the background
    screen.fill(white) 

    # Second, paint on all the bricks
    for i in range(len(bricks)):
        pygame.draw.rect(screen, bricks[i].colour, bricks[i].rect, 0) 

    # Third, paint the paddle on the screen
    pygame.draw.rect(screen, paddle.colour, paddle.rect, 0) 

    # Fourth, paint the ball on the screen
    pygame.draw.circle(screen, red, (int(ball.centreX), int(ball.centreY)),ball.radius, 0) 

    # Fifth, paint the text with the current and high scores on:
    scoreLabel = myfont.render("Current Score: " + str(currentScore), 1, (0, 0, 0)) 
    screen.blit(scoreLabel, (0, 0)) 
    highLabel = myfont.render("High Score: " + str(highScore), 1, (0, 0, 0)) 
    screen.blit(highLabel, (width*0.5, 0)) 

    # Finally, push the new pixels to the display. 
    pygame.display.update() 

# Helper function to update the game over screen.
def updateGameOver():
    screen.fill(white) 
    gameOver = myfont.render("Game Over", 1, (0,0,0))
    screen.blit(gameOver, ((width * 0.5) - 100, height * 0.5))
    tryAgain = myfont.render("Press Enter to Retry", 1, (0,0,0))
    screen.blit(tryAgain, ((width * 0.5) - 100, (height* 0.5) + 30))
    pygame.display.update() 

# Helper function to update the congratulations screen.
def updateCongratulations():
    screen.fill(white) 
    congratulations = myfont.render("You win! Congratulations!", 1, (0,0,255))
    screen.blit(congratulations, ((width * 0.25) - 100, height * 0.5))
    playAgain = myfont.render("Press Enter to Start a New Game", 1, (0,0,0))
    screen.blit(playAgain, ((width * 0.25) - 100, (height* 0.5) + 30))
    pygame.display.update() 

# Helper function to move the ball. 
def moveBall():
    # Move the centre of the ball in the x direction depending on the speed.
    ball.centreX += ball.speedX 

    # Move the centre of the ball in the y direction depending on the speed. 
    ball.centreY += ball.speedY 

# Helper function to perform of the necessary collision detections.
def detectBallCollisions():
    global currentScore
    
    # Detect ball collisions
    # Wall Collisions
    # If the ball goes outside of the boundaries in a particular direction  reflect the ball in the opposite direction
    if ((ball.centreX < circleRadius) or (ball.centreX > width - circleRadius)):
        ball.speedX = -ball.speedX 
    if (ball.centreY < ball.radius):
        ball.speedY = -ball.speedY 

    # Collisions with the Paddle horizontal plane
    pYOffset = abs(ball.centreY - paddle.rect.centery) 
    pXOffset = abs(ball.centreX - paddle.rect.centerx) 
    if ((pYOffset < abs(ball.radius + paddle.rect.height/2)) and (pXOffset < abs(ball.radius - paddle.rect.width * 0.75))):
        ball.speedY = -ball.speedY 

    # Collisions with the bricks
    for i in range(len(bricks)):
        if (bricks[i].exist):
            bYOffset = abs(ball.centreY - bricks[i].rect.centery) 
            bXOffset = abs(ball.centreX - bricks[i].rect.centerx) 
            # Check for collisions with the horizontal plane
            if ((bYOffset < abs(ball.radius + bricks[i].rect.height/2)) and (bXOffset < abs(ball.radius - bricks[i].rect.width * 0.75))):
                ball.speedY = -ball.speedY 
                bricks[i].hitPoints = bricks[i].hitPoints - 1 
                currentScore+=1 
                updateHighScore() 

            # Check for collisions in the vertical plane
            # yOffset needs to be contained within the height of the paddle, xOffset can be the same
            if (ball.centreY < abs(bricks[i].centreY - bricks[i].height/2) and ball.centreX == abs(bricks[i].centreX - bricks[i].rect.width/2)):
                ball.speedX = -ball.speedX 
                bricks[i].hitPoints = bricks[i].hitPoints - 1 
                currentScore+=1
                updateHighScore() 

# Helper function to update the colours of the bricks based on how much damage they have taken
def updateBricks():
    for i in range(len(bricks)):
        if (bricks[i].hitPoints == 3):
            bricks[i].colour = green 
        elif (bricks[i].hitPoints == 2):
            bricks[i].colour = yellow 
        elif (bricks[i].hitPoints == 1):
            bricks[i].colour = red 
        elif (bricks[i].hitPoints == 0):
            bricks[i].colour = white 
            bricks[i].exist = False 

# Helper function to reset the bricks to their starting state. 
def resetBricks():
    for i in range (len(bricks)):
        bricks[i].resetHP() 
        
def updateHighScore():
    global highScore
    if currentScore > highScore:
        highScore = currentScore

#--------------------- Initialisation ----------------------------------#
# Here is where we set up the various parameters of our game, this is
# for all intents and purposes, where the functionality of the code starts
# from.

# Initialise the Pygame module and functions
pygame.init() 

# Load a font into the module so we can display some text with it. 
myfont = pygame.font.SysFont("arial", 30) 

# Initialise the game screen
screen = pygame.display.set_mode(size) 
pygame.display.set_caption("Coding Hub Brick Breaker: Solution") 

# Initialise the paddle
paddle = Paddle(100, 15, paddleSpeed, blue) 

# Initialise the ball
ball = Ball(circleRadius, red) 

# Initialise the bricks
bricks = [Brick(100, 15, green, 3, brickPosList[count][0], brickPosList[count][1]) for count in xrange(len(brickPosList))] 

# Initialise the parameters of the game. 
initGame() 

# Set up a clock to lock the game at a specific frame rate
clock = pygame.time.Clock() 

# Run indefinitely
while True:

    while running:
        # Limit frame rate to 60 frames per second
        clock.tick(60) 
        # Get every event that has happened within the last frame
        for event in pygame.event.get():
            # If the player has opted to exit, quit the game
            if event.type == pygame.QUIT:
                pygame.display.quit() 
                sys.exit() 

            # Was there a key pressed down on the keyboard?
            if event.type == pygame.KEYDOWN:

                # Get the details of the keys that were pressed
                keys = pygame.key.get_pressed() 

                # Which key was pressed? Set the direction accordingly
                if keys[pygame.K_ESCAPE]:
                    pygame.display.quit() 
                    sys.exit() 
                if keys[pygame.K_LEFT]:
                    direction = -paddle.speed 
                elif keys[pygame.K_RIGHT]:
                    direction = paddle.speed 
            else:
                direction = 0 

        # Limit the character movement to stay within the screen (i.e. detect collisions)
        if ((paddle.rect.centerx + (paddle.width * 0.5)) > width):
            direction = 0 
            paddle.rect = paddle.rect.move(-1, 0) 
        if ((paddle.rect.centerx - (paddle.width * 0.5)) < 0):
            direction = 0 
            paddle.rect = paddle.rect.move(1, 0) 

        paddle.rect = paddle.rect.move(direction, 0) 

        moveBall()

        detectBallCollisions() 
	
        # If the ball falls out of bounds, stop the game
        if (ball.centreY > deathZone):
            running = False
            gameLost= True

        updateBricks()
	
        # If there are no bricks left, finish the game
        if ( sum([b.exist for b in bricks])==0):
            running = False
            gameWon= True

        updateScreen()

    # Display the game over or winning screen and wait for the player to provide input
    while running == False:
        # Limit frame rate to 60 frames per second
        clock.tick(60)
        # Get every event that has happened within the last frame
        for event in pygame.event.get():
            # If the player has opted to exit, quit the game
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()

            # Was there a key pressed down on the keyboard?
            if event.type == pygame.KEYDOWN:

                # Get the details of the keys that were pressed
                keys = pygame.key.get_pressed()

                if keys[pygame.K_ESCAPE]:
                    pygame.display.quit() 
                    sys.exit()
                if keys[pygame.K_RETURN]:
                    # If the player preses the enter key, restart the game for another attempt
                    running = True
                    gameLost = False
                    gameWon = False
                    initGame()
                    resetBricks()
	
        if gameLost == True:            
        	updateGameOver()
        if gameWon == True:
            updateCongratulations()
