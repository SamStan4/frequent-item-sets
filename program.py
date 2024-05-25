#!/usr/bin/python3

import bisect

data_file_name = "browsing-data.txt"
output_file_name = "./output.txt"
given_threshold = 100

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
#     method name     --> 
#     method purpose  --> 
#     member of       -->
#     preconditions   --> 
#     postconditions  --> 
#     date created    --> 
#     last modified   --> 
#     programmer      --> 
#     sources         --> 

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#################################################################################################################################################################################################################
#
#          /$$$$$$  /$$        /$$$$$$   /$$$$$$   /$$$$$$  /$$$$$$$$  /$$$$$$ 
#         /$$__  $$| $$       /$$__  $$ /$$__  $$ /$$__  $$| $$_____/ /$$__  $$
#        | $$  \__/| $$      | $$  \ $$| $$  \__/| $$  \__/| $$      | $$  \__/
#        | $$      | $$      | $$$$$$$$|  $$$$$$ |  $$$$$$ | $$$$$   |  $$$$$$ 
#        | $$      | $$      | $$__  $$ \____  $$ \____  $$| $$__/    \____  $$
#        | $$    $$| $$      | $$  | $$ /$$  \ $$ /$$  \ $$| $$       /$$  \ $$
#        |  $$$$$$/| $$$$$$$$| $$  | $$|  $$$$$$/|  $$$$$$/| $$$$$$$$|  $$$$$$/
#         \______/ |________/|__/  |__/ \______/  \______/ |________/ \______/ 
#
#################################################################################################################################################################################################################

class rule_one:

    def __init__(self, left : str, right : str, con : float) -> None:
        # note: { i } => j with confidence c
        self.i = left
        self.j = right
        self.c = con

    def __lt__(self, item) -> bool:
        if not isinstance(item, rule_one):
            return None
        elif (self.c != item.c):
            return self.c < item.c
        elif (self.i != item.i):
            return self.i < item.i
        else:
            return False

    def __gt__(self, item) -> bool:
        if not isinstance(item, rule_one):
            return None
        elif (self.c != item.c):
            return self.c > item.c
        elif (self.i != item.i):
            return self.i > item.i
        else:
            return False
        
    def __str__(self) -> str:
        string = "{} {} {:.4f}".format(self.i, self.j, self.c)
        return string
    
#################################################################################################################################################################################################################
    
class rule_two:

    def __init__(self, left1 : str, left2 : str, right : str, con : float) -> None:
        # note: { i1, i2 } => j with confidence c
        lhs = sorted([left1, left2])
        self.i1 = lhs[0]
        self.i2 = lhs[1]
        # if left2 < left1:
        #     left1, left2 = left2, left1
        # self.i1 = left1
        # self.i2 = left2
        self.j = right
        self.c = con

    def __lt__(self, item) -> bool:
        if not isinstance(item, rule_two):
            return None
        if (self.c != item.c):
            return self.c < item.c
        elif (self.i1 != item.i1):
            return self.i1 > item.i1
        elif (self.i2 != item.i2):
            return self.i2 > item.i2
        else:
            return False
    
    def __gt__(self, item) -> bool:
        if not isinstance(item, rule_two):
            return None
        if (self.c != item.c):
            return self.c > item.c
        elif (self.i1 != item.i1):
            return self.i1 < item.i1
        elif (self.i2 != item.i2):
            return self.i2 < item.i2
        else:
            return False
    
    def __str__(self) -> str:
        string = "{} {} {} {:.4f}".format(self.i1, self.i2, self.j, self.c)
        return string


#################################################################################################################################################################################################################
    
class rule_top_five:

    def __init__(self) -> None:
        self.top_list = []
    
    def insert_value(self, item : rule_one) -> None:
        if len(self.top_list) < 5:
            bisect.insort(self.top_list, item)
        else:
            if (item > self.top_list[0]):
                del self.top_list[0]
                bisect.insort(self.top_list, item)

    def get_top_five(self) -> list:
        return self.top_list[::-1]
     
#################################################################################################################################################################################################################
    
