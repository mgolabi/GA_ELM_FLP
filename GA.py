from multiprocessing import Pool
import numpy as np
import random
import time

def genetic_algorithm(cost_function=None, dimension=None, maximum_iterations=None, population=None, population_size=None, selection_rate=None, mutation_rate=None):
    start_ = time.time()
    # we need to initialize the population if it is needed
    if population is None:
        population = np.zeros((population_size, dimension), dtype=float)
        for i in range(population_size):
            population[i] = population[i] = np.random.uniform(low=0.0, high=1.0, size=dimension)

    # We prefer to run the experiments in parallel
    pool = Pool(processes=16)
    # The cost function for all the members in the
    # population will be calculated in parallel.
    cost = pool.map(cost_function, population)

    # Let's find the best objective value and
    # best member in the population
    ind = np.argsort(cost).astype(dtype=int)
    cost = np.sort(cost)
    population = population[ind, :]

    iterations = population_size

    # We define the keep ratio
    keep = int(np.floor(selection_rate * population_size))

    # The stopping criterion is set to be a
    # maximum number of iterations
    while iterations < maximum_iterations:
        # The variable M is used to define the number
        # of matings
        M = (population_size - keep) // 2

        # In the following lines, we use a
        # simple roulette  selection strategy
        *iterats, = range(1, keep + 1)
        probs = np.flipud(iterats / np.sum(iterats))

        *indexes, = range(len(probs))
        ma_index = np.random.choice(indexes, keep // 2, replace=True, p=probs)
        pa_index = np.random.choice(indexes, keep // 2, replace=True, p=probs)

        *ixs_1, = range(keep, population_size, 2)
        *ixs_2, = range(keep + 1, population_size, 2)

        # The crossover points will be executed randomly
        cps_1 = np.random.randint(0, dimension - 1, size=M)
        cps_2 = np.random.randint(0, dimension, size=M)

        for cp_1, cp_2, ip, im, ipa, ima in zip(cps_1, cps_2, ixs_1, ixs_2, pa_index, ma_index):
            # If cp_1 and cp_2 points are equal, we do a single point crossover
            if cp_1 == cp_2:

                population[im] = population[ima, :]
                population[ip] = population[ipa, :]

                for i in range(cp_1, dimension):
                    if not population[ipa, i] in population[ima]:
                        population[im, i] = population[ipa, i]
                    cp2 = dimension - cp_1 - 1
                    if not population[ima, cp2] in population[ipa]:
                        population[ip, cp2] = population[ima, cp2]
            else:
                # Otherwise, we apply a two-point crossover
                if cp_1 > cp_2:
                    cp_1, cp_2 = cp_2, cp_1

                population[im] = population[ima, :]
                population[ip] = population[ipa, :]

                for i in range(cp_1, cp_2):
                    if not population[ipa, i] in population[ima]:
                        population[im, i] = population[ipa, i]

                    if not population[ima, i] in population[ipa]:
                        population[ip, i] = population[ima, i]

        # In the next few lines, we will randomly apply three types of
        # mutation on the population
        nmut = int((population_size - 1) * dimension * mutation_rate)

        mrows = np.random.randint(1, population_size, size=nmut)
        #mcols = np.random.randint(0, dimension, size=nmut)
        for row in mrows:
            rand = np.random.uniform()
            #swap operator
            if rand < 0.33:
                mcols = np.random.randint(0, dimension, size=2)
                population[row][mcols[0]], population[row][mcols[1]] = population[row][mcols[1]], population[row][mcols[0]]
            #inverse operator
            elif (rand>=0.33 and rand<0.66):
                a = random.randint(0, dimension)
                b = random.randint(0, dimension)
                aa = min(a, b)
                bb = max(a, b)
                population[row][aa:bb] = population[row][aa:bb][::-1]
            #mutate by randomly changing the values of selected items
            else:
                numb = random.randint(1, round(dimension / 10))
                mcols = np.random.randint(0, dimension, size=numb)
                for cols in mcols:
                    population[row][cols] = np.random.uniform()


        # Let's call the cost function for all the individuals
        cost = pool.map(cost_function, population)

        population = np.asarray(population)
        cost = np.asarray(cost)

        # The population need to be sorted since we are using
        # roulette while
        ind = np.argsort(cost)
        cost = cost[ind]
        population = population[ind, :]

        # The number of function evaluations should
        # be updated at the end of each iteration
        iterations = iterations + population_size
        timee = time.time()-start_

    return population[0], cost[0], timee
