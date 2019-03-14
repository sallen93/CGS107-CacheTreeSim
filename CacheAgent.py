# TODO: Still might need an uncertainty value to return to Arbitrator.

class Cache:
	def __init__(self, env, learning_rate, alpha, debug):
		self.learning_rate = learning_rate
		self.alpha = alpha
		self.env = env
		self.num_actions = env.num_actions
		self.uncertainty = 0				# Start with full uncertainty
		self.old_rpe = 1					# Holding variable for uncertainty calculation
		self.current_state = 0
		self.CACHE_DEBUG = debug
	
	# Get reward prediction error			
	def best_action(self, state):
		if self.CACHE_DEBUG:
			print("\t\tRPE Calc")
			print("\t\tState: ", state, " is terminal = : ", self.env.states[state].terminal)
		if not(self.env.states[state].terminal):  #or self.env.states[state].action_val_dict["lever"][1] < 0:
			max_q = 0
			max_a = ""
			for x in self.env.states[state].action_val_dict: 	#iterate through s' options
				#if self.self.CACHE_DEBUG:
					#print("Max-Q: ", max_q, "Q[x]: ", self.env.states[state].action_val_dict[x][0])
				if max_q < self.env.states[state].action_val_dict[x][0]: 
					# Potential bias here for last highest q-val if q-vals match.
					max_q = self.env.states[state].action_val_dict[x][0]
					max_a = x
				if self.CACHE_DEBUG:
					print("\t\tMax-Q: ", max_q, "Max-a: ", x)
			return x 
		else:
			return -1
	
	
	# Calculate new Q-value and uncertainty
	# Q = q + alpha(lr(R(s') + Q(s',a') - q))
	def Qsarsa(self, s, a, lr, alpha):
		if not(self.env.states[s].terminal):
			q, s_prime = self.env.states[s].action_val_dict[a]
			r = self.env.states[s_prime].reward
			a_p = self.best_action(s_prime)
			if a_p == -1:
				q_update = q + (alpha * (lr*(r - q)))
				if self.CACHE_DEBUG:
					print("\t\tReward: ", r, "\tUpdated Q-value: ", q_update)
				return q_update
				
				
			q_prime = self.env.states[s_prime].action_val_dict[a_p][0]
			rpe = r +  lr * (q_prime - q)
			q_update = q + (alpha * rpe)
			if self.CACHE_DEBUG:
				print("q' = ", q_prime)
			if self.CACHE_DEBUG:
				print("\t\tReward: ", r, "\tUpdated Q-value: ", q_update)
			return q + (alpha * (lr * (q_prime - q)))
		else:
			if self.CACHE_DEBUG:
				print("\t\tQsarsa: reached terminal state. R = ", q + (lr*(r - q)))
			return q + (alpha * (lr*(r - q)))
			
	# Decide on next move
	def get_next_action(self, state, lr, alpha):
		# Choose highest Q-value
		max_q = 0
		max_a = 0
		if not(self.env.states[state].terminal):    #action_val_dict["lever"][1] > 0:
			for x in self.env.states[state].action_val_dict: 	#iterate through s' options
				if max_q < self.env.states[state].action_val_dict[x][0]: 
					# Potential bias here for last highest q-val if q-vals match.
					max_q = self.env.states[state].action_val_dict[x][0]
					max_a = x
				if self.CACHE_DEBUG:
					print("\tMax-Q: ", max_q, "Max-a: ", x)
			
			
		if not(self.env.states[self.current_state].terminal):
			# Calculate udpated Q-value and change states 
			prev_q = self.env.states[self.current_state].action_val_dict[max_a][0]
			self.env.states[self.current_state].action_val_dict[max_a][0] = self.Qsarsa(state, max_a, lr, alpha)
			
			if self.CACHE_DEBUG:
					print("\tSTATE: ", self.current_state, 
							"\n\tAction: ", max_a,
							"\n\t\tOld Q-value: ", prev_q, 
							"\n\t\tNew Q-value: ", self.env.states[self.current_state].action_val_dict[max_a][0])
			self.current_state = self.env.states[self.current_state].action_val_dict[max_a][1]
		return max_a

	def run_task(self):
		depth = 1
		old_q1 = 0
		new_q1 = 0
		old_q2 = 0
		new_q2 = 0
		if self.num_actions == 2:	
			if self.current_state == 0 or self.current_state == 1:
				if self.CACHE_DEBUG:
					print("\tDepth: ", depth, "State: ", self.current_state)
				
				b_a = self.best_action(self.current_state)
				old_q1 = self.env.states[self.current_state].action_val_dict[b_a][0]
				action_taken = self.get_next_action(self.current_state, self.learning_rate, self.alpha)
				new_q1 = self.env.states[self.current_state].action_val_dict[action_taken][0]
				depth += 1
			if self.current_state == 0 or self.current_state == 1:
				if self.CACHE_DEBUG:
					print("\tDepth: ", depth, "State: ", self.current_state)
				
				b_a = self.best_action(self.current_state)
				old_q2 = self.env.states[self.current_state].action_val_dict[b_a][0]
				action_taken = self.get_next_action(self.current_state, self.learning_rate, self.alpha)
				new_q2 = self.env.states[self.current_state].action_val_dict[action_taken][0]
				depth += 1
				
			#print("CACHE_UNCERT: ", 1 - ((old_q1 - new_q1) + (old_q2 - new_q2)))
			
			self.uncertainty = 1 - ((old_q1 - new_q1) + (old_q2 - new_q2))
			self.current_state = 0
			# Return new states for logging
			return self.env.states[0].get_QA_Vals(self.env), self.env.states[1].get_QA_Vals(self.env), self.uncertainty

		return [-1,-1],[-1,-1]
	
	
	
	
	
	
	
	
	