class pair_matrix:

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #     method name     --> __init__()
    #     method purpose  --> constructor
    #     member of       --> pair_matrix
    #     preconditions   --> none
    #     postconditions  --> none
    #     date created    --> 5/15/2024
    #     last modified   --> 5/15/2024
    #     programmer      --> sam stanley
    #     sources         --> none

    def __init__(self, item_list : list) -> None:
        self.pair_grid = []
        self.num_items = len(item_list)
        self.code_to_num = {}
        self.num_to_code = {}
        size = len(item_list)
        self.pair_grid = [0] * (size * (size + 1) // 2)
        for i in range (0, len(item_list), 1):
            self.code_to_num[item_list[i]] = i
            self.num_to_code[i] = item_list[i]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #     method name     --> get_internal_index()
    #     method purpose  --> returns the actual index of an element in the array, 2d -> 1d
    #     member of       --> pair_matrix
    #     preconditions   --> none
    #     postconditions  --> none
    #     date created    --> 5/15/2024
    #     last modified   --> 5/15/2024
    #     programmer      --> sam stanley
    #     sources         --> none

    def get_internal_index(self, i : str, j : str) -> int:
        i = self.code_to_num[i]
        j = self.code_to_num[j]
        if (i == j):
            return -1
        if (i > j):
            i, j = j, i
        return i * (2 * self.num_items - i + 1) // 2 + j - i

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #     method name     --> __getitem__()
    #     method purpose  --> returns item at given 2d index
    #     member of       --> pair_matrix
    #     preconditions   --> none
    #     postconditions  --> none
    #     date created    --> 5/15/2024
    #     last modified   --> 5/16/2024
    #     programmer      --> sam stanley
    #     sources         --> none

    def __getitem__(self, index : list) -> int:
        i, j = index
        real_index = self.get_internal_index(i, j)
        if real_index == -1:
            return -1
        elif real_index >= len(self.pair_grid):
            return -1
        else:
            return self.pair_grid[real_index]
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #     method name     --> __setitem__()
    #     method purpose  --> sets item at given 2d index
    #     member of       --> pair_matrix
    #     preconditions   --> none
    #     postconditions  --> none
    #     date created    --> 5/15/2024
    #     last modified   --> 5/16/2024
    #     programmer      --> sam stanley
    #     sources         --> none
    
    def __setitem__(self, index : list, val : int) -> None:
        i, j = index
        real_index = self.get_internal_index(i, j)
        if real_index == -1:
            return
        elif real_index >= len(self.pair_grid):
            return
        else:
            self.pair_grid[real_index] = val

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #     method name     --> get_num_items()
    #     method purpose  --> returns the total number of items with value >= min
    #     member of       --> pair_matrix
    #     preconditions   --> none
    #     postconditions  --> none
    #     date created    --> 5/15/2024
    #     last modified   --> 5/16/2024
    #     programmer      --> sam stanley
    #     sources         --> none

    def get_num_items(self, min = 0) -> None:
        total = 0
        for i in range(len(self.pair_grid)):
            if self.pair_grid[i] >= min:
                total += 1
        return total

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#################################################################################################################################################################################################################

class triple_matrix:

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #     method name     --> __init__()
    #     method purpose  --> constructor
    #     member of       --> triple_matrix
    #     preconditions   --> none
    #     postconditions  --> none
    #     date created    --> 5/16/2024
    #     last modified   --> 5/16/2024
    #     programmer      --> sam stanley
    #     sources         --> none

    def __init__(self) -> None:
        self.tripple_table = {}

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #     method name     --> increment()
    #     method purpose  --> increments an index based off of a given key
    #     member of       --> triple_matrix
    #     preconditions   --> none
    #     postconditions  --> none
    #     date created    --> 5/16/2024
    #     last modified   --> 5/16/2024
    #     programmer      --> sam stanley
    #     sources         --> none

    def increment(self, key : set, add = 1) -> None:
        frozen_key = frozenset(key)
        if len(key) != 3:
            return
        if frozen_key not in self.tripple_table:
            self.tripple_table[frozen_key] = 0
        self.tripple_table[frozen_key] += add
        
        
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #     method name     --> get_frequent_elements()
    #     method purpose  --> gets items in the tripple table that are above a certian amount
    #     member of       --> triple_matrix
    #     preconditions   --> none
    #     postconditions  --> none
    #     date created    --> 5/16/2024
    #     last modified   --> 5/16/2024
    #     programmer      --> sam stanley
    #     sources         --> none

    def get_frequent_elements(self, min : int) -> list:
        freq_tripple_list = []
        for key in self.tripple_table:
            if self.tripple_table[key] >= min:
                freq_tripple_list.append(set(key))
        return freq_tripple_list
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #     method name     --> get_frequent_elements_table()
    #     method purpose  --> gets items in the tripple table that are above a certian amount and returns a dict that contains the item + its support
    #     member of       --> triple_matrix
    #     preconditions   --> none
    #     postconditions  --> none
    #     date created    --> 5/16/2024
    #     last modified   --> 5/16/2024
    #     programmer      --> sam stanley
    #     sources         --> none
    
    def get_frequent_elements_table(self, min : int) -> dict:
        freq_table_dict = {}
        for key in self.tripple_table:
            if self.tripple_table[key] >= min:
                freq_table_dict[key] = self.tripple_table[key]
        return freq_table_dict

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#################################################################################################################################################################################################################

class analysis_wrapper:

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #     method name     --> __init__()
    #     method purpose  --> constructor
    #     member of       --> analysis_wrapper
    #     preconditions   --> none
    #     postconditions  --> none
    #     date created    --> 5/15/2024
    #     last modified   --> 5/15/2024
    #     programmer      --> sam stanley
    #     sources         --> none

    def __init__(self, min : int) -> None:
        self.threshold = min
        self.frequent_items = []
        self.frequent_pairs = []
        self.frequent_triples = []
        self.frequent_items_dict = {}
        self.frequent_pairs_dict = {}
        self.frequent_triples_dict = {}
        self.populate_frequent_items()
        self.populate_frequent_pairs()
        self.populate_frequent_triples()


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #     method name     --> run_analysis()
    #     method purpose  --> runs the entire program
    #     member of       --> analysis_wrapper
    #     preconditions   --> constructor executed
    #     postconditions  --> none
    #     date created    --> 5/15/2024
    #     last modified   --> 5/15/2024
    #     programmer      --> sam stanley
    #     sources         --> none

    def run_analysis(self) -> None:
        top_five_rule_one = self.get_top_five_conf_pairs()
        top_five_rule_two = self.get_top_five_conf_tripples()
        self.print_output(top_five_rule_one, top_five_rule_two)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #     method name     --> get_items_in_freq_pairs()
    #     method purpose  --> this function will return a list of items that appear in a frequent pair
    #     member of       --> analysis_wrapper
    #     preconditions   --> none
    #     postconditions  --> none
    #     date created    --> 5/16/2024
    #     last modified   --> 5/16/2024
    #     programmer      --> sam stanley
    #     sources         --> none

    def get_items_in_freq_pairs(self) -> list:
        pair_item_set = set()
        for pair in self.frequent_pairs:
            pair_list = list(pair)
            for item in pair_list:
                pair_item_set.add(item)
        return list(pair_item_set)


    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #     method name     --> populate_frequent_items()
    #     method purpose  --> populates a list of items that appear a minimum number of times
    #     member of       --> analysis_wrapper
    #     preconditions   --> program constructor was called, file exists
    #     postconditions  --> none
    #     date created    --> 5/15/2024
    #     last modified   --> 5/15/2024
    #     programmer      --> sam stanley
    #     sources         --> none

    def populate_frequent_items(self) -> None:
        item_freq = {}
        input_stream = open(data_file_name, "r")
        for line in input_stream:
            basket = line.replace('\n', '').split()
            for item in basket:
                if item in item_freq:
                    item_freq[item] += 1
                else:
                    item_freq[item] = 1
        input_stream.close()
        for key in item_freq:
            if item_freq[key] >= self.threshold:
                self.frequent_items.append(key)
                self.frequent_items_dict[key] = item_freq[key]
    
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #     method name     --> populate_frequent_pairs()           this function is slow AF
    #     method purpose  --> populates a list of pairs that appear a minimum number of times using the A-priori algorithim
    #     member of       --> analysis_wrapper
    #     preconditions   --> program constructor was called, file exists
    #     postconditions  --> none
    #     date created    --> 5/15/2024
    #     last modified   --> 5/16/2024
    #     programmer      --> sam stanley
    #     sources         --> none

    def populate_frequent_pairs(self) -> None:
        pair_grid = pair_matrix(self.frequent_items)
        frequent_item_set = set(self.frequent_items)
        input_stream = open(data_file_name, "r")
        for line in input_stream:
            basket = line.replace('\n', '').split()
            for i in range(len(basket)):
                if basket[i] in frequent_item_set:
                    for j in range(i + 1, len(basket)):
                        if basket[j] in frequent_item_set:
                            pair_grid[basket[i], basket[j]] += 1
        input_stream.close()
        for i in range(len(self.frequent_items)):
            for j in range(i + 1, len(self.frequent_items)):
                if (pair_grid[self.frequent_items[i], self.frequent_items[j]] > self.threshold):
                    self.frequent_pairs.append(set([self.frequent_items[i], self.frequent_items[j]]))
                    self.frequent_pairs_dict[frozenset(set([self.frequent_items[i], self.frequent_items[j]]))] = pair_grid[self.frequent_items[i], self.frequent_items[j]]

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #     method name     --> populate_frequent_triples()           this function is also SLOW AF
    #     method purpose  --> populates a list of triples that appear a minimum number of times using the A-priori algorithim
    #     member of       --> analysis_wrapper
    #     preconditions   --> program constructor was called, file exists
    #     postconditions  --> none
    #     date created    --> 5/16/2024
    #     last modified   --> 5/16/2024
    #     programmer      --> sam stanley
    #     sources         --> none

    def populate_frequent_triples(self) -> None:
        triple_grid = triple_matrix()
        frequent_pair_items = set(self.get_items_in_freq_pairs())
        input_stream = open(data_file_name, "r")
        for line in input_stream:
            basket = line.replace('\n', '').split()
            for i in range(len(basket)):
                if basket[i] in frequent_pair_items:
                    for j in range(i + 1, len(basket)):
                        if basket[j] in frequent_pair_items:
                            for k in range(j + 1, len(basket)):
                                if basket[k] in frequent_pair_items:
                                    triple_grid.increment(set([basket[i], basket[j], basket[k]]))
        input_stream.close()
        self.frequent_triples = triple_grid.get_frequent_elements(given_threshold)
        self.frequent_triples_dict = triple_grid.get_frequent_elements_table(given_threshold)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #     method name     --> get_top_five_conf_pairs()
    #     method purpose  --> this function returns the top 5 confident { i } => j
    #     member of       --> analysis_wrapper
    #     preconditions   --> frequent_pairs is populated
    #     postconditions  --> none
    #     date created    --> 5/16/2024
    #     last modified   --> 5/16/2024
    #     programmer      --> sam stanley
    #     sources         --> none

    def get_top_five_conf_pairs(self) -> list:
        top_five_list = rule_top_five()
        for key in self.frequent_pairs_dict:
            pair = list(key)
            top_five_list.insert_value(rule_one(pair[0], pair[1], self.frequent_pairs_dict[key] / self.frequent_items_dict[pair[0]]))
            top_five_list.insert_value(rule_one(pair[1], pair[0], self.frequent_pairs_dict[key] / self.frequent_items_dict[pair[1]]))
        return top_five_list.get_top_five()
            

    def get_top_five_conf_tripples(self) -> list:
        top_five_list = rule_top_five()
        for key in self.frequent_triples_dict:
            triple = list(key)
            top_five_list.insert_value(rule_two(triple[0], triple[1], triple[2], self.frequent_triples_dict[key] / self.frequent_pairs_dict[frozenset(set([triple[0], triple[1]]))]))        
            top_five_list.insert_value(rule_two(triple[1], triple[2], triple[0], self.frequent_triples_dict[key] / self.frequent_pairs_dict[frozenset(set([triple[1], triple[2]]))]))        
            top_five_list.insert_value(rule_two(triple[0], triple[2], triple[1], self.frequent_triples_dict[key] / self.frequent_pairs_dict[frozenset(set([triple[0], triple[2]]))]))
        return top_five_list.get_top_five()
            

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #     method name     --> print_frequent_items()
    #     method purpose  --> displays to the terminal, the list of frequent items
    #     member of       --> analysis_wrapper
    #     preconditions   --> frequent_items is populated
    #     postconditions  --> none
    #     date created    --> 5/15/2024
    #     last modified   --> 5/15/2024
    #     programmer      --> sam stanley
    #     sources         --> none

    def print_frequent_items(self) -> None:
        for item in self.frequent_items:
            print("ITEM[" + str(item) + "] --> FREQ[" + str(self.frequent_items_dict[item]) + "]")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #     method name     --> print_frequent_pairs()
    #     method purpose  --> displays to the terminal, the list of frequent pairs
    #     member of       --> analysis_wrapper
    #     preconditions   --> frequent_pairs is populated
    #     postconditions  --> none
    #     date created    --> 5/15/2024
    #     last modified   --> 5/16/2024
    #     programmer      --> sam stanley
    #     sources         --> none

    def print_frequent_pairs(self) -> None:
        for pair in self.frequent_pairs:
            print("PAIR[" + str(pair) + "] --> FREQ[" + str(self.frequent_pairs_dict[frozenset(pair)]) + "]")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
    #     method name     --> print_frequent_triples()
    #     method purpose  --> displays to the terminal, the list of frequent triples
    #     member of       --> analysis_wrapper
    #     preconditions   --> frequent_triples is populated
    #     postconditions  --> none
    #     date created    --> 5/16/2024
    #     last modified   --> 5/16/2024
    #     programmer      --> sam stanley
    #     sources         --> none

    def print_frequent_triples(self) -> None:
        for triple in self.frequent_triples:
            print("TRIPLE[" + str(triple) + "] --> FREQ[" + str(self.frequent_triples_dict[frozenset(triple)]) + "]")

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    def print_output(self, rule_one_top : list, rule_two_top : list) -> None:
        output_stream = open(output_file_name, "w")
        output_stream.write("OUTPUT A\n")
        for rule in rule_one_top:
            output_stream.write(str(rule) + "\n")
        output_stream.write("OUTPUT B\n")
        for rule in rule_two_top:
            output_stream.write(str(rule) + "\n")
        output_stream.close()


#################################################################################################################################################################################################################
#
#                                 /$$             /$$$ /$$$          /$$$$$$                                 /$$     /$$                    
#                                |__/            /$$_/|_  $$        /$$__  $$                               | $$    |__/                    
#         /$$$$$$/$$$$   /$$$$$$  /$$ /$$$$$$$  /$$/    \  $$      | $$  \__//$$   /$$ /$$$$$$$   /$$$$$$$ /$$$$$$   /$$  /$$$$$$  /$$$$$$$ 
#        | $$_  $$_  $$ |____  $$| $$| $$__  $$| $$      | $$      | $$$$   | $$  | $$| $$__  $$ /$$_____/|_  $$_/  | $$ /$$__  $$| $$__  $$
#        | $$ \ $$ \ $$  /$$$$$$$| $$| $$  \ $$| $$      | $$      | $$_/   | $$  | $$| $$  \ $$| $$        | $$    | $$| $$  \ $$| $$  \ $$
#        | $$ | $$ | $$ /$$__  $$| $$| $$  | $$|  $$     /$$/      | $$     | $$  | $$| $$  | $$| $$        | $$ /$$| $$| $$  | $$| $$  | $$
#        | $$ | $$ | $$|  $$$$$$$| $$| $$  | $$ \  $$$ /$$$/       | $$     |  $$$$$$/| $$  | $$|  $$$$$$$  |  $$$$/| $$|  $$$$$$/| $$  | $$
#        |__/ |__/ |__/ \_______/|__/|__/  |__/  \___/|___/        |__/      \______/ |__/  |__/ \_______/   \___/  |__/ \______/ |__/  |__/
#
#################################################################################################################################################################################################################

def main() -> None:
    
    program = analysis_wrapper(given_threshold)
    program.run_analysis()

#################################################################################################################################################################################################################

main()