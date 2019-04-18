from random import random, choice, choices
from itertools import repeat
ALPHABET = "abcdefghijklmnopqrstuvwxyz"

def compare(ch1, ch2):
    return sum(x == y for x, y in zip(ch1, ch2))

def mutate(sample, selector, charfunc): #jajajajajajajajajaja das list
    return [old if select is False else charfunc() for old, select in zip(sample, selector)]

def next_father(goal, father, offspring, mutatefunc):
    childs = [mutatefunc(father) for _ in range(offspring)]
    childfit = [compare(goal, ch) for ch in childs]
    bestch = max(zip(childs, childfit), key=lambda x: x[1])
    return bestch[0]

def statistics(goal, father, child, selector):
    gmt, nmt, bmt = 0, 0, 0
    for idx, value in enumerate(selector):
        if value is not False:
            if father[idx] == goal[idx] != child[idx]: bmt += 1
            elif father[idx] != goal[idx] == child[idx]: gmt += 1
            else: nmt += 1
    return gmt, nmt, bmt

def random_selector(rate, lenght):
    return tuple(False if random() > rate else True for _ in range(lenght))

def keep_good_selector(goal, child):
    return tuple(False if x == y else True for x, y in zip(goal, child))

def random_char():
    return choice(ALPHABET)

def Weasel_Algorithm(goal, offspring, mutrate, original=True):
    '''Implementation of simple genetic algorithm derived from the Infinite Monkey Theorem.'''
    goalfitness = len(goal)
    father = choices(ALPHABET, k=goalfitness)
    fitness = compare(goal, father)
    iterations = 0
    generation_stats = []
    generation_fit = []
    
    if original:
        def my_selector():
            return random_selector(mutrate, goalfitness)
    else:
        def my_selector():
            return keep_good_selector(goal, father)
    
    while fitness != goalfitness:
        stats = (0, 0, 0)
        population = []
        for _ in range(offspring):
            selector = my_selector()
            child = mutate(father, selector, random_char)
            ch_stats = statistics(goal, father, child, selector)
            stats = tuple(x+y for x, y in zip(stats, ch_stats))
            population.append(child)
        
        childfit = [compare(goal, ch) for ch in population]
        bestchild = max(zip(population, childfit), key=lambda x: x[1])
        generation_stats.append(stats)
        generation_fit.append(bestchild[1])
        father = bestchild[0]
        fitness = bestchild[1]
        iterations += 1
        print(iterations, "".join(father), sep=": ")
    
    return "".join(father), generation_stats, generation_fit

def OracleTrick(goal):
    '''As pointed out in the paper "Efficient Per Query Information Extraction from Hamming Oracle" 
    (https://marksmannet.com/RobertMarks/REPRINTS/2010-EfficientPerQueryInformationExtraction.pdf)
    the efficiency of the process greatly depends on the election of our fitness function.
    If our oracle returns the position of the correct letters rather than the number of correct ones the whole process
    takes a maximum of 26 rounds.'''
    
    def Oracle(sample):
        return [x == y for x, y in zip(sample, goal)]
    
    lengoal = len(goal)
    father = choices(ALPHABET, k=lengoal)
    
    for letter in ALPHABET:
        correct = Oracle(repeat(letter, lengoal))
        father = [fatherletter if x is False else letter for fatherletter, x in zip(father, correct)]
    
    return "".join(father)

if __name__ == '__main__':
    print(Weasel_Algorithm("methinksitslikeaweasel", 100, 0.1)[0])
    print("OracleTrick", OracleTrick("methinksitslikeaweasel"), sep=": ")
    