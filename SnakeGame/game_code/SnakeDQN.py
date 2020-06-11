# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 12:01:13 2020

@author: Mbugush
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import random
import numpy as np
from  collections import deque
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
import pygame

class DQN:
    def __init__(self,actions,states,load_weights,weights_path,train):
        self.states=states
        self.actions=actions
        self.load_weights=load_weights
        self.weights_path=weights_path
        self.memory=deque(maxlen=2500)
        self.gamma=0.95
        self.epsilon=1
        self.epsilon_min=0.01
        self.epsilon_decay=0.995
        self.learning_rate=0.001
        self.batch_size=20
        self.train=train
        self.model=self.build_model()
    def build_model(self):
        model=Sequential()
        model.add(Dense(150,input_dim=self.states,activation='relu'))
        model.add(Dense(150,activation='relu'))
        model.add(Dense(150,activation='relu'))
        model.add(Dense(self.actions,activation='softmax'))
        model.compile(loss='mse',optimizer=Adam(lr=self.learning_rate))
        if self.load_weights:
           model.load_weights(self.weights_path)
        return model
    def get_state(self,game,snake,food):
        state=[
            #snake moving left,right,up or down
            snake.x_change==-20,
            snake.x_change==20,
            snake.y_change==-20,
            snake.y_change==20,
            #food on left,right,above or below snake
            snake.rect.topleft[0]>food.rect.topleft[0],
            snake.rect.topleft[0]<food.rect.topleft[0],
            snake.rect.topleft[1]>food.rect.topleft[1],
            snake.rect.topleft[1]<food.rect.topleft[1],
            #snake is almost leaving playarea boundary
            snake.rect.topleft[0]==20,
            snake.rect.topleft[0]==game.width-40,
            snake.rect.topleft[1]==20,
            snake.rect.topleft[1]==game.height-40,
            #snake is almost eating itself
            [snake.rect.topleft[0]+20,snake.rect.topleft[1]] in snake.trail_arr,
            [snake.rect.topleft[0]-20,snake.rect.topleft[1]] in snake.trail_arr,
            [snake.rect.topleft[0],snake.rect.topleft[1]+20] in snake.trail_arr,
            [snake.rect.topleft[0],snake.rect.topleft[1]-20] in snake.trail_arr
        ]
        #return an array of 0s and 1s instead of True/False
        for i in range(len(state)):
            state[i]=int(state[i])
        return np.array(state)
    def remember(self,state,action,reward,new_state,done):
        self.memory.append((state,action,reward,new_state,done))
    def replay(self):
        #adjusts network's weights according to 20 random samples from 
        #generated training data
        if len(self.memory)<self.batch_size:
            return
        samples=random.sample(self.memory,self.batch_size)
        for sample in samples:
            pygame.event.pump()
            state,action,reward,new_state,done=sample
            target=self.model.predict(np.array([state]))
            if done:
                target[0][action]=reward
            else:
                Q_future=np.amax(self.model.predict(np.array([new_state]))[0])
                target[0][action]=reward+Q_future*self.gamma
            self.model.fit(np.array([state]),target,epochs=1,verbose=0)
    def train_short_memory(self,state,action,reward,new_state,done):
        #adjusts networks weights according to most recent actions
        target=self.model.predict(np.array([state]))
        if done:
            target[0][action]=reward
        else:
            Q_future=np.amax(self.model.predict(np.array([new_state]))[0])
            target[0][action]=reward+Q_future*self.gamma
        self.model.fit(np.array([state]),target,epochs=1,verbose=0)
    def act(self,state):
        if self.train:
            #epsilon is set to give randomness of actions, allowing for
            #exploration
            self.epsilon*=self.epsilon_decay
            self.epsilon=max(self.epsilon_min,self.epsilon)
            if np.random.random()<self.epsilon:
                return random.randrange(self.actions)
            #predicts best actions according to network weights
            act_values=self.model.predict(np.array([state]))
            return np.argmax(act_values[0])
        else:
            act_values=self.model.predict(np.array([state]))
            return np.argmax(act_values[0])
    def set_reward(self,snake,food):
        self.reward=0
        if snake.game_crash:
            self.reward-=20
            return self.reward
        if snake.eaten:
            self.reward+=10
            return self.reward
        else:
            #minor rewards to give network feedback whether it's learning
            if snake.rect.x==food.rect.x:
                if snake.rect.y<food.rect.y:
                    if snake.y_change==20:
                        self.reward+=0.2
                        return self.reward  
                elif snake.rect.y>food.rect.y:
                    if snake.y_change==-20:
                        self.reward+=0.2
                        return self.reward  
            if snake.rect.y==food.rect.y:
                if snake.rect.x<food.rect.x:
                    if snake.x_change==20:
                        self.reward+=0.2
                        return self.reward 
                elif snake.rect.x>food.rect.x:
                    if snake.x_change==-20:
                        self.reward+=0.2
                        return self.reward  
        return self.reward
   