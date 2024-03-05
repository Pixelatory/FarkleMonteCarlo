import itertools
from typing import List, Tuple
from collections import Counter

# Define the possible outcomes of a single dice roll
dice_outcomes = [1, 2, 3, 4, 5, 6]

# Generate all possible combinations of 6 dice rolls
all_6_combos = list(itertools.product(dice_outcomes, repeat=6))
all_5_combos = list(itertools.product(dice_outcomes, repeat=5))
all_4_combos = list(itertools.product(dice_outcomes, repeat=4))
all_3_combos = list(itertools.product(dice_outcomes, repeat=3))
all_2_combos = list(itertools.product(dice_outcomes, repeat=2))
all_1_combos = list(itertools.product(dice_outcomes, repeat=1))


def ratio_to_percent_str(ratio):
    return f"{ratio * 100:.3f}%"

def is_straight(combo: Tuple[int]):
    tmp_combo = list(combo)
    tmp_combo = tmp_combo.sort()
    for i in range(len(combo)):
        if tmp_combo[i] != i:
            return False
    return True


def of_a_kind(combo: Tuple[int], value: int) -> List:
    roll_counts = Counter(combo)
    satisfied = []
    for num, count in roll_counts.items():
        if count == value:
            satisfied.append(num)
    return satisfied

def count_value(combo: Tuple[int], value: int):
    count = 0
    for v in combo:
        if v == value:
            count += 1
    return count

def is_farkle(combo: Tuple[int]):
    if len(of_a_kind(combo, 6)) > 0 or len(of_a_kind(combo, 5)) > 0 \
    or len(of_a_kind(combo, 4)) > 0 or len(of_a_kind(combo, 3)) > 0 \
    or len(of_a_kind(combo, 2)) == 3 or count_value(combo, 5) > 0 \
    or count_value(combo, 1) > 0:
        return False
    return True

def count_true(fn, lst):
    count = 0
    for entry in lst:
        if fn(entry):
            count += 1
    return count


def is_6_dice(combo):
    if len(of_a_kind(combo, 6)) > 0 or is_straight(combo):
        return True
    

if __name__ == "__main__":
    percentage_fn = lambda fn, lst: ratio_to_percent_str(count_true(fn, lst) / len(lst))
    print(percentage_fn(is_farkle, all_6_combos))
    print(percentage_fn(is_farkle, all_5_combos))
    print(percentage_fn(is_farkle, all_4_combos))
    print(percentage_fn(is_farkle, all_3_combos))
    print(percentage_fn(is_farkle, all_2_combos))
    print(percentage_fn(is_farkle, all_1_combos))