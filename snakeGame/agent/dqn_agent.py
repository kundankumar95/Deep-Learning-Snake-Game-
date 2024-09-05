import numpy as np
import random
from collections import deque
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten

def build_model(input_shape, action_space):
    model = Sequential([
        Flatten(input_shape=input_shape),
        Dense(24, activation='relu'),
        Dense(24, activation='relu'),
        Dense(action_space, activation='linear')
    ])
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.001), loss='mse')
    return model

class DQNAgent:
    def __init__(self, state_shape, action_space, batch_size=64, memory_size=10000, gamma=0.99):
        self.state_shape = state_shape
        self.action_space = action_space
        self.batch_size = batch_size
        self.memory = deque(maxlen=memory_size)
        self.gamma = gamma
        self.model = build_model(state_shape, action_space)
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_space)
        q_values = self.model.predict(np.expand_dims(state, axis=0))
        return np.argmax(q_values[0])

    def replay(self):
        if len(self.memory) < self.batch_size:
            return

        minibatch = random.sample(self.memory, self.batch_size)
        states, actions, rewards, next_states, dones = zip(*minibatch)

        states = np.array(states)
        next_states = np.array(next_states)
        actions = np.array(actions)
        rewards = np.array(rewards)
        dones = np.array(dones)

        q_values_next = np.amax(self.model.predict(next_states), axis=1)
        targets = rewards + self.gamma * q_values_next * (1 - dones)

        q_values = self.model.predict(states)
        for i in range(self.batch_size):
            q_values[i][actions[i]] = targets[i]

        self.model.fit(states, q_values, epochs=1, verbose=0)

        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
