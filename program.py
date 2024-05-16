#!/usr/bin/python3

def get_triangle_matrix(num_elements : int) -> list[int]:
    return [0] * int((((num_elements - 1) * num_elements) / 2))

def get_num_freq_items(threashold : int, item_freq_table : dict) -> int:
    num_freq_items = 0
    for item in item_freq_table:
        if item_freq_table[item] > threashold:
            num_freq_items += 1
    return num_freq_items

def get_freq_item_list(threashold : int, item_freq_table : dict) -> list[str]:
    freq_items = []
    for item in item_freq_table:
        if item_freq_table[item] > threashold:
            freq_items.append(item)
    return freq_items

def print_freq_items(threashold : int, item_freq_table : dict) -> None:
    i = 0
    j = 0
    for item in item_freq_table:
        if item_freq_table[item] > threashold:
            print("ITEM[" + str(item) + "] : FREQ[" + str(item_freq_table[item]) + "]")

def get_item_dict() -> dict:
    input_file = open("browsing-data.txt", "r")
    item_table = {}
    for line in input_file:
        codes = line.replace('\n', '').split()
        for code in codes:
            if code not in item_table:
                item_table[code] = 1
            else:
                item_table[code] += 1
    return item_table

get_triangle_matrix(642)