# Why_Would_You_Do_That
SnT Project 2021, Cognitive Revolutionaries, Brain and Cognitive Society

# Authors
1. [Akanksha Singh](https://github.com/s-akanksha "Akanksha Singh's GitHub Profile")
2. [Suyash Mallik](https://github.com/zapmonkey02 "Suyash Mallik's Github Profile")

Under Mentor [Shivanshu Tyagi](https://github.com/spazewalker "Shivanshu Tyagi's Github Profile")

# Motivation

To study the evolution and spread of altruism in a large population by simulating an artificial environment with agents that are subject to a certain set of rules for survival and reproduction. These agents can pick and choose between combinations of different strategies and our goal is to find a set of conditions that are conducive to the development of altruistic strategies that are beneficial to the individual agent as well. In particular, we aim to study the development, viability and trade-offs of recognition systems and memory, and their impact on the development of altruistic strategies. 

# Progress

1. Understanding Game theory: Agents’ outcomes depend on not only their own but also other agents’ decisions. 
2. Understanding altruism and its types and reading some papers on how it emerges: Cook’s dilemma, Green beard altruism etc.
3. Learning the basics of Python, Pytorch, Numpy.
4. Designing a Simulation
5. Implementing the simulation in Python
6. Reading about Deep Learning
7. Learning about Reinforcement learning
8. Implementing a Q-deep learning Model

# Desgining a Simulation

We designed a system where agents had a prisoner’s dilemma problem with cooperation and defection as options: 

|   P1/P2   | Cooperate | Defect |
| --------- | --------- | ------ |
| Cooperate |    1,1    |   0,2  |
|  Defect   |    2,0    |0.5, 0.5|


Our model comprises of 3 types of agents:


1. Always Cooperative.
2. Always defect.
3. Maintain a record of their last interaction with every other agent and reciprocate their previous actions. If they have had no previous interactions, they decide randomly.
4. Always choose randomly.


Agents of type 3 need extra food to maintain these records and their memories are refreshed after a fixed duration of time. The amount of extra food needed, interval for memory refreshal, number of units of food needed to survive and reproduce can be varied to study how recognition systems impact altruism under different environmental constraints.

# Python Implementation Of Simulation

We created separate classes for:

1. Agents
2. Environment
3. Tree having two member variables: Agent1 & Agent2 that store the id’s of the agents on the tree

We create a list of agents and assign them IDs equal to their index in the list. We also create an array of trees.

Each day, we run a set number of iterations. During one iteration, for each agent we first randomly decide whether it will get food, and if yes, we will randomly place it on a particular tree and store its id in the tree’s member variable.

After doing this for each agent we go tree by tree in the trees list and compute the results of the interaction between the agents on each tree.

1. If there is only one agent on a tree, agent’s food gets incremented by 2
2. If there are two agents on a tree, their food values are altered based on their interaction and agent_type. If the agent is of type3, its memory is also updated.

After each day, agents with less than the amount of food needed to live(livereq) die, and their is_alive attribute is changed to False. Out of those left alive, those who are of type3 and do not have enough extra units of food to maintain memory will have their memories cleared. Then, for those alive, we check if they have enough food to reproduce(repreq) and create another agent of the same type if they do. Then, the age of each agent alive is incremented. Further, the agents who have completed their reset period will also have their memories cleared.

# Results of the Simulation

In this simulation, always-cooperative agents had a significant advantage and fared best among all types. With no facial recognition or memory based agents, always defective agents take over and always-cooperative agents die off. However, our simulation explains how altruistic traits evolved and are present in different species, like humans, because of the reward they receive from memory-based agents and because defective agents or ‘cheaters’ are punished by them. Thus, our simulation gives a scenario in which the very counterintuitive evolution and survival of altruistic agents becomes plausible. 

# Training an Agent 

Now we aim to design an agent that can choose the best course of action to maximise its chances of survival and reproduction, using reinforcement learning. The TFT strategy is the best strategy if the agent has memory and recognition. However, given the agent does not have the ability to identify and remember other agents, we trained it to pick the best choice using Deep Q learning, having only the state parameters as available information. State parameters do not completely define the state but are the values that are available to the agent for it to decide its action. A state will have all three types of agents and an ‘interaction history’ array for storing the previous interactions of all type3 agents with our agent. 

# Deep-Q learning

Q-value is the estimated value of long term reward for a particular action performed by the agent in a particular state. We build a neural network to calculate Q value for each possible action(cooperate/defect) for given state parameters. The neural network will have the state parameters as input and the Q values for the two possible actions as output. The state parameters to be used as input would be:

1. The number of times agent has cooperated in the past
2. The number of times agent has defected in the past
3. The number of times agent has faced cooperation
4. The number of times agent has faced defection

In the implementation, when we randomly initialize a state, we first pick random values for all types of agents, and all state parameters. Then, while creating the interaction history, we consider that the number of co-operations and defections done by our agent against the type3 agents are in proportion to (type3/type1+type2+type3), and then initialize the interaction history. This gives a better picture of how past actions of the agent affect the future interactions. 

Now, to train the neural network we would need target Q-values so that we can calculate a loss function. This target Q value is calculated using the following formula:

                                                    Target  = reward + (gamma)max(Q(s’,a))

Where reward is the immediate reward on performing the action, gamma is the discount rate, s’  is the new state after action a1 was performed on state s. Max(Q(s’,a)) is the maximum Q value(according to current weights) in state s’ for any action. Thus, this Q value will eventually converge to the correct Q value. We used the hubber’s loss function to train our model. 

Now, we randomly initialize the weights and initial state. Then, the agent performs actions based on ‘exploration rate’. It chooses to explore or exploit based on exploration rate. Exploration means randomly choosing an action and exploitation means choosing the action with the maximum Q value according to current weights. The exploration rate gradually decreases with each cycle, as it is beneficial for the agent to explore in the beginning when the Q values aren’t very accurate and to exploit when the Q values are close to convergence. With every action, we keep storing the state,action, immediate reward and next_state as a ‘step’ in the memory. Then, after a fixed number of steps, we randomly pick a minibatch of steps and use it to train our model. 

This is how we successfully determine the Q value for each action for each possible state and have an agent which can pick the best choice for itself. 
 
 # Conclusions
 
We successfully designed and implemented a scenario in which altruistic strategies are evolutionarily successful which can act as a crucial key in the study of altruism in different species. We also learnt about deep learning and reinforcement learning and designed a Deep-Q learning model that trains an agent who does not have identification ability to pick the best strategy and maximise its long term survival and propagation. This project helped us expand our knowledge and managed to achieve its goals of studying altruism and survival in biological systems using python and Reinforcement learning.








