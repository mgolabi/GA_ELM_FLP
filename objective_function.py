import pandas as pd
from random import choice
import numpy as np


class Eval():
    def __init__(self, Candidate_List, df_shortest, df_edge, opened_list, p: int):
        self.p = p
        self.Candidate_List = Candidate_List
        self.df_shortest = df_shortest
        self.df_edge = df_edge
        self.opened_list = opened_list


    def eval(self):
        Travel = 0

        df_short_new = self.df_shortest[self.opened_list]

        bvu = np.zeros((len(self.df_edge.values), 2))
        gamma_j = dict.fromkeys(self.opened_list, 0)
        #gamma_bar_j = dict.fromkeys(self.opened_list, 0)
        #ro_j = dict.fromkeys(self.opened_list, 0)
        #L_bar = dict.fromkeys(self.opened_list, 0)
        #w_j = dict.fromkeys(self.opened_list, 0)
        #lost_j = dict.fromkeys(self.opened_list, 0)

        for i in range(0, len(self.df_edge.values)):
            x, y = eval(self.df_edge["Edges"][i])
            travel_x = 0
            travel_y = 0
            gamma_x = 0
            gamma_y = 0

            if list(df_short_new.loc[x, :]) and list(df_short_new.loc[y, :]):

                # Find closest open facility to x
                closest_dist_x = min(df_short_new.loc[x, :])
                # print(closest_dist_x)
                row_x = df_short_new.iloc[x]
                ind_set_x = row_x.reset_index().set_index(x).loc[closest_dist_x]
                if len(ind_set_x) > 1:
                    ind_set_x.index = [x for x in range(0, len(ind_set_x.values))]
                    ind_x = choice(list(ind_set_x["index"]))
                    # print("x", x, "case1", ind_x)
                elif len(ind_set_x) == 1:
                    ind_x = (df_short_new == closest_dist_x).idxmax(axis=1)[x]
                    # print("x", x, "case equal", ind_x)
                # Find closest open facility to x
                closest_dist_y = min(df_short_new.loc[y, :])
                # print(closest_dist_y)
                row_y = df_short_new.iloc[y]
                ind_set_y = row_y.reset_index().set_index(y).loc[closest_dist_y]
                if len(ind_set_y) > 1:
                    ind_set_y.index = [x for x in range(0, len(ind_set_y.values))]
                    ind_y = choice(list(ind_set_y["index"]))
                    # print("y", y, "case1", ind_y)
                elif len(ind_set_y) == 1:
                    ind_y = (df_short_new == closest_dist_y).idxmax(axis=1)[y]
                    # print("y", y, "case equal", ind_y)
                # Calculating the decomposing points
                if ind_x == ind_y:
                    bvu[i][0] = self.df_edge["Length"][i]
                    bvu[i][1] = 0
                else:
                    bvu[i][0] = (closest_dist_y + self.df_edge["Length"][i] - closest_dist_x) / 2
                    bvu[i][1] = (closest_dist_x + self.df_edge["Length"][i] - closest_dist_y) / 2
                # Share of edge(x,y) on producing gamma
                gamma_x = self.df_edge["Demand"][i] * bvu[i][0] / self.df_edge["Length"][i]
                gamma_y = self.df_edge["Demand"][i] * bvu[i][1] / self.df_edge["Length"][i]
                # Travel time of those located on edge(x,y)
                travel_x = gamma_x * (closest_dist_x + (bvu[i][0] / 2))
                travel_y = gamma_y * (closest_dist_y + (bvu[i][1] / 2))
                # Updating the traveling time objective function
            Travel = Travel + travel_x + travel_y
            # Updating the entrance rate of each facility after considering the effect of edge(x,y)
            gamma_j[ind_x] = gamma_j[ind_x] + gamma_x
            gamma_j[ind_y] = gamma_j[ind_y] + gamma_y



        a = Travel

        return a

