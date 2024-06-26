data_file_name = "browsing-data.txt"
output_file_name = "./output.txt"
given_threshold = 100

class top_five:

    def __init__(self) -> None:
        self.top_five_arr = []

    def insert_item(self, new_item) -> None:
        if len(self.top_five_arr) < 5:
            self.top_five_arr.append(new_item)
            self.top_five_arr.sort()
        elif self.top_five_arr[0] < new_item:
            self.top_five_arr[0] = new_item
            self.top_five_arr.sort()

    def get_top_five_array(self) -> list:
        return self.top_five_arr[::-1]
    
class rule_one:

    def __init__(self, left : str, right : str, con : float) -> None:
        self.left_value = left
        self.right_value = right
        self.confidence = con

    def __lt__(self, other_item) -> bool:
        if not isinstance(other_item, rule_one):
            return None
        elif self.confidence != other_item.confidence:
            return self.confidence < other_item.confidence
        else:
            return self.left_value > self.right_value
        
    def __gt__(self, other_item) -> bool:
        if not isinstance(other_item, rule_one):
            return None
        elif self.confidence != other_item.confidence:
            return self.confidence > other_item.confidence
        else:
            return self.left_value < other_item.left_value
        
    def __eq__(self, other_item) -> bool:
        if not isinstance(other_item, rule_one):
            return None
        return (self.confidence == other_item.confidence) and (self.left_value ==  other_item.left_value)
        
    def __str__(self) -> str:
        return "{} {} {:.4f}".format(self.left_value, self.right_value, self.confidence)

class rule_two:

    def __init__(self, left_one : str, left_two : str, right : str, con : float) -> None:
        # if (left_two > left_one):
        #     left_one, left_two = left_two, left_one
        # self.left_item_one = left_one
        # self.left_item_two = left_two
        pair = sorted([left_one, left_two])
        self.left_item_one = pair[0]
        self.left_item_two = pair[1]
        self.right_item = right
        self.confidence = con
    
    def __lt__(self, other_item) -> bool:
        if not isinstance(other_item, rule_two):
            return None
        if self.confidence != other_item.confidence:
            return self.confidence < other_item.confidence
        elif self.left_item_one != other_item.left_item_two:
            return self.left_item_one > other_item.left_item_one
        else:
            return self.left_item_two > other_item.left_item_two
    
    def __gt__(self, other_item) -> bool:
        if not isinstance(other_item, rule_two):
            return None
        elif self.confidence != other_item.confidence:
            return self.confidence > other_item.confidence
        elif self.left_item_one != other_item.left_item_one:
            return self.left_item_one < other_item.left_item_one
        else:
            return self.left_item_two < other_item.left_item_two
    
    def __eq__(self, other_item) -> bool:
        if not isinstance(other_item, rule_two):
            return None
        return (self.confidence == other_item.confidence) and (self.left_item_one == other_item.left_item_one) and (self.left_item_two == other_item.left_item_two)
    
    def __str__(self) -> str:
        return "{} {} {} {:.4f}".format(self.left_item_one, self.left_item_two, self.right_item, self.confidence)

def get_frequent_item_set() -> dict:
    frequency_dict = {}
    input_stream = open(data_file_name, "r")
    for line in input_stream:
        basket = line.replace('\n', '').split()
        for item in basket:
            frequency_dict[item] = frequency_dict.get(item, 0) + 1
    input_stream.close()
    keys_to_delete = []
    for item in frequency_dict:
        if frequency_dict[item] < given_threshold:
            keys_to_delete.append(item)
    for item in keys_to_delete:
        del frequency_dict[item]
    return frequency_dict

def get_pair_candidates(frequent_items : dict) -> set:
    return set(frequent_items)

