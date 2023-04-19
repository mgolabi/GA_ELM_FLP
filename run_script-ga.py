from GA_ELM import *
from GA import *
import objective_function as OF
import csv


if __name__ == '__main__':

    #problems = ["Node200", "Node300", "Node400", "Node500", "Node600", "Node700"]
    problems = ["Node200"]
    num_run = 1

    for i in problems:
        if i == "Node200":
            obj_name = OF.NODEE200().evaluate
            dim_ = len(OF.NODEE200().Candidate_List)
            f = open('Node200result_ga.csv', 'w')
            writer = csv.writer(f)
        elif i == "Node300":
            obj_name = OF.NODEE300().evaluate
            dim_ = len(OF.NODEE300().Candidate_List)
            f = open('Node300result_ga.csv', 'w')
            writer = csv.writer(f)
        elif i == "Node400":
            obj_name = OF.NODEE400().evaluate
            dim_ = len(OF.NODEE400().Candidate_List)
            f = open('Node400result_ga.csv', 'w')
            writer = csv.writer(f)
        elif i == "Node500":
            obj_name = OF.NODEE500().evaluate
            dim_ = len(OF.NODEE500().Candidate_List)
            f = open('Node500result_ga.csv', 'w')
            writer = csv.writer(f)
        elif i == "Node600":
            obj_name = OF.NODEE600().evaluate
            dim_ = len(OF.NODEE600().Candidate_List)
            f = open('Node600result_ga.csv', 'w')
            writer = csv.writer(f)
        else:
            obj_name = OF.NODEE700().evaluate
            dim_ = len(OF.NODEE700().Candidate_List)
            f = open('Node700result_ga.csv', 'w')
            writer = csv.writer(f)

        for j in range(0, num_run):
            dd = [i, j]

            #For implementing classical GA
            #a, b, c = genetic_algorithm(cost_function=obj_name, dimension=dim_, maximum_iterations=50000, population=None,
            #     population_size=500, selection_rate=0.8, mutation_rate=0.05)

            #For applying GA-ELM
            a, b, c, d, e = ga_elm(cost_function=obj_name, dimension=dim_, maximum_iterations=50000, population=None,
                 population_size=500, selection_rate=0.8, mutation_rate=0.05, no_of_real_iterations=2, percent_real=0.1)
            # print(a, b, c, d, e)
            dd = dd+[b, c]
            print(dd)
            writer.writerow(dd)
        f.close()


    #a, b, c, d, e = ga_elm(cost_function=OF.NODEE700().evaluate, dimension=90, maximum_iterations=80, population=None, population_size=20,
                      #selection_rate=0.8, mutation_rate=0.05, no_of_exact_iterations=2, percent_elm= 0.5)
    #print(a, b, c, d, e)
    #ddd = [b, c, e]
    #print(ddd)
     #a, b, c = genetic_algorithm(cost_function=OF.NODEE200().evaluate, dimension=20, maximum_iterations=20, population=None, population_size=5,
                       #selection_rate=0.8, mutation_rate=0.05)
     #print(a, b, c)