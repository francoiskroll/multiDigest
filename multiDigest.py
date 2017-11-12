# COMPLETE DIGEST RESTRICTION MAPPING WITH TWO OR MORE ENZYMES
# Francois Kroll
# 06/03/2017

import itertools
from itertools import product

# INPUT
# _frags are the lengths of the fragments we obtain after complete digestion
    # e.g. e1_frags are the lengths of the fragments obtained after complete digestion by enzyme 1
k = 3 # number of enzymes
e1_frags = [2, 7, 9]
e2_frags = [4, 4, 5, 5]
e3_frags = [2, 16]
e_frags = [e1_frags, e2_frags, e3_frags] # list of lists gathering the k sets of fragments
all_frags = [2, 2, 2, 2, 2, 3, 5] # lengths of the fragments obtained after complete digestion by all k enzymes combined

# for a different number of enzymes:
    # change k to the number of enzymes
    # delete or add (an) e_frags list(s) (e.g. delete e3_frags or add e4_frags)
    # change e_frags correspondingly

# ALGORITHM
# Generates all possible permutations of fragments inside one set of fragments (e.g. e1_frags)
def frags2permutations (frags):
    return map(list, itertools.permutations(frags))

# Converts one of the permutations generated by frags2permutations into its corresponding sites
    # more precisely: into its corresponding enzyme-specific restriction sites map
def oneperm2sites (perm):
    sites = [0]
    for i in range (0, len(perm)):
        sites.append (sites[i] + perm[i])
    return sites

# Converts all possible permutations of one set of fragments into their corresponding enzyme-specific restiction sites maps
    # i.e. a generalization of oneperm2sites for all permutations of one set
def allpermutations2allsites (permutations):
    allsites = []
    for p in permutations:
        allsites.append (oneperm2sites (p))
    return allsites

# From a combination of k possible enzyme-specific restriction sites map, generates the fragments we would obtain if the enzymes were combined
    # in other words, it generates the virtual all_frags list we would obtain
# all_sites is the virtual full restriction sites map i.e. the sum of the k enzyme-specific restriction sites maps
# all_frags_test is the virtual all_frags set we would have obtained with this full restriction sites map
        # it is called test because we are going to test it against the real all_frags set we received as input
def sites2allfrags (combination):
    all_sites = list(itertools.chain.from_iterable(combination))
    all_sites.sort()
    all_frags_test = [x - all_sites[i - 1] for i, x in enumerate(all_sites)][1:]
    all_frags_test = filter (lambda a: a != 0, all_frags_test)
    all_frags_test.sort()
    return all_frags_test

# From all possible combinations of enzyme-specific restriction sites maps,
# checks if the fragments we would obtain with the k enzymes combined (i.e. the virtual all_frags = all_frags_test) are the same as the real fragments we received as input (i.e. all_frags)
# if they are the same, then we have a potential correct answer i.e. enzyme-specific restriction sites maps that are compatible with the input fragments sets
def filterCorrectAnswers (sites):
    for combination in list(product(*sites.values())):
        combination = list(combination)
        if set(combination[0]).intersection(*combination) == set([0, sum(all_frags)]):
        # checks if there are no sites in common between the k enzyme-specific restriction sites maps (other than 0 and the width of the original sequence)
        # indeed, restriction sites are entirely enzyme-specific
            possible_answer = sites2allfrags (combination)
            possible_answer = filter (lambda a: a != 0 and a != sum(all_frags), possible_answer)
            if set(possible_answer) == set(all_frags):
            # checks if the virtual fragments we generated are the same as the real fragments we received
            # we have a potential solution if that is the case
                for e in range (1, k+1):
                    print 'Enzyme %i restriction sites:' %(e), filter (lambda a: a != 0 and a != sum(all_frags), combination [e-1])
                print 'Restriction sites map: ', filter (lambda a: a != 0 and a != sum(all_frags), sorted(list(itertools.chain.from_iterable(combination))))
                print ''
                #return # to have all possible solutions, remove this return statement


permutations = {} # dictionary that will hold all the possible permutations of one set of fragments
sites = {} # dictionary that will hold all the enzyme-specific restriction sites maps

# fills in the permutations dictionary
for frags in e_frags:
    permutations ['e%i' % (e_frags.index (frags) + 1)] = frags2permutations(frags)

# fills in the sites dictionary
for i in range (1, k+1):
    sites ['e%i' % (i)] = allpermutations2allsites (permutations ['e%i' % (i)])

filterCorrectAnswers (sites)
