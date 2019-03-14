from Environment import Environment, State
from CacheAgent import Cache
from TreeAgent import Tree
import random

class Arbiter:
	def __init__(self, env, cache_alpha, cache_lr, tree_df):
		self.cache = Cache(env, cache_alpha, cache_lr, False)
		self.tree = Tree(env, tree_df)
		#self.select_agent = ""
		#self.current_state = 0
		
		
	def run_task(self):
			cache_task = self.cache.run_task()
			tree_task = self.tree.run_task()
			
			c_s0, c_s1, c_u = cache_task
			t_s0, t_s1, t_u = tree_task
			
			if c_u > t_u:
				return cache_task, tree_task, "Cache"
			else:
				return cache_task, tree_task, "Cache"
			
			cache.current_state = 0
			tree.current_state = 0


def get_Averages(num_trials, cycles_per_trial, alpha, lr, discount_factor, write_to_file, filename):
	DEBUG = False
	
	env = Environment(2, True)
	
	# Holding arrays for calculation/final output
	# Arrays indexed by cycle of trial.
	c_s0_lever_avg = [0 for x in range(cycles_per_trial)]
	c_s0_magazine_avg = [0 for x in range(cycles_per_trial)]
	c_s1_lever_avg = [0 for x in range(cycles_per_trial)]
	c_s1_magazine_avg = [0 for x in range(cycles_per_trial)]
	
	t_s0_lever_avg = [0 for x in range(cycles_per_trial)]
	t_s0_magazine_avg = [0 for x in range(cycles_per_trial)]
	t_s1_lever_avg = [0 for x in range(cycles_per_trial)]
	t_s1_magazine_avg = [0 for x in range(cycles_per_trial)]
	
	t_u_avg = [0 for x in range(cycles_per_trial)]
	c_u_avg = [0 for x in range(cycles_per_trial)]
	
	# Generate data
	for x in range(num_trials):
		# Create new instance
		env = Environment(2, True)
		arb = Arbiter(env, alpha, lr, discount_factor)
		
		for c in range(cycles_per_trial):
			cache, tree, choice = arb.run_task()
			c_s0, c_s1, c_u = cache
			t_s0, t_s1, t_u = tree
			
			c_s0_lever, c_s0_magazine = c_s0
			c_s1_lever, c_s1_magazine = c_s1
			
			t_s0_lever, t_s0_magazine = t_s0
			t_s1_lever, t_s1_magazine = t_s1
			
			# Add cycle
			c_s0_lever_avg[c] += c_s0_lever
			c_s0_magazine_avg[c] += c_s0_magazine
			c_s1_lever_avg[c] += c_s1_lever
			c_s1_magazine_avg[c] += c_s1_magazine
			c_u_avg[c] += c_u
			
			t_s0_lever_avg[c] += t_s0_lever
			t_s0_magazine_avg[c] += t_s0_magazine
			t_s1_lever_avg[c] += t_s1_lever
			t_s1_magazine_avg[c] += t_s1_magazine
			t_u_avg[c] += t_u * 100000
			
	# Divide elements by trial count to produce averages
	for x in range(cycles_per_trial):
		c_s0_lever_avg[x] /= num_trials
		c_s0_magazine_avg[x] /= num_trials
		c_s1_lever_avg[x] /= num_trials
		c_s1_magazine_avg[x] /= num_trials
		c_u_avg[x] /= num_trials
		
		t_s0_lever_avg[x] /= num_trials
		t_s0_magazine_avg[x] /= num_trials
		t_s1_lever_avg[x] /= num_trials
		t_s1_magazine_avg[x] /= num_trials
		t_u_avg[x] /= num_trials
		
		#print(s1_magazine_avg[x])
		
	# Output to file
	if write_to_file:
		filen = filename + "T"+str(num_trials)+"_C"+str(cycles_per_trial)+".csv"
		print("Data saved as ", filen)
		f = open(filen, "w")
		f.write("interval, C_s0_lever, C_s0_magazine, C_s1_lever, C_s1_magazine, C_Unc, T_s0_lever, T_s0_magazine, T_s1_lever, T_s1_magazine, T_Unc\n")
		
		for x in range(cycles_per_trial):
			new_row_p1 = str(x) + ", " + str(c_s0_lever_avg[x]) + ", " + str(c_s0_magazine_avg[x]) + ", " + str(c_s1_lever_avg[x]) + ", " + str(c_s1_magazine_avg[x]) + ", " + str(c_u_avg[x]) + ", "
			new_row_p2 = str(t_s0_lever_avg[x]) + ", " + str(t_s0_magazine_avg[x]) + ", " + str(t_s1_lever_avg[x]) + ", " + str(t_s1_magazine_avg[x]) + ", " + str(t_u_avg[x]) + "\n"
			new_row = new_row_p1 + new_row_p2
			f.write(new_row)
		
		
#get_Averages(1000, 250, .00001, True, "TreeAVG")
get_Averages(1000, 250, .5, .1, .00001, True, "ArbiterAVG")