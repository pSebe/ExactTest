from sys import argv
import numpy as np
from scipy.stats import entropy as KLdivergence

def prob_indep(counts, n):
# counts: (matrix) contingency table
# n:      (int)    sum of counts
	R = [sum(row) for row in counts]
	C = [sum([counts[i][j] for i in range(len(counts))]) for j in range(len(counts[0]))]
	prob = []
	for i in range(len(counts)):
		prob.append([])
		for j in range(len(counts[i])):
			prob[-1].append(0)
			prob[i][j] = R[i]*C[j]/n**2
	return prob

def total(counts):
# counts: (matrix) contingency table
	if len(counts)==0:
		return 0
	return sum(counts[0])+total(counts[1:])

def flatten(M):
	L = []
	for row in M:
		L = L + row
	return np.array(L)

def printv(str, flag="-v"):
	if flag in argv:
		print(str)

def MonteCarlo(KL, prob, n, sample_size=1E6, seed=0):
	np.random.seed(seed)
	printv("Sampling from H0...")
	sample = np.random.multinomial(n, prob, int(sample_size))
	printv("Calculating KL for samples...")
	KL_sample = np.array([KLdivergence(obs, prob, 2) for obs in sample])
	printv("Computing p-value..")
	p = (KL_sample >= KL).sum()/sample_size
	return p

def receive_cont_table(path):
	M = []
	with open(path, "r") as F:
		for line in F:
			M.append([int(x) for x in line.strip().split("\t")])
	return M

# receive input
printv("Receiving input...")
counts = receive_cont_table(argv[1])
n = total(counts)
# put expected (H0) and observed distributions in numpy arrays
printv("Calculating H0 distribution...")
exp = flatten(prob_indep(counts, n))
obs = flatten(counts)/n
# remove counts[i][j] where row i and col j are empty
printv("Removing rows/cols without counts...")
mask = np.argwhere(exp>0).flatten()
exp, obs = exp[mask], obs[mask]
# calculate KL-divergence and assess significance
printv("Calculating KL divergence...")
KL = KLdivergence(obs, exp, 2)
p = MonteCarlo(KL, exp, n)

print(p)
printv("KL="+str(KL), flag="-kl")