#############################################################################################################
"""
Waiting time consideration according to M/M/1
"""
class Eval_wait():
    def __init__(self, Candidate_List, df_shortest, df_edge, opened_list, w_max: int, mu: int, p: int):
        self.p = p
        self.Candidate_List = Candidate_List
        self.df_shortest = df_shortest
        self.df_edge = df_edge
        self.opened_list = opened_list
        self.mu = mu
        self.w_max = w_max



    def eval(self):
        Travel = 0
        Waiting = 0

        
        df_short_new = self.df_shortest[self.opened_list]

        bvu = np.zeros((len(self.df_edge.values), 2))
        gamma_j = dict.fromkeys(self.opened_list, 0)
        gamma_bar_j = dict.fromkeys(self.opened_list, 0)
        ro_j = dict.fromkeys(self.opened_list, 0)
        L_bar = dict.fromkeys(self.opened_list, 0)
        w_j = dict.fromkeys(self.opened_list, 0)
        lost_j = dict.fromkeys(self.opened_list, 0)


        for i in range(0, len(self.df_edge.values)):
            x, y = eval(self.df_edge["Edges"][i])
            travel_x = 0
            travel_y = 0
            gamma_x = 0
            gamma_y = 0

            if list(df_short_new.loc[x, :]) and list(df_short_new.loc[y, :]):

                # Find closest open facility to x
                closest_dist_x = min(df_short_new.loc[x, :])
                # print(closest_dist_x)
                row_x = df_short_new.iloc[x]
                ind_set_x = row_x.reset_index().set_index(x).loc[closest_dist_x]
                if len(ind_set_x) > 1:
                    ind_set_x.index = [x for x in range(0, len(ind_set_x.values))]
                    ind_x = choice(list(ind_set_x["index"]))
                    # print("x", x, "case1", ind_x)
                elif len(ind_set_x) == 1:
                    ind_x = (df_short_new == closest_dist_x).idxmax(axis=1)[x]
                    # print("x", x, "case equal", ind_x)
                # Find closest open facility to x
                closest_dist_y = min(df_short_new.loc[y, :])
                # print(closest_dist_y)
                row_y = df_short_new.iloc[y]
                ind_set_y = row_y.reset_index().set_index(y).loc[closest_dist_y]
                if len(ind_set_y) > 1:
                    ind_set_y.index = [x for x in range(0, len(ind_set_y.values))]
                    ind_y = choice(list(ind_set_y["index"]))
                    # print("y", y, "case1", ind_y)
                elif len(ind_set_y) == 1:
                    ind_y = (df_short_new == closest_dist_y).idxmax(axis=1)[y]
                    # print("y", y, "case equal", ind_y)
                # Calculating the decomposing points
                if ind_x == ind_y:
                    bvu[i][0] = self.df_edge["Length"][i]
                    bvu[i][1] = 0
                else:
                    bvu[i][0] = (closest_dist_y + self.df_edge["Length"][i] - closest_dist_x) / 2
                    bvu[i][1] = (closest_dist_x + self.df_edge["Length"][i] - closest_dist_y) / 2
                # Share of edge(x,y) on producing gamma
                gamma_x = self.df_edge["Demand"][i] * bvu[i][0] / self.df_edge["Length"][i]
                gamma_y = self.df_edge["Demand"][i] * bvu[i][1] / self.df_edge["Length"][i]
                # Travel time of those located on edge(x,y)
                travel_x = gamma_x * (closest_dist_x + (bvu[i][0] / 2))
                travel_y = gamma_y * (closest_dist_y + (bvu[i][1] / 2))
                # Updating the traveling time objective function
            Travel = Travel + travel_x + travel_y
            # Updating the entrance rate of each facility after considering the effect of edge(x,y)
            gamma_j[ind_x] = gamma_j[ind_x] + gamma_x
            gamma_j[ind_y] = gamma_j[ind_y] + gamma_y

        for item in self.opened_list:
            if self.mu >= gamma_j[item] + 1/self.w_max:
                w_j[item] = 1/(self.mu - gamma_j[item])
            else:
                w_j[item] = 10000000
            Waiting = Waiting + (w_j[item] * gamma_j[item])

        a = (Travel + Waiting)



        return a
########################################################################################################################
class NODEE200():
    def __init__(self):
        """ :param number_of_variables: Number of decision variables of the problem.
        """
        super(NODEE200, self).__init__()
        self.Candidate_List = [35, 174, 57, 63, 185, 121, 160, 101, 2, 24, 180, 66, 22, 30, 69, 123, 172, 4, 189, 62,
                               161, 67, 134, 5, 93, 168, 130, 40, 33, 99, 29, 7, 198, 48, 91, 94, 41, 164, 31, 196]

        self.p = 10
        self.mu = 10
        self.w_max = 100

        self.df_shortest = pd.read_csv("shortest_path_200.csv", index_col=0)

        self.df_edge = pd.read_csv("edge_200.csv", index_col=0)
        #self.df_edge["Demand"] = [self.df_edge["Length"][i] / 10 for i in range(0, len(self.df_edge.values))]



    def evaluate(self, solution):

        solution1 = np.array(solution)

        indices = (-solution1).argsort()[:self.p]
        opened_list = [str(self.Candidate_List[i]) for i in indices]
        
        a = Eval(Candidate_List=self.Candidate_List,
                 df_shortest=self.df_shortest,
                 df_edge=self.df_edge,
                 opened_list=opened_list,
                 #w_max=self.w_max,
                 #mu=self.mu,
                 p=self.p).eval()

        #solution.objective = a

        return (a)

    def get_name(self):
        return 'NODEE200'
