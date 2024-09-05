import numpy as np
from game.snake_game import SnakeGame, WIDTH, HEIGHT, BLOCK_SIZE
from agent.dqn_agent import DQNAgent

def preprocess_state(state):
    # Flatten the state for the neural network
    return np.reshape(state, (WIDTH // BLOCK_SIZE, HEIGHT // BLOCK_SIZE, 1))

def train_agent(episodes):
    env = SnakeGame()
    agent = DQNAgent((WIDTH // BLOCK_SIZE, HEIGHT // BLOCK_SIZE, 1), 4)
    for episode in range(episodes):
        state = env.reset()
        state = preprocess_state(state)
        done = False
        total_reward = 0

        while not done:
            action = agent.act(state)
            next_state, reward, done = env.step(action)
            next_state = preprocess_state(next_state)
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            total_reward += reward

            if done:
                print(f"Episode {episode + 1}: Total reward: {total_reward}")

            agent.replay()

        if episode % 10 == 0:
            print(f"Episode {episode}: Epsilon {agent.epsilon:.2f}")

    env.close()

if __name__ == "__main__":
    train_agent(1000)
