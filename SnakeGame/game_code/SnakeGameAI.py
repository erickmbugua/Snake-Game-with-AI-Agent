# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 15:36:09 2020

@author: Mbugush
"""
import pygame
from SnakeDQN import DQN
from random import randint

snake_body=pygame.image.load("E:\PythonProjects\SnakeGame\images\snakeBody.png")
high_score=0

class Game():
    def __init__(self,width,height):
        pygame.init()
        self.width=width
        self.height=height
        self.screen=pygame.display.set_mode((self.width,self.height+60))
        self.bg = pygame.image.load("E:\PythonProjects\SnakeGame\images\playground.png")
        pygame.display.set_caption("Snake Game")
        self.clock=pygame.time.Clock()
        self.FPS=500
class Snake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.snake_head=pygame.image.load("E:\PythonProjects\SnakeGame\images\snakehead.png").convert()
        self.image=pygame.transform.smoothscale(self.snake_head,(20,20))
        self.rect=self.image.get_rect()
        self.rect.topleft=[20,20]
        self.game_crash=False
        self.body_size=0
        self.trail_arr=[]
        self.x_change=0
        self.y_change=0
        self.eaten=False
    def update_position(self,action):
        #sets x_change,y_change according to user's input
        if action==0:#DO NOTHING
            None
        elif action==1:#UP
            if len(self.trail_arr)>1 :#prevents snake from going back along same path
                if self.y_change!=20:
                    self.y_change=-20
                    self.x_change=0
            else:
                self.y_change=-20
                self.x_change=0
        elif action==2:#DOWN
            if len(self.trail_arr)>1 :
                if self.y_change!=-20:
                    self.y_change=20
                    self.x_change=0
            else:
                self.y_change=20
                self.x_change=0
        elif action==3:#LEFT
            if len(self.trail_arr)>1 :
                if self.x_change!=20:
                    self.x_change=-20
                    self.y_change=0
            else:
                self.x_change=-20
                self.y_change=0
        elif action==4:#RIGHT
            if len(self.trail_arr)>1 :
                if self.x_change!=-20:
                    self.x_change=20
                    self.y_change=0
            else:
                self.x_change=20
                self.y_change=0
    def update(self,game,food):
        #changes position of snake according to user's input
        if self.x_change==-20:
            self.rect.x-=20
            #checking that the new position isn't a part of the snake's body
            #else end game i.e snake hasn't eaten itself
            if self.rect.topleft not in self.trail_arr:
                self.trail_arr.append(self.rect.topleft)
                self.maintain_size_of_array()
            else:
                self.game_crash=True
        elif self.x_change==20:
            self.rect.x+=20
            if self.rect.topleft not in self.trail_arr:
                self.trail_arr.append(self.rect.topleft)
                self.maintain_size_of_array()
            else:
                self.game_crash=True
        elif self.y_change==-20:
            self.rect.y-=20
            if self.rect.topleft not in self.trail_arr:
                self.trail_arr.append(self.rect.topleft)
                self.maintain_size_of_array()
            else:
                self.game_crash=True
        elif self.y_change==20:
            self.rect.y+=20
            if self.rect.topleft not in self.trail_arr:
                self.trail_arr.append(self.rect.topleft)
                self.maintain_size_of_array()
            else:
                self.game_crash=True
        self.check_game_over(game)
        check_eat(self,food)
        self.elongate()
    def maintain_size_of_array(self):
        #ensures the trail_arr only contains parts of the changing snake body
        if len(self.trail_arr)>self.body_size:
            for i in range(len(self.trail_arr)-self.body_size-1):
                del self.trail_arr[i]
    def elongate(self):
        #appends the new position if snake has eaten thus increasing size
        if self.eaten==True:
            self.body_size+=1
        self.eaten=False
    def check_game_over(self,game):
        #checks if the snake has touched the playarea
        if self.rect.x==0 or self.rect.y==0\
               or self.rect.x==game.width-20 or self.rect.y==game.height-20\
               or [self.rect.x,self.rect.y] in self.trail_arr:
            self.game_crash=True
            
class Food(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.prey=pygame.image.load("E:\PythonProjects\SnakeGame\images\sungura.png")
        self.image=pygame.transform.smoothscale(self.prey,(20,20))
        self.rect=self.image.get_rect()
        self.x_rand=randint(40,380)
        self.x_food=self.x_rand-self.x_rand%20
        self.y_rand=randint(40,380)
        self.y_food=self.y_rand-self.y_rand%20
        self.rect.topleft=(self.x_food,self.y_food)
    def change_pos(self,snake):
        self.x_rand=randint(20,380)
        self.x_food=self.x_rand-self.x_rand%20
        self.y_rand=randint(20,380)
        self.y_food=self.y_rand-self.y_rand%20
        if (self.x_food,self.y_food) not in snake.trail_arr:
            self.rect.topleft=(self.x_food,self.y_food)
        else:
            self.change_pos(snake)
        
def check_eat(snake,food):
    #checks if snake has eaten food. If true, changes position of food
    if snake.rect.topleft==food.rect.topleft:
        food.change_pos(snake)
        snake.eaten=True

def record(snake):
    global high_score
    if snake.body_size>=high_score:
        high_score=snake.body_size    
            
def display_score(snake,game):
    global high_score
    text1=pygame.font.SysFont('chalkduster.ttf',30)
    score=str(snake.body_size)
    score_text="Score:"+score
    img1=text1.render(score_text,True, (255,0,0))
    game.screen.blit(img1,(50,460))
    text2=pygame.font.SysFont('chalkduster.ttf',30)
    record(snake)
    highest_score=str(high_score)
    high_score_text="Highest Score:"+highest_score
    img2=text2.render(high_score_text,True, (255,0,255))
    game.screen.blit(img2,(200,460))

def draw_sprites(all_sprites,food,snake,game):
    #draws all the sprites on the screen
    all_sprites.update(game,food)
    game.screen.fill((255,255,255))
    game.screen.blit(game.bg,(10,10))
    all_sprites.draw(game.screen)
    for i in range(len(snake.trail_arr)-1):
        game.screen.blit(snake_body,snake.trail_arr[i])
    display_score(snake,game)
    pygame.display.update()
def run(agent):
    trials=200
    counter_games=0
    running=True
    while counter_games<trials and running:
        game=Game(440,440)
        snake=Snake()
        food=Food() 
        all_sprites=pygame.sprite.Group()
        all_sprites.add(snake)
        all_sprites.add(food)
        draw_sprites(all_sprites,food,snake,game)
        game.clock.tick(game.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running=False
        while snake.game_crash!=True:
            pygame.event.get()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running=False
            cur_state=agent.get_state(game,snake,food)
            action=agent.act(cur_state)
            snake.update_position(action)
            new_state=agent.get_state(game,snake,food)
            draw_sprites(all_sprites,food,snake,game)
            if agent.train:
                reward=agent.set_reward(snake,food)
                agent.train_short_memory(cur_state,action,reward,new_state,snake.game_crash)
                agent.remember(cur_state,action,reward,new_state,snake.game_crash)
        if agent.train:
            agent.replay()
        counter_games+=1
        print(f'Game:{counter_games}         Score:{snake.body_size}')
    if train:
        agent.model.save_weights(agent.weights_path)
    pygame.quit()
        
if __name__=='__main__':
    #select either snake_weights or snake_weights2
    #snake_weights is more trained as compared to snake_weights2
    weights_path='E:\PythonProjects\SnakeGame\weights\snake_weights.hdf5'
    #set True if you want to use already trained model
    load_weights=True
    #set True if you want to continue training
    train=True
    agent=DQN(5,16,load_weights,weights_path,train)
    if load_weights:
        print("Weights Loaded")
    run(agent)

