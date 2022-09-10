import pygame
import time
import random
 
pygame.init()
 
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
 
dis_width = 1200
dis_height = 800
 
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Multiplayer')
 
clock = pygame.time.Clock()
arrow_keys = [pygame.K_LEFT, pygame.K_UP,pygame.K_RIGHT,pygame.K_DOWN]
wasd_keys= [pygame.K_a,pygame.K_w,pygame.K_d,pygame.K_s]
jilk_keys = [pygame.K_j,pygame.K_i,pygame.K_l,pygame.K_k]

snake_block = 10
snake_speed = 25
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 15)
class Player:
    def __init__(self, color,keys):
        self.x = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
        self.y = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
        
        self.x_change = 0
        self.y_change = 0
        self.alive = True
        self.is_eating = False
        self.color = color
        self.snake_list = []
        self.length = 1
        self.direction = None
        self.snake_head = []
        self.keys = keys

    def left_press(self):
        if(self.direction != "right"):
            self.x_change = -snake_block
            self.y_change = 0
            self.direction = "left"

    def right_press(self):
        if(self.direction != "left"):
            self.x_change = snake_block
            self.y_change = 0
            self.direction = "right"

    def up_press(self):
        if(self.direction != "down"):
            self.x_change = 0
            self.y_change = -snake_block
            self.direction = "up"

    def down_press(self):
        if(self.direction != "up"):
            self.x_change = 0
            self.y_change = snake_block
            self.direction = "down"

    def collide(self, other):
        for x in other.snake_list:
            if x == self.snake_head:
                self.length -= 1
                #print("collision")
            
    def press(self,key):
        if key == self.keys[0]:
            self.left_press()
        elif key == self.keys[1]:
            self.up_press()
        elif key == self.keys[2]:
            self.right_press()
        elif key == self.keys[3]:
            self.down_press()

    def move(self,food):
        if self.length < 1:
            self.length = 1
        #print(f"x: {self.x} y: {self.y}")
        self.is_eating = False
        self.x += self.x_change
        self.y += self.y_change
        # set size of snake
        self.snake_head=[]
        self.snake_head.append(self.x)
        self.snake_head.append(self.y)
        self.snake_list.append(self.snake_head)
        while len(self.snake_list) > self.length:
            del self.snake_list[0]
        
        #draw snake
        for x in self.snake_list:
            pygame.draw.rect(dis, self.color, [x[0], x[1], snake_block, snake_block])
        # check self crash
        for x in self.snake_list[:-1]:
            if x == self.snake_head:
                self.length -=1
                #self.alive = False
        
        # check frame crash
        if self.x >= dis_width or self.x < 0 or self.y >= dis_height or self.y < 0:
            #self.length -=1
            if self.x >= dis_width:
                self.x = 0
            elif self.x < 0:
                self.x = dis_width
            elif self.y >= dis_height:
                self.y = 0
            else:
                self.y = dis_height
            #self.alive = False
        if self.x == food[0] and self.y == food[1]:
            self.length +=1
            self.is_eating = True


def display_scores(players):
    for i, player in enumerate(players):
        value = score_font.render(f"Player {i} score: " + str(player.length -1), True, green)
        dis.blit(value, [0, i*20])
   
 
def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])
    
def spawn_food(food):
    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
    food = (foodx,foody)
    draw_food(food)
    #print(f"Food spawned at{food}")
    return food

def draw_food(food):
    pygame.draw.rect(dis, red, [food[0], food[1], snake_block, snake_block])

def gameLoop():
    food = (0,0)
    game_over = False
    game_close = False
    p1 = Player(yellow, arrow_keys)
    p2 = Player(blue, wasd_keys)
    p3 = Player(white, jilk_keys)
    players = [p1,p2,p3]
    food = spawn_food(food)
    while not game_over:
        while game_close == True:
            
            message("You Lost! Press C-Play Again or Q-Quit", red)
            pygame.display.update()
 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            
            if event.type == pygame.KEYDOWN:
                for player in players:
                    player.press(event.key)
        
        dis.fill(black)
        # Move players
        for player in players:
            player.move(food)

        # Status of players
        food_spawned = False
        for player in players:
            if not player.alive:
                game_close = True
            if player.is_eating:
                food = spawn_food(food)
                food_spawned = True
            for other in players:
                if not player == other:
                    player.collide(other)

        if not food_spawned:
            draw_food(food)
        display_scores(players)
        pygame.display.update()
 
        clock.tick(snake_speed)
 
    pygame.quit()
    quit()
 
 
gameLoop()