########################################################################################################################
class NODEE300():
    def __init__(self):
        """ :param number_of_variables: Number of decision variables of the problem.
        """
        super(NODEE300, self).__init__()
        self.Candidate_List = [136, 151, 241, 139, 137, 101, 175, 215, 99, 185, 166, 97, 238, 190, 19, 119, 43, 34, 211,
                               10, 207, 203, 252, 260, 204, 195, 57, 254, 100, 259, 134, 70, 231, 12, 206, 214, 279, 113,
                               74, 230, 143, 41, 177, 51, 150, 81, 77, 50, 208, 182]

        self.p = 20
        self.mu = 10
        self.w_max = 100

        self.df_shortest = pd.read_csv("shortest_path_300.csv")

        self.df_edge = pd.read_csv("edge_300.csv")
        #self.df_edge["Demand"] = [self.df_edge["Length"][i] / 10 for i in range(0, len(self.df_edge.values))]



    def evaluate(self, solution):

        solution1 = np.array(solution)
        indices = (-solution1).argsort()[:self.p]
        opened_list = [str(self.Candidate_List[i]) for i in indices]

        a = Eval(Candidate_List=self.Candidate_List,
                 df_shortest=self.df_shortest,
                 df_edge=self.df_edge,
                 opened_list=opened_list,
                 #w_max=self.w_max,
                 #mu=self.mu,
                 p=self.p).eval()

        #solution.objective = a

        return (a)

    def get_name(self):
        return 'NODEE300'
########################################################################################################################
class NODEE400():
    def __init__(self):
        """ :param number_of_variables: Number of decision variables of the problem.
        """
        super(NODEE400, self).__init__()
        self.Candidate_List = [98, 219, 388, 258, 23, 247, 166, 366, 105, 162, 145, 16, 86, 386, 228, 1, 272, 81, 39,
                               348, 93, 243, 148, 54, 204, 379, 49, 123, 160, 83, 223, 375, 267, 159, 182, 119, 131, 270,
                               17, 110, 135, 269, 15, 334, 255, 13, 212, 121, 35, 279, 100, 289, 237, 239, 196, 101, 194,
                               256, 210, 352]

        self.p = 30
        self.mu = 10
        self.w_max = 100

        self.df_shortest = pd.read_csv("shortest_path_400.csv")

        self.df_edge = pd.read_csv("edge_400.csv")
        #self.df_edge["Demand"] = [self.df_edge["Length"][i] / 10 for i in range(0, len(self.df_edge.values))]



    def evaluate(self, solution):

        solution1 = np.array(solution)
        indices = (-solution1).argsort()[:self.p]
        opened_list = [str(self.Candidate_List[i]) for i in indices]

        a = Eval(Candidate_List=self.Candidate_List,
                 df_shortest=self.df_shortest,
                 df_edge=self.df_edge,
                 opened_list=opened_list,
                 #w_max=self.w_max,
                 #mu=self.mu,
                 p=self.p).eval()

        #solution.objective = a

        return (a)

    def get_name(self):
        return 'NODEE400'
