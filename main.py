import itertools
import random
from typing import List, Tuple
from collections import Counter
from tqdm import tqdm

WIN_SCORE = 10000

SCORES = {
    "straight": 2000,
    "6-same": WIN_SCORE,
    "2-sets-of-3": 2500,
    "5-same": 2000,
    "4-same": 1500,
    "3-pair": 1500,
    
    "3-same": {
        "1": 1000,
        "2": 200,
        "3": 300,
        "4": 400,
        "5": 500,
        "6": 600,
    },

    "one": 100,
    "five": 50,
}

def roll_dice(num_dice, num_sides=6):
    """
    Simulates rolling 'num_dice' number of dice with 'num_sides' faces each.
    
    Parameters:
        num_dice (int): The number of dice to roll.
        num_sides (int): The number of faces on each die. Default is 6.
        
    Returns:
        list: A list containing the result of each dice roll.
    """
    if num_dice < 1 or num_sides < 2:
        return []
    
    return [random.randint(1, num_sides) for _ in range(num_dice)]

def is_straight(rolls: List[int], total_num_dice: int) -> bool:
    if len(rolls) < total_num_dice:
        return False
    
    rolls.sort()
    for i in range(len(rolls)):
        if rolls[i] != i:
            return False
    return True

def of_a_kind(rolls: List[int], value: int) -> List:
    roll_counts = Counter(rolls)
    satisfied = []
    for num, count in roll_counts.items():
        if count == value:
            satisfied.append(num)
            rolls = [x for x in rolls if x != num]
    return satisfied, rolls


def count_value(rolls: Tuple[int], value: int):
    count = 0
    for v in rolls:
        if v == value:
            count += 1
    return count

def is_farkle(combo: Tuple[int]):
    if len(of_a_kind(combo, 6)[0]) > 0 or len(of_a_kind(combo, 5)[0]) > 0 \
    or len(of_a_kind(combo, 4)[0]) > 0 or len(of_a_kind(combo, 3)[0]) > 0 \
    or len(of_a_kind(combo, 2)[0]) == 3 or count_value(combo, 5) > 0 \
    or count_value(combo, 1) > 0:
        return False
    return True

def farkle_score(rolls: List[int], total_num_dice: int) -> Tuple[int, List[int]]:
    if is_farkle(rolls) or len(rolls) == 0:
        return 0, rolls
    elif is_straight(rolls, total_num_dice):
        return SCORES["straight"], []
    elif len(of_a_kind(rolls, 2)[0]) == 3:
        return SCORES["3-pair"], []
    elif len(of_a_kind(rolls, 3)[0]) == 2:
        return SCORES["2-sets-of-3"], []
    
    score = 0
    if len(of_a_kind(rolls, 5)[0]) > 0:
        five_same = of_a_kind(rolls, 5)[1]
        score += SCORES["5-same"]
        rolls = five_same
    if len(of_a_kind(rolls, 4)[0]) > 0:
        four_same = of_a_kind(rolls, 4)[1]
        score += SCORES["4-same"]
        rolls = four_same
    if len(of_a_kind(rolls, 3)[0]) > 0:
        three_same = of_a_kind(rolls, 3)
        if len(three_same[0]) > 1:
            raise Exception("three_same should have 1 entry")
        score += SCORES["3-same"][str(three_same[0][0])]
        rolls = three_same[1]
    
    score += SCORES["one"] * count_value(rolls, 1) + SCORES["five"] * count_value(rolls, 5)
    rolls = [x for x in rolls if x != 5 and x != 1]
    return score, rolls

def add_to_scoring_dict(scoring, value):
    if value in scoring:
        scoring[value] += 1
    else:
        scoring[value] = 1
    return scoring

if __name__ == "__main__":
    # Counters and parameters
    num_sides = 6
    total = 0
    count = 0
    
    scoring = {}
    with tqdm() as pbar:
        while True:
            this_hand = 0
            num_dice = 6
            # original roll of num_dice
            rolls = roll_dice(num_dice, num_sides)
            tmp = farkle_score(rolls, num_dice)

            # there are dice left that didn't count for a previous score, roll them again until you farkle
            while tmp[0] > 0:
                this_hand += tmp[0]
                total += tmp[0]
                num_dice = len(tmp[1])
                rolls = roll_dice(num_dice, num_sides)
                tmp = farkle_score(rolls, num_dice)

            scoring = add_to_scoring_dict(scoring, this_hand)

            count += 1
            pbar.update(1)
            if count % 50 == 0:
                pbar.set_description(f"Average score: {total / count:.2f}")

            if count % 1000000 == 0:
                for k, v in scoring.items():
                    tmp = round((v / count) * 100, 2)
                    if tmp != 0:
                        print(k, tmp)
