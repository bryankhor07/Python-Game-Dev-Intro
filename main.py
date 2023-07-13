import pygame
import time
import random
pygame.font.init()

# This is the width and height of your window.
WIDTH, HEIGHT = 1000, 700

# This is how you set up your window.
WINDOW = pygame.display.set_mode((WIDTH,HEIGHT))

# This is how you set the name of your game at the top of the window.
pygame.display.set_caption("Space Dodge")

# This is how you load an image: pygame.image.load(bg.jpeg)
# For some of you, your image might be a little bit smaller and you might want to scale it up or make it larger.
# so that it fills the screen. Now, to scale your image, you can do the following: 
# pygame.transform.scale(pygame.image.load("bg.jpeg"),(WIDTH,HEIGHT))
BG = pygame.transform.scale(pygame.image.load("bg.jpeg"),(WIDTH,HEIGHT))

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60

PLAYER_VELOCITY = 5
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VELOCITY = 3

FONT = pygame.font.SysFont("comicsans", 30)

# Okay, now that we have our background image, we actually need to put that on the screen. Now I like to do all of my drawing
# in a separate function just to keep it very clear and kind of organized. So I'm going to create a function here
# called draw inside of this function.
def draw(player, elapsed_time, stars):
    # For now, I'm going to draw this background image onto the screen.
    # To do that, we're going to use our window, which is our capital WINDOW variable, and we're going to say, WINDOW.blit().
    # blit() is a special method that you use when you want to draw an image or a surface.
    # So we are going to blit the background image and then we need to pass the coordinates of the top left hand corner of this image.
    # So in pygame, when we're talking about our coordinate system, zero zero is the top left hand corner of the screen.
    # Now I want my background image to fill the entire screen, so I'm going to put zero zero
    # as the coordinate of where the top left hand corner of this background image should be placed.

    # Now, to draw the elapsed time, we actually need to use a font because we're going to have text
    # on the screen that says time. So what we need to do is initialize our font module, create
    # a font object, and then use that font to render some text on the screen.
    WINDOW.blit(BG, (0,0))

    # This statement will give us the time in text.
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "yellow")
    # Now that we have our text, we need to render this on the screen.
    # (10,10) is the x and y axis
    WINDOW.blit(time_text, (10,10))

    # This is how you draw your player on your window.
    # I'm also going to set a color for my player.
    pygame.draw.rect(WINDOW, "red", player)

    for star in stars:
        pygame.draw.rect(WINDOW, "white", star)

    # This is going to refresh the display, which means any draws that we've done
    # will actually be applied and put onto the screen. 
    pygame.display.update()

# So now that we have our window here, our width and height, we need to set up what's known as the main game loop.
# Now, whenever you're working in a game, you need a loop, typically a while loop that is going to run while the game runs.
# So that actually keeps it alive. The while loop will do things like check for collision, check for movements or key presses
# and then adjust what's being displayed on the screen.