########################################################################################################################
class NODEE500():
    def __init__(self):
        """ :param number_of_variables: Number of decision variables of the problem.
        """
        super(NODEE500, self).__init__()
        self.Candidate_List = [357, 385, 247, 412, 349, 138, 95, 147, 87, 185, 94, 244, 178, 479, 263, 264, 154, 216,
                               481, 291, 213, 493, 301, 243, 487, 372, 420, 383, 421, 197, 156, 298, 310, 459, 49, 374,
                               322, 367, 237, 139, 382, 270, 137, 384, 7, 188, 299, 290, 428, 25, 93, 116, 358, 336, 214,
                               380, 470, 199, 14, 297, 446, 486, 369, 443, 232, 462, 253, 55, 212, 491]

        self.p = 40
        self.mu = 10
        self.w_max = 100

        self.df_shortest = pd.read_csv("shortest_path_500.csv")

        self.df_edge = pd.read_csv("edge_500.csv")
        #self.df_edge["Demand"] = [self.df_edge["Length"][i] / 10 for i in range(0, len(self.df_edge.values))]



    def evaluate(self, solution):

        solution1 = np.array(solution)
        indices = (-solution1).argsort()[:self.p]
        opened_list = [str(self.Candidate_List[i]) for i in indices]

        a = Eval(Candidate_List=self.Candidate_List,
                 df_shortest=self.df_shortest,
                 df_edge=self.df_edge,
                 opened_list=opened_list,
                 #w_max=self.w_max,
                 #mu=self.mu,
                 p=self.p).eval()

        #solution.objective = a

        return (a)

    def get_name(self):
        return 'NODEE500'
########################################################################################################################
class NODEE600():
    def __init__(self):
        """ :param number_of_variables: Number of decision variables of the problem.
        """
        super(NODEE600, self).__init__()
        self.Candidate_List = [226, 311, 378, 499, 109, 539, 535, 381, 465, 414, 396, 353, 99, 2, 374, 90, 38, 82, 395,
                               137, 9, 546, 402, 344, 387, 599, 506, 97, 330, 245, 255, 449, 534, 154, 272, 282, 566,
                               202, 446, 518, 373, 555, 293, 19, 73, 81, 150, 62, 48, 304, 466, 39, 75, 28, 67, 476, 153,
                               463, 452, 342, 254, 592, 71, 405, 497, 388, 359, 410, 53, 182, 474, 350, 567, 225, 280,
                               57, 558, 126, 36, 170]

        self.p = 50
        self.mu = 10
        self.w_max = 100

        self.df_shortest = pd.read_csv("shortest_path_600.csv")

        self.df_edge = pd.read_csv("edge_600.csv")
        #self.df_edge["Demand"] = [self.df_edge["Length"][i] / 10 for i in range(0, len(self.df_edge.values))]



    def evaluate(self, solution):

        solution1 = np.array(solution)
        indices = (-solution1).argsort()[:self.p]
        opened_list = [str(self.Candidate_List[i]) for i in indices]

        a = Eval(Candidate_List=self.Candidate_List,
                 df_shortest=self.df_shortest,
                 df_edge=self.df_edge,
                 opened_list=opened_list,
                 #w_max=self.w_max,
                 #mu=self.mu,
                 p=self.p).eval()

        #solution.objective = a

        return (a)

    def get_name(self):
        return 'NODEE600'
########################################################################################################################
class NODEE700():
    def __init__(self):
        """ :param number_of_variables: Number of decision variables of the problem.
        """
        super(NODEE700, self).__init__()
        self.Candidate_List = [133, 633, 544, 222, 453, 11, 682, 680, 566, 669, 578, 687, 645, 576, 154, 190, 231, 379,
                               655, 340, 58, 75, 138, 398, 574, 525, 688, 269, 623, 613, 281, 26, 535, 130, 329, 662,
                               546, 584, 545, 444, 313, 497, 501, 283, 436, 307, 604, 162, 411, 450, 579, 552, 336, 558,
                               509, 694, 458, 7, 17, 401, 335, 62, 256, 681, 600, 582, 266, 620, 299, 2, 692, 577, 144,
                               586, 195, 103, 435, 12, 524, 106, 73, 13, 656, 671, 151, 416, 249, 410, 115, 366]

        self.p = 60
        self.mu = 10
        self.w_max = 100

        self.df_shortest = pd.read_csv("shortest_path_700.csv")

        self.df_edge = pd.read_csv("edge_700.csv")
        #self.df_edge["Demand"] = [self.df_edge["Length"][i] / 10 for i in range(0, len(self.df_edge.values))]



    def evaluate(self, solution):

        solution1 = np.array(solution)
        indices = (-solution1).argsort()[:self.p]
        opened_list = [str(self.Candidate_List[i]) for i in indices]

        a = Eval(Candidate_List=self.Candidate_List,
                 df_shortest=self.df_shortest,
                 df_edge=self.df_edge,
                 opened_list=opened_list,
                 #w_max=self.w_max,
                 #mu=self.mu,
                 p=self.p).eval()

        #solution.objective = a

        return (a)

    def get_name(self):
        return 'NODEE700'
