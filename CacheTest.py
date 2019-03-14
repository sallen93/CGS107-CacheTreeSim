from Environment import Environment, State
from CacheAgent import Cache
import random

'''	
# Simple test code
env = Environment(2, True)
cache = Cache(env, .5, .1, True)

#tree.run_task()
print("(",env.states[0].action_val_dict["lever"],", ",env.states[0].action_val_dict["magazine"],")")
print("(",env.states[1].action_val_dict["lever"],", ",env.states[1].action_val_dict["magazine"],")")
#print(env.states[0].action_val_dict["magazine"])
for x in range(25):
	print(cache.run_task())

'''


# Same as get_Averages except devalues R by val_reduct (R - val_reduct) halfway through each trial
def get_Averages_Deval(num_trials, cycles_per_trial, alpha, lr, write_to_file, filename, val_reduct):
	DEBUG = False
	
	env = Environment(2, True)
	cache = Cache(env, lr, alpha, DEBUG)
	
	# Holding arrays for calculation/final output
	# Arrays indexed by cycle of trial.
	s0_lever_avg = [0 for x in range(cycles_per_trial)]
	s0_magazine_avg = [0 for x in range(cycles_per_trial)]
	s1_lever_avg = [0 for x in range(cycles_per_trial)]
	s1_magazine_avg = [0 for x in range(cycles_per_trial)]
	
	# Generate data
	for x in range(num_trials):
		# Create new instance
		env = Environment(2, True)
		cache = Cache(env, True, lr, alpha, DEBUG)
		
		# Train on new environment / agent
		for c in range(cycles_per_trial):
		
			if random.randint(1,2) == 2:
				env.states[3].reward = val_reduct
		
			s0, s1 = cache.run_task()
			s0_lever, s0_magazine = s0
			s1_lever, s1_magazine = s1
			cache.current_state = 0
			
			# Add cycle
			s0_lever_avg[c] += s0_lever
			s0_magazine_avg[c] += s0_magazine
			s1_lever_avg[c] += s1_lever
			s1_magazine_avg[c] += s1_magazine
			
	# Divide elements by trial count to produce averages
	for x in range(cycles_per_trial):
		s0_lever_avg[x] /= num_trials
		s0_magazine_avg[x] /= num_trials
		s1_lever_avg[x] /= num_trials
		s1_magazine_avg[x] /= num_trials
		
		#print(s1_magazine_avg[x])
		
	# Output to file
	if write_to_file:
		filen = filename+"_C"+str(cycles_per_trial)+"_VR"+str(val_reduct)+"_A"+str(alpha)+"_LR"+str(lr)+".csv" #"_T"+str(num_trials)
		print("Data saved as ", filen)
		f = open(filen, "w")
		f.write("interval, s0_lever, s0_magazine, s1_lever, s1_magazine\n")
		
		for x in range(cycles_per_trial):
			new_row = str(x) + ", " + str(s0_lever_avg[x]) + ", " + str(s0_magazine_avg[x]) + ", " + str(s1_lever_avg[x]) + ", " + str(s1_magazine_avg[x]) + "\n"
			f.write(new_row)


def get_Averages(num_trials, cycles_per_trial, alpha, lr, write_to_file, filename):
	DEBUG = False
	
	env = Environment(2, True)
	cache = Cache(env, lr, alpha, DEBUG)
	
	# Holding arrays for calculation/final output
	# Arrays indexed by cycle of trial.
	s0_lever_avg = [0 for x in range(cycles_per_trial)]
	s0_magazine_avg = [0 for x in range(cycles_per_trial)]
	s1_lever_avg = [0 for x in range(cycles_per_trial)]
	s1_magazine_avg = [0 for x in range(cycles_per_trial)]
	uncertainty_avg = [0 for x in range(cycles_per_trial)]
	
	# Generate data
	for x in range(num_trials):
		# Create new instance
		env = Environment(2, True)
		cache = Cache(env, lr, alpha, DEBUG)
		
		for c in range(cycles_per_trial):
			s0, s1, uncertainty = cache.run_task()
			s0_lever, s0_magazine = s0
			s1_lever, s1_magazine = s1
			cache.current_state = 0
			
			# Add cycle
			s0_lever_avg[c] += s0_lever
			s0_magazine_avg[c] += s0_magazine
			s1_lever_avg[c] += s1_lever
			s1_magazine_avg[c] += s1_magazine
			uncertainty_avg[c] = uncertainty
			
	# Divide elements by trial count to produce averages
	for x in range(cycles_per_trial):
		s0_lever_avg[x] /= num_trials
		s0_magazine_avg[x] /= num_trials
		s1_lever_avg[x] /= num_trials
		s1_magazine_avg[x] /= num_trials
		uncertainty_avg[x] /= num_trials
		
		print(s0_lever_avg[x], s0_magazine_avg[x], s1_lever_avg[x], s1_magazine_avg[x], uncertainty_avg[x])
		
	# Output to file
	if write_to_file:
		filen = filename + "T"+str(num_trials)+"_C"+str(cycles_per_trial)+"_A"+str(alpha)+".csv"
		print("Data saved as ", filen)
		f = open(filen, "w")
		f.write("interval, s0_lever, s0_magazine, s1_lever, s1_magazine, uncertainty\n")
		
		for x in range(cycles_per_trial):
			new_row = str(x) + ", " + str(s0_lever_avg[x]) + ", " + str(s0_magazine_avg[x]) + ", " + str(s1_lever_avg[x]) + ", " + str(s1_magazine_avg[x]) + "\n"
			f.write(new_row)
		
		
#get_Averages_Deval(1000, 250, .5, .1, True, "ValReductStoch",.5)
get_Averages(1, 25, 1, .2, True, "Cache_UncertaintyTest")


	
	