import set10constants

from itertools import combinations
from collections import OrderedDict

class Set10Calculator:
    def __init__(self, level=4, traits=["Heartsteel"], keep=[], highroll= [], gold=0) -> None:
        self.keep = keep
        self.highroll = highroll
        self.level = level # the number of units you can actually play and what units you can reasonably see
        self.gold = gold
        self.desired = traits # list of traits you are okay with

    
    def find_probability(self, total, dead):
        prob = 1
        i = 0 # i is both our iterator as well as our counter for how many choices have been made, which changes the odds for the following choice very slightly since we don't have replacement.
        while i < set10constants.breakpoints[total]:
            prob *= self.find_specific_prob(total - i - dead, len(self.desired)) 
            i += 1
            # (i-1)(okayTraits * i) -> every iteration, we are calculating odds that the number of okay traits weren't chosen. 
            # Ex: Suppose we have 8 traits in and we are looking for 2 traits. We have 2 tailored choices.
            # We are also assuming we have EDM in right now, which is a trait that can't get an emblem.
            # First iteration, we calculate the odds of not hitting to be 5/7. key - i - dead = 8 - 0 - 1 = 7, so this adds up
            # Second iteration, we calculate the odds of not hitting to be 4/6. key - i - dead = 8 - 1 - 1 = 6
        while i < 4:
            prob *= self.find_specific_prob(len(set10constants.traits["has_emblem"]) - i, len(self.desired))
            i += 1
            # Ex: From before, suppose we have 8 traits in and we are looking for 2 traits. We have 2 tailored choices.
            # Third iteration, we have chosen twice, which means there are 21 options. 
            # We calculate the odds of not hitting to be 19/21. 24 - i - dead = 21
            # Fourth iteration, we calculate the odds of not hitting to be 18/20. 24 - i - dead = 20
        return 1 - prob
    
    def find_specific_prob(self, choices, desired):
        if choices <= 0:
            return 0
        else:
            return max((choices - desired) / choices, 0) # if probability is negative, then change to 0

    def evaluate_combo(self, combo, breakpoints, desired_traits):
        # Count traits and check for desired traits in one pass
        combo_traits = set(trait for champ in combo for trait in champ['traits'])
        trait_count = len(combo_traits)

        # check if combo has all desired traits
        contains_desired = all(trait in combo_traits for trait in desired_traits)

        # check if combo contains all required units
        contains_keep = all(set10constants.champions_by_name[unit] in combo for unit in self.keep)

        return trait_count in breakpoints and contains_desired and contains_keep

    def find_boards(self): 
        champ_list = []
        for i in range(1, set10constants.max_cost[self.level] + 1):
            champ_list += set10constants.champions_by_cost[i]
        
        for unit in self.highroll:
            if set10constants.champions_by_name[unit] not in champ_list:
                champ_list.append(unit)

        # Generate all combinations of champions based on the player's level
        possible_combinations = list(combinations(champ_list, self.level))

        print(len(possible_combinations))

        # Filter combinations based on trait breakpoints and desired traits
        valid_boards = [combo for combo in possible_combinations if self.evaluate_combo(combo, set10constants.breakpoints.keys(), self.desired)]

        return valid_boards

    def find_board_probability(self, board):
        board_traits = set(trait for champ in board for trait in champ['traits'])

        trait_count = len(board_traits)

        dead = 0

        for trait in board_traits:
            if trait in set10constants.traits["no_emblem"]:
                dead += 1
        
        return self.find_probability(trait_count, dead)



    def get_best_comps(self):
        boards = self.find_boards()

        print('boards complete')

        probability_dictionary = {}

        trait_dictionary = {}

        for board in boards:
            board_units = [champ['name'] for champ in board]
            board_traits = tuple(set(trait for champ in board for trait in champ['traits']))

            if board_traits in trait_dictionary:
                probability = trait_dictionary[board_traits]
            else:
                probability = self.find_board_probability(board)

            if probability not in probability_dictionary:
                probability_dictionary[probability] = []

            if board_traits not in trait_dictionary:
                trait_dictionary[board_traits] = probability
            
            probability_dictionary[probability].append(board_units)
        
        sorted_prob_dict = OrderedDict(sorted(probability_dictionary.items(), reverse = True))

        best = list(sorted_prob_dict.items())[0]

        print('The highest probability is: ', best[0])
        print('These are valid comps:')
        for comp in best[1]:
            print(comp)

        print('The highest probability is: ', best[0])


def main():
    early_heart = Set10Calculator(4, ["Heartsteel"], ["K'Sante"])

    middle_viego = Set10Calculator(7, ['Pentakill', 'Edgelord'], ["Yone", "Viego", "Riven"], ["AkaliT","AkaliK","Viego"])

    early_heart.get_best_comps()

    middle_viego.get_best_comps()


if __name__ == "__main__":
    main()