# So what we're going to do is create a function called main.
# This is really where the main game logic is going to exist.
def main():
    run = True

    # We're going to pick a starting X and a starting Y position for our character. 
    # Now remember that this is going to be the top left hand corner of where we are drawing the player.
    # So we can pick any x coordinate we want. I'm going to pick 200 and then for the Y coordinate, we want this player to be
    # at the bottom of the screen. So to do this dynamically, we're going to take the height of the screen
    # and we're going to subtract the height of the player. So we take height minus player height. That gives us the top left
    # hand corner where we draw this player. So that means that since our height is 700 and our player height is 60,
    # we're going to draw this at 640, meaning the bottom of the player will be directly at the bottom of the screen.
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT) # pygame.Rect(x, y, width, height)

    # We need to set up a clock object to adjust the velocity of our player.
    clock = pygame.time.Clock()

    # We know how much time has elapsed. time.time() is going to give us the current time.
    start_time = time.time()
    elapsed_time = 0

    # Now we're going to generate our projectiles.
    # I'm going to say star add increment is equal to 2000 milliseconds, 
    # which means the first star that we add will be added in 2000 milliseconds.
    star_add_increment = 2000
    # This is actually just going to be a variable that tells us when we should add the next star.
    star_count = 0

    # This is where we're going to store all of our different stars that are currently on screen
    stars = []

    hit = False
    # Inside of here is going to be our main game loop.
    while run:
        # We're going to put 60, which is the maximum number of frames per second or number of times that you want
        # this while loop to be running.
        # This is essentially going to delay the while loop such that it will only run a maximum of 60 times per second.
        star_count += clock.tick(60)

        # So we're essentially storing what time we started the while loop. And then every time we iterate,
        # we're getting what the current time is and subtracting that from the start time, which will give us the number of seconds
        # that have elapsed since we started the game.
        elapsed_time = time.time() - start_time

        # As soon as we have 2000 milliseconds that have elapsed, then we trigger this and then we add a star.
        # Now I'm actually going to add three stars at a time, but you could add a random number.
        if star_count > star_add_increment:
            for _ in range(3):
                # Now the reason we're doing this is because we want to pick a random integer in the range of zero
                # and width
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                # Now we add this star to our stars list.
                stars.append(star)

            star_add_increment = max(200, star_add_increment- 50)
            star_count = 0

        # The first thing that I always do inside of my game loop is I check to see if the user press the X button on the window.
        # If they did that, then I want to close the window. It's not automatically programed in.
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # If the user hit the X button then run = False and break the loop.
                run = False
                break

        # Now that we have a rectangle, we want to move it around. Now to move the rectangle is as easy as adjusting the x coordinate
        # of this rectangle. The first thing we need to do is listen for different key presses. 
        # If the user presses the left-arrow key, I want to move left, which would be reducing its x value.
        # Now this will give you a list of all of the keys that the user has pressed and tell you, well, if they press them or not.
        keys = pygame.key.get_pressed()
        # If they're pressing the left arrow key, then we're going to subtract the x.
        # The reason we subtract x is because we want to move to the left. 
        # So by subtracting their x coordinate, we move them closer to the zero zero position.
        # Now we have the player velocity set at five, which means every time that you press this key, we're going to go
        # five pixels backwards.
        # We need to add (player.x - PLAYER_VELOCITY >= 0) and (player.x + PLAYER_VELOCITY + player.width <= WIDTH) 
        # so that the player don't move completely off the screen.
        if keys[pygame.K_LEFT] and player.x - PLAYER_VELOCITY >= 0:
            player.x -= PLAYER_VELOCITY
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VELOCITY + player.width <= WIDTH:
            player.x += PLAYER_VELOCITY

        # We need to move our stars
        for star in stars[:]:
            star.y += STAR_VELOCITY
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break
        
        # Lastly, we need to handle when the player loses the game when it gets hit by a star.
        # Before our draw statement, we're going to check if the player was hit by a star.
        if hit:
            lost_text = FONT.render("You Lost!", 1, "yellow")
            # Okay, now I'm going to draw this on the center of the screen.
            WINDOW.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            # I'm also going to display the duration that the player survived.
            time_text = FONT.render(f"You survived for {round(elapsed_time)}s", 1, "yellow")
            WINDOW.blit(time_text, (WIDTH/2 - time_text.get_width()/2, HEIGHT/2 - time_text.get_height()/2 + 40))
            # Since I'm not doing this in the draw function, I need to manually update the display
            pygame.display.update()
            # Then we just freeze the game. So this is just delaying everything for 4 seconds.
            pygame.time.delay(4000)
            # You can either break to end the game or call the main function to restart the game.
            break
        
        # So now before we exit our while loop, we're going to call this draw function.
        # So now every single frame, we're going to call the draw function and it's going to continue
        # to draw this on the screen.
        # Okay, so now that we have our player, we want to draw this player onto the screen. 
        # So I'm going to pass this player rectangle to my draw function
        # Now that we have the elapsed time, we can pass that to our draw function and we can draw the elapsed time on the screen.
        draw(player, elapsed_time, stars)
    
    # pygame.quit() will close the game for us.
    pygame.quit()

# Now, what this statement is doing right here is making sure that we are directly running this python file.
# So we're running the file itself. 
# We're not importing it because if we were to import it or if we were, did not have this line, for example,
# if we were to import this file from another python file, we don't need this statement.
if __name__ == "__main__":
    main()