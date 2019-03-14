class Tree:
	def __init__(self, env, discount_factor):
		self.env = env
		self.discount_factor = discount_factor
		self.current_state = 0
		self.uncertainty = 1
		self.last_update = 0
		
	def run_task(self):
		depth = 1	
		while not(self.env.states[self.current_state].terminal):
			action_taken = self.get_next_action(self.current_state, self.discount_factor)
			depth += 1
		self.current_state = 0
		
		# Return new states for logging
		return self.env.states[0].get_QA_Vals(self.env), self.env.states[1].get_QA_Vals(self.env), self.uncertainty	
		
	# Decide on next move
	def get_next_action(self, s, discount_factor):
		# Get next action
		a = ""
		if self.env.states[s].action_val_dict["lever"][0] > self.env.states[s].action_val_dict["magazine"][0]:
			a = "lever"
		else:
			a = "magazine"
			
		# Update q-value of a with Bellman evaluation
		s_prime = self.env.states[s].action_val_dict[a][1]
		q_update = discount_factor * (self.Finite_Bellman(s_prime) - self.env.states[s].action_val_dict[a][0])
		
		self.uncertainty = (self.last_update - q_update)
		#print("Uncertainty: ", self.uncertainty)
		
		self.env.states[s].action_val_dict[a][0] += q_update
		self.current_state = self.env.states[s].action_val_dict[a][1]
		
	# This equation and environment are deterministic, so T(s, a, s') = 1.
	# Reduced equation = V_pi(s) = R(s,pi(s)) + eps[s' in S](discount_factor * V*(s'))
	def Finite_Bellman(self, s):
		#Hard coding formula recursion with if statements do to env smimplicity
		#For all s'
		# sum R(s') + Q-val of best next action (if term q = R)
		if self.env.states[s].terminal:
			#print("Terminal")
			return self.env.states[s].reward #* discount_factor
		
		Qfwd = 0
		for x in range(2):#self.env.states[s].action_val_dict[x][0]:
			if x == 0:
				a = "lever"
			else:
				a = "magazine"
			s_prime = self.env.states[s].action_val_dict[a][1] # s'
			rs_prime = self.env.states[s_prime].reward
			q_prime = self.max_a_q(s_prime)
			
			Qfwd += rs_prime + q_prime
		
		return Qfwd
		
	# get and return reward/Q-value
	def R(self, s, a):
		if a == 0:
			a = "lever"
		if a == 1:
			a = "magazine"
		return self.env.states[s].action_val_dict[a][0]		
		
	def max_a_q(self, s):
		if self.env.states[s].action_val_dict["lever"][0] > self.env.states[s].action_val_dict["magazine"][0]:
			return self.env.states[s].action_val_dict["lever"][0]
		else:
			return self.env.states[s].action_val_dict["magazine"][0]
		
		
		
		
		
		
		
		