def get_frequent_item_pair_set(pair_candidates : set) -> dict:
    frequency_dict = {}
    input_stream = open(data_file_name, "r")
    for line in input_stream:
        basket = line.replace('\n', '').split()
        for i in range(len(basket)):
            if basket[i] in pair_candidates:
                for j in range(i + 1, len(basket)):
                    if basket[j] in pair_candidates:
                        key = frozenset([basket[i], basket[j]])
                        frequency_dict[key] = frequency_dict.get(key, 0) + 1
    input_stream.close()
    keys_to_delete = []
    for pair in frequency_dict:
        if frequency_dict[pair] < given_threshold:
            keys_to_delete.append(pair)
    for pair in keys_to_delete:
        del frequency_dict[pair]
    return frequency_dict

def get_triple_candidates(frequent_pairs : dict) -> set:
    candidate_set = set()
    for pair in frequent_pairs:
        for item in pair:
            candidate_set.add(item)
    return candidate_set

def get_frequent_item_triple_set(triple_candidates : set) -> dict:
    frequency_dict = {}
    input_stream = open(data_file_name, "r")
    for line in input_stream:
        basket = line.replace('\n', '').split()
        for i in range(0, len(basket), 1):
            if basket[i] in triple_candidates:
                for j in range(i + 1, len(basket), 1):
                    if basket[j] in triple_candidates:
                        for k in range(j + 1, len(basket), 1):
                            if basket[k] in triple_candidates:
                                key = frozenset([basket[i], basket[j], basket[k]])
                                frequency_dict[key] = frequency_dict.get(key, 0) + 1
    input_stream.close()
    keys_to_delete = []
    for triple in frequency_dict:
        if frequency_dict[triple] < given_threshold:
            keys_to_delete.append(triple)
    for triple in keys_to_delete:
        del frequency_dict[triple]
    return frequency_dict

def get_top_five_rule_one(frequent_items : dict, frequent_pairs : dict) -> list:
    rule_one_top_five = top_five()
    for key in frequent_pairs:
        pair = list(key)
        rule_one_top_five.insert_item(rule_one(pair[0], pair[1], frequent_pairs[key] / frequent_items[pair[0]]))
        rule_one_top_five.insert_item(rule_one(pair[1], pair[0], frequent_pairs[key] / frequent_items[pair[1]]))
    return rule_one_top_five.get_top_five_array()

def get_top_five_rule_two(frequent_pairs : dict, frequent_triples : dict) -> list:
    rule_two_top_five = top_five()
    for key in frequent_triples:
        triple = list(key)
        rule_two_top_five.insert_item(rule_two(triple[0], triple[1], triple[2], (frequent_triples[key] / frequent_pairs[frozenset([triple[0], triple[1]])])))
        rule_two_top_five.insert_item(rule_two(triple[2], triple[0], triple[1], (frequent_triples[key] / frequent_pairs[frozenset([triple[2], triple[0]])])))
        rule_two_top_five.insert_item(rule_two(triple[1], triple[2], triple[0], (frequent_triples[key] / frequent_pairs[frozenset([triple[1], triple[2]])])))
    return rule_two_top_five.get_top_five_array()

def print_rules_to_output_file(rule_one_top_five : list, rule_two_top_five : list) -> None:
    output_stream = open(output_file_name, "w")
    output_stream.write("OUTPUT A\n")
    for item in rule_one_top_five:
        output_stream.write(str(item) + "\n")
    output_stream.write("OUTPUT B\n")
    for item in rule_two_top_five:
        output_stream.write(str(item) + "\n")
    output_stream.close()

def run_analysis() -> None:
    frequent_items = get_frequent_item_set()
    pair_candidates = get_pair_candidates(frequent_items)
    frequent_pairs = get_frequent_item_pair_set(pair_candidates)
    triple_candidates = get_triple_candidates(frequent_pairs)
    frequent_triples = get_frequent_item_triple_set(triple_candidates)
    rule_one_top_five = get_top_five_rule_one(frequent_items, frequent_pairs)
    rule_two_top_five = get_top_five_rule_two(frequent_pairs, frequent_triples)
    print_rules_to_output_file(rule_one_top_five, rule_two_top_five)

run_analysis()