import pygame
from random import choice

# TODO
# -holding
# -better scoring
# -bag randomizer
# -speeding up
# -game over screen
# -title screen
# -fix rotating on right side
# -line that isn't bottom

# the arrays on the right are the shapes of the blockss
# eg the T is [
# [0, 1, 0]
# [1, 1, 1]
# ] 
tetrominoes = {
    'O': {'color': "yellow", 'shape': [[1, 1], [1, 1]]},
    'I': {'color': "cyan", 'shape': [[1, 1, 1, 1]]},
    'Z': {'color': "red", 'shape': [[1, 1, 0], [0, 1, 1]]},
    'S': {'color': "green", 'shape': [[0, 1, 1], [1, 1, 0]]},
    'L': {'color': "orange", 'shape': [[1, 0, 0], [1, 1, 1]]},
    'J': {'color': "blue", 'shape': [[0, 0, 1], [1, 1, 1]]},
    'T': {'color': "purple", 'shape': [[0, 1, 0], [1, 1, 1]]}
}

# set up pygame stuff
pygame.init()
screen = pygame.display.set_mode((250, 600))
pygame.display.set_caption("ICS3U1 Tetris")

# run until user asks to quit
running = True

class Tetromino:
    def __init__(self, shapecolor=None):
        # generates a random shapecolor if one isn't provided
        if not shapecolor:
            self.shapecolor = choice(list(tetrominoes.keys()))
        else:
            self.shapecolor = shapecolor
        # uses the dict to assign a color and shape to the main key
        self.color = tetrominoes[self.shapecolor]['color']
        self.shape = tetrominoes[self.shapecolor]['shape']
        self.position = [0, round(10 / 2) - round(len(self.shape[0]) / 2)]

    # move block left if a is pressed and it's a valid position.
    def movement(self, keys):
        if keys[pygame.K_a]:
            self.position[1] -= 1
            if not self.valid_position():
                self.position[1] += 1
        elif keys[pygame.K_d]:
            self.position[1] += 1
            if not self.valid_position():
                self.position[1] -= 1
        
    def gravity(self):
        self.position[0] += 1
        if not self.valid_position():
            self.position[0] -= 1
            self.lockin()

    def rotate(self, keys):
        if keys[pygame.K_e]:
            # found this neat line on stack overflow, it rotates a 2d list clockwise
            # (in this case the block)
            self.shape = list(zip(*self.shape[::-1]))
            if not self.valid_position():
                # same but counter clockwise
                self.shape = list(zip(*self.shape))[::-1]
        elif keys[pygame.K_q]:
            self.shape = list(zip(*self.shape))[::-1]
            if not self.valid_position():
                self.shape = list(zip(*self.shape[::-1]))

    # checks if the position you're trying to go to is valid
    def valid_position(self):
        for row_index, row in enumerate(self.shape):
            for col_index, value in enumerate(row):
                if value != 0:
                    new_x = self.position[1] + col_index
                    new_y = self.position[0] + row_index
                    if new_x < 0 or new_x > 9 or new_y > 19 or (new_y >= 0 and game_grid[new_y][new_x] != 0):
                        return False
        return True
    
    # locks in current position into the main game grid.
    def lockin(self):
        for row_index, row in enumerate(self.shape):
            for col_index, value in enumerate(row):
                if value != 0:
                    game_grid[self.position[0] + row_index][self.position[1] + col_index] = self.color
        # makes you lose if you reach the top
        if game_grid[0][4] or game_grid[0][5] or game_grid[0][3] or game_grid[0][6]:
            pygame.quit()
        else:
            self.__init__()

    # drawing of tetronimoes is done seperately from placed grid, because doing them together was a nightmare
    def draw(self):
        for row_index, row in enumerate(self.shape):
            for col_index, value in enumerate(row):
                if value != 0:
                    pygame.draw.rect(screen, self.color, ((self.position[1] + col_index) * 25, (self.position[0] + row_index) * 25, 25, 25))
                

# grid used for game
#!!!! THE GRID IS IN Y, X !!!! [0][1] IS 1 TILE RIGHT OF THE TOP LEFT!!!
game_grid = [
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
  ]

clock = pygame.time.Clock()
time = 0
tetro =  Tetromino()
interval = 30
score = 0
held = None

# set up text for score
font = pygame.font.Font('freesansbold.ttf', 20)

# main game loop
while running:
    screen.fill("black")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                if held:
                    temp = tetro.shapecolor
                    tetro.__init__(held)
                    held = temp
                else:
                    held = tetro.shapecolor
                    tetro.__init__()
    time += 1

    # updates and draws text
    scoretext = font.render(f"Score: {score}", True, "white")
    heldtext = font.render(f"Held:", True, "white")
    screen.blit(scoretext, (40, 540))
    screen.blit(heldtext, (160, 520))
    held_render_pos = [160, 540]
    
    # pretty much just slightly tweaked code from Tetronimo.draw() to render the block you're holding
    if held:
        for row_index, row in enumerate(tetrominoes[held]['shape']):
                for col_index, value in enumerate(row):
                    if value != 0:
                        pygame.draw.rect(screen, tetrominoes[held]['color'], (held_render_pos[0] + (col_index * 25), held_render_pos[1] + (row_index * 25), 25, 25))

    # basically multiplies the index by 25 to draw a 25 by 25 square at the appropriate place
    # relative to the grid. i found enumerate on google to have access to both the indices and values
    for row_index, row in enumerate(game_grid):
        for col_index, value in enumerate(row):
            pygame.draw.rect(screen, value, (col_index * 25, row_index * 25, 25, 25))

    full_count = 0

    # checks and clears line at bottom.
    for i in game_grid[19]:
        if i != 0:
            full_count += 1
    if full_count == 10:
        for i in range(10):
            game_grid[19][i] = 0
        score += 100

        # brings everything down 1 tile after clearing tile
        for i in range(19, 0, -1):
            game_grid[i] = game_grid[i-1]
        game_grid[0] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        

    keys = pygame.key.get_pressed()

    # makes the block fall faster if s is held
    if keys[pygame.K_s]:
        gravity_interval = 5
    # mega slow down for debugging
    elif keys[pygame.K_p]:
        gravity_interval = 120
    else:
        gravity_interval = 30
    movement_interval = 7

    tetro.draw()

    # the interval dictactes how often the blocks move down a tile or are allowed to move
    if time % gravity_interval == 0:
        tetro.gravity()
    if time % movement_interval == 0:
        tetro.movement(keys)
        tetro.rotate(keys)

    # generates grid lines for visibility
    for row_index, row in enumerate(game_grid):
        for col_index, value in enumerate(row):
            pygame.draw.line(screen, "gray", [col_index * 25, 0], [col_index * 25, 500])
            pygame.draw.line(screen, "gray", [0, row_index * 25], [250, row_index * 25])
    # two extra lines that dont get drawn in the for loop
    pygame.draw.line(screen, "gray", [0, 499], [250, 499])
    pygame.draw.line(screen, "gray", [249, 0], [249, 500])

    # update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()