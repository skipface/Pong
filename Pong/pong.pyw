import pygame 
import random

# Score
RED = 0
BLUE = 0

# Settings
WIDTH = 800
HEIGHT = 600
FPS = 60
PADDLE_SIZE = 120
BALL_SIZE = 10
COMPUTER = False

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 155)
red = (155, 0, 0)

# Init pygame
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
screen.fill(black)

pygame.display.update()


class Paddle:
    def __init__(self, x):
        self.x = x
        self.y = HEIGHT/2
        self.direction = "none"
        self.nextMove = 0

    def update(self): 
        # Move the paddle
        if self.direction == "up" and self.y >= 0: 
            self.y -= 5
        elif self.direction == "down" and self.y <= HEIGHT - PADDLE_SIZE:
            self.y += 5

    def computerUpdate(self, ball):
        # If computer mode is enabled
        # Move paddle2 based on ball.y pos
        if COMPUTER == True:
                if ball.y <= self.y and self.nextMove == 0:
                    self.direction = "up"
                    self.nextMove = 10 # Delay the paddles next move for 15 ticks 
                elif ball.y >= self.y and self.nextMove == 0:
                    self.direction = "down"
                    self.nextMove = 10
                self.nextMove -= 1

    def draw(self):
        # Draw the paddle to the screen
        pygame.draw.rect(screen, white, (self.x, self.y, 10, PADDLE_SIZE))

class Ball:
    def __init__(self):
        self.x = WIDTH / 2
        self.y = HEIGHT / 2
        self.directionX = random.choice(["left", "right"])
        self.directionY = random.choice(["up", "down"])

    def update(self):        
        # Move the ball
        if self.directionX == "left":
            self.x -= 5
        if self.directionX == "right":
            self.x += 5
        if self.directionY == "up":
            self.y -= 5
        if self.directionY == "down":
            self.y += 5

        # Change direction if out of bounds
        if self.y <= 0:
            self.directionY = "down"
        if self.y >= HEIGHT - BALL_SIZE:
            self.directionY = "up"

    def collisions(self, paddle1, paddle2):
        global BLUE
        global RED

        # When the ball touches the paddle change direction
        if self.x >= 10 and self.x <= 20 and self.y >= paddle1.y and self.y <= paddle1.y + PADDLE_SIZE:
            self.directionX = "right"
        if self.x <= WIDTH - 20 and self.x >= WIDTH - 30 and self.y >= paddle2.y and self.y <= paddle2.y + PADDLE_SIZE:
            self.directionX = "left"

        # Add score if ball is behind paddle
        if self.x <= 0:
            RED += 1
            main()
        if self.x >= WIDTH:
            BLUE += 1
            main()

        # If score is > 7 end the game
        if BLUE == 7:
            gameOver("red")
        if RED == 7:
            gameOver("blue")
        
    def draw(self):
        # Draw the ball to the screen
        pygame.draw.rect(screen, white, (self.x, self.y, BALL_SIZE, BALL_SIZE))

def drawText(text, x, y, color):
    font = pygame.font.SysFont(text, 60)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))

def startMenu():
    global COMPUTER

    while True:
        screen.fill(black)
        drawText("Welcome to Pong!", WIDTH/2 - 230, HEIGHT/2 - 50, white)
        drawText("Press c to start or esc to exit", WIDTH/2 - 280, HEIGHT/2, white)
        drawText("Computer {}".format(COMPUTER), 10, HEIGHT - 50, white)
        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_c:
                    main()
                if e.key == pygame.K_ESCAPE:
                    pygame.exit()
                if e.key == pygame.K_t:
                    COMPUTER = not COMPUTER

def gameOver(Winner):
    global RED
    global BLUE

    BLUE = 0
    RED = 0

    screen.fill(black)
    drawText("Congratulations {} you win!".format(Winner), WIDTH/2 - 300, HEIGHT/2, white)
    pygame.display.update()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                if e.key == pygame.K_c:
                    startMenu()

def main():
    # Change to global or else python will assign a new variable
    # Instead of accessing the global variable RED, and BLUE.
    global RED
    global BLUE

    paddle1 = Paddle(10)
    paddle2 = Paddle(WIDTH - 20)
    ball =  Ball()

    # Main loop
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit()
                if e.key == pygame.K_UP:
                    paddle1.direction = "up"
                if e.key == pygame.K_DOWN:
                    paddle1.direction = "down"
                if COMPUTER == False:
                    if e.key == pygame.K_w:
                        paddle2.direction = "up"
                    if e.key == pygame.K_s:
                        paddle2.direction = "down"
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_UP or e.key == pygame.K_DOWN:
                    paddle1.direction = "none"
                if COMPUTER == False:
                    if e.key == pygame.K_w or e.key == pygame.K_s:
                        paddle2.direction = "none"

        # Move paddles and ball
        paddle1.update()
        paddle2.update()
        ball.update()
        ball.collisions(paddle1, paddle2)
        if COMPUTER == True: paddle2.computerUpdate(ball)

        # Draw screen
        screen.fill(black)
        paddle1.draw()
        paddle2.draw()
        ball.draw()
        drawText(str(BLUE), WIDTH/2 - 60, HEIGHT/2, red)
        drawText(str(RED), WIDTH/2 + 50, HEIGHT/2, blue)
        pygame.display.update()

        clock.tick(FPS)                  

if __name__ == "__main__":
    startMenu()