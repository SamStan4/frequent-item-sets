data_file_name = "browsing-data.txt"
output_file_name = "./output.txt"
given_threshold = 100

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

frequent_items = get_frequent_item_set()

pair_candidates = get_pair_candidates(frequent_items)

frequent_pairs = get_frequent_item_pair_set(pair_candidates)

triple_candidates = get_triple_candidates(frequent_pairs)

frequent_triples = get_frequent_item_triple_set(triple_candidates)

print(len(frequent_items))
print(len(frequent_pairs))
print(len(frequent_triples))