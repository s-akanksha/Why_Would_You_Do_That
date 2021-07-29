import random
import gym
import numpy as np
from collections import deque
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras import backend as K
import random as rand

import tensorflow as tf

EPISODES = 5000

class env:
  def __init__(self):
    self.state_size = 4
    self.action_size = 2
    self.num_agent_1 = 0
    self.num_agent_2 = 0
    self.num_agent_3 = 0
    self.interaction_history = []
    self.coop = 0
    self.defect = 0
    self.face_coop = 0
    self.face_defect = 0
    self.state = [self.coop,self.defect,self.face_coop,self.face_defect]
  
  def reset(self):
    self.num_agent1 = rand.randint(1,100)
    self.num_agent2 = rand.randint(1,100)
    self.num_agent3 = rand.randint(1,100)
    self.interaction_history = np.zeros(self.num_agent3)
    self.coop = rand.randint(1,100)
    self.defect = rand.randint(1,100)
    self.face_coop = rand.randint(1,100)
    self.face_defect = rand.randint(1,100)
    proportion = self.num_agent3/(self.num_agent1+self.num_agent2+self.num_agent3)
    for i in range(int(self.coop*proportion)):
      k = rand.randint(1,self.num_agent3)-1
      if self.interaction_history[k]!=1:
        self.interaction_history[k]=1
    for i in range(int(self.defect*proportion)):
      k = rand.randint(1,self.num_agent3)-1
      if self.interaction_history[k]!=-1:
        self.interaction_history[k]=-1
    self.state = [self.coop,self.defect,self.face_coop,self.face_defect]
    return self.state

  def step(self,action):
    if action==0:
      action = -1
    encounter = rand.randint(1,self.num_agent1+self.num_agent2+self.num_agent3)
    partner_does = 0
    if encounter<self.num_agent1:
      partner_does = 1
    if encounter>self.num_agent1 and encounter<self.num_agent2+self.num_agent1:
      partner_does = -1
    if encounter>self.num_agent1+self.num_agent2:
      partner_does = self.interaction_history[encounter-self.num_agent1-self.num_agent2-1]
      self.interaction_history[encounter-self.num_agent1-self.num_agent2-1] = action
    if partner_does == 0:
      partner_does = rand.choice([-1,1])
    reward = 0 #initialize reward 0
    if partner_does == 1:
      self.face_coop+=1
      if action == 1:
        reward = 1
      if action == -1:
        reward = 2
    if partner_does == -1:
      self.face_defect+=1
      if action == 1:
        reward = 0
      if action == -1:
        reward = 0.5
    if action == 1:
      self.coop+=1
    else:
      self.defect+=1
    self.state = [self.coop,self.defect,self.face_coop,self.face_defect]
    return state, reward
    
class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95    # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.99
        self.learning_rate = 0.001
        self.model = self._build_model()
        self.target_model = self._build_model()
        self.update_target_model()

   
    def _huber_loss(self, y_true, y_pred, clip_delta=1.0):
        error = y_true - y_pred
        cond  = K.abs(error) <= clip_delta

        squared_loss = 0.5 * K.square(error)
        quadratic_loss = 0.5 * K.square(clip_delta) + clip_delta * (K.abs(error) - clip_delta)

        return K.mean(tf.where(cond, squared_loss, quadratic_loss))

    def _build_model(self):
        # Neural Net for Deep-Q learning Model
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss=self._huber_loss,
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def update_target_model(self):
        # copy weights from model to target_model
        self.target_model.set_weights(self.model.get_weights())

    def memorize(self, state, action, reward, next_state):
        self.memory.append((state, action, reward, next_state))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return rand.choice([0,1])
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])  # returns action

    def replay(self, batch_size):
        minibatch = random.sample(self.memory, batch_size)
        for state, action, reward, next_state in minibatch:
            target = self.model.predict(state)
            t = self.target_model.predict(next_state)[0]
            target[0][action] = reward + self.gamma * np.amax(t)
            # target[0][action] = reward + self.gamma * t[np.argmax(a)]
            self.model.fit(state, target, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def load(self, name):
        self.model.load_weights(name)

    def save(self, name):
        self.model.save_weights(name)


if __name__ == "__main__":
    env = env()
    state_size = 4
    action_size = 2
    agent = DQNAgent(state_size, action_size)
    batch_size = 32

    for e in range(EPISODES):
        state = env.reset()
        state = np.reshape(state, [1, state_size])
        for time in range(500):
            action = agent.act(state)
            next_state, reward = env.step(action)
            next_state = np.reshape(next_state, [1, state_size])
            agent.memorize(state, action, reward, next_state)
            state = next_state
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)
     
    state = env.reset()
    string = input("Run simulation with trained agvent?")
    if string == "yes":
      for i in range (50):
        print(env.num_agent1,env.num_agent2,env.num_agent3,env.interaction_history)
        action = agent.act(state)
        print(action)
        next_state, reward = env.step(action)
        print(reward)
        next_state = np.reshape(next_state, [1, state_size])
        agent.memorize(state, action, reward, next_state)
        state = next_state
