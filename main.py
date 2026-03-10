import random
from mimetypes import init

from pygame import display, image, QUIT, key, K_LEFT, K_RIGHT, draw, time # type: ignore

init()

width, height = 800, 600
screen = display.set_mode((width, height))
display.set_caption("Car Racing Game")

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

car_image = image.load('car.png')  
car_width = 50
car_height = 100

car_x = width // 2
car_y = height - car_height - 10
obstacle_width = 50
obstacle_height = 100
obstacle_x = random.randint(0, width - obstacle_width)
obstacle_y = -obstacle_height
obstacle_speed = 5
score = 0

# Game loop
running = True
while running:
    for event in event.get():
        if event.type == QUIT:
            running = False

    keys = key.get_pressed()
    if keys[K_LEFT] and car_x > 0:
        car_x -= 5
    if keys[K_RIGHT] and car_x < width - car_width:
        car_x += 5

    # Move the obstacle
    obstacle_y += obstacle_speed
    if obstacle_y > height:
        obstacle_y = -obstacle_height
        obstacle_x = random.randint(0, width - obstacle_width)
        score += 1

    # Collision detection
    if (car_y < obstacle_y + obstacle_height and
        car_y + car_height > obstacle_y and
        car_x < obstacle_x + obstacle_width and
        car_x + car_width > obstacle_x):
        print("Collision! Game Over.")
        running = False

    screen.fill(white)
    screen.blit(car_image, (car_x, car_y))
    draw.rect(screen, red, (obstacle_x, obstacle_y, obstacle_width, obstacle_height))
    display.flip()
    time.Clock().tick(60)

quit()

