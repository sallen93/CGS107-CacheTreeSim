# Simulation environment
import random

class State:
	# This constructs individual states. 
	# Reward(integer) determines the reward value of reaching a state.
	# Terminal(Boolean) says whether or not the state is terminal (Cache) or a leaf (Tree)
	# Actions(integer 2 or 3) specifies  which test you are running. 2 = lever/mag 3 = lever/mag/chain
	def __init__(self, reward, terminal, num_actions):
		self.reward = reward
		self.terminal = terminal
		self.num_actions = num_actions
		
		# initialize all Q-values to 0 in action-value(indexed by action name)
		# [Q-value, s']
		
		if num_actions == 2:
			self.action_val_dict = {
				"lever" : [0,0],
				"magazine" : [0,0]
			}
		if num_actions == 3:
			self.action_val_dict = {
				"lever" : [0,0],
				"magazine" : [0,0],
				"chain" : [0,0]
			}
	
	# Updates the newly calculated Q-values
	def updateValue(action, value):
		self.action_val_list[action] = value
		
	def get_QA_Vals(self, num_actions):
		lever = self.action_val_dict["lever"][0]
		magazine = self.action_val_dict["magazine"][0]
		if num_actions == 3:
			chain = self.action_val_dict["chain"][0]
			return lever, magazine, chain
		return lever, magazine
		
# Creates the state environment for agent to work in.
# TODO: Make 3-action env
class Environment:
	def __init__(self, num_actions,stoch):
		self.states = []
		self. num_actions = num_actions
		# 2-action experiment
		if self.num_actions == 2:
			self.states.append(State(0,False,2))
			self.states.append(State(0,False,2))
			self.states.append(State(0,True,2))
			self.states.append(State(1,True,2))
			
			if stoch == True:
				# Set s-s'/action-reward pairs
				stoch_range = 1
				# s0
				self.states[0].action_val_dict["lever"] = [random.uniform(.1, stoch_range), 1] # Go to s1
				self.states[0].action_val_dict["magazine"] = [random.uniform(.1, stoch_range), 2] # Go to s2
				# s1
				self.states[1].action_val_dict["lever"] = [random.uniform(.1, stoch_range), 2] # Go to s2
				self.states[1].action_val_dict["magazine"] = [random.uniform(.1, stoch_range), 3] # Go to s3 (Reward!)
				# s2
				self.states[2].action_val_dict["lever"] = [0, -1] # Reference end with -1
				# s3
				self.states[3].action_val_dict["lever"] = [0, -1] # Reference end with -1
			else:
				# Set s-s'/action-reward pairs
				# s0
				self.states[0].action_val_dict["lever"] = [0, 1] # Go to s1
				self.states[0].action_val_dict["magazine"] = [0, 2] # Go to s2
				# s1
				self.states[1].action_val_dict["lever"] = [0, 2] # Go to s2
				self.states[1].action_val_dict["magazine"] = [0, 3] # Go to s3 (Reward!)