import set10constants

from itertools import combinations
from collections import OrderedDict

#import plotly.express as px



class Generic_Calculator:
    def __init__(self, desired=1, dead=0, total_emblems=24) -> None:
        self.desired = desired # number of traits you are okay with
        self.dead = dead # number of dead traits you have
        self.all = total_emblems # number of traits with emblems

    
    def find_probability(self):
        probabilities = []
        for key, value in set10constants.breakpoints.items():
            prob = 1
            i = 0 # i is both our iterator as well as our counter for how many choices have been made, which changes the odds for the following choice very slightly since we don't have replacement.
            while i < value:
                prob *= self.find_specific_prob(key - i - self.dead, self.desired) 
                i += 1
                # (i-1)(okayTraits * i) -> every iteration, we are calculating odds that the number of okay traits weren't chosen. 
                # Ex: Suppose we have 8 traits in and we are looking for 2 traits. We have 2 tailored choices.
                # We are also assuming we have EDM in right now, which is a trait that can't get an emblem.
                # First iteration, we calculate the odds of not hitting to be 5/7. key - i - dead = 8 - 0 - 1 = 7, so this adds up
                # Second iteration, we calculate the odds of not hitting to be 4/6. key - i - dead = 8 - 1 - 1 = 6
            while i < 4:
                prob *= self.find_specific_prob(self.all - i, self.desired)
                i += 1
                # Ex: From before, suppose we have 8 traits in and we are looking for 2 traits. We have 2 tailored choices.
                # Third iteration, we have chosen twice, which means there are 21 options. 
                # We calculate the odds of not hitting to be 19/21. 24 - i - dead = 21
                # Fourth iteration, we calculate the odds of not hitting to be 18/20. 24 - i - dead = 20
            probabilities.append(1 - prob)
        return probabilities
    
    def find_specific_prob(self, choices, desired):
        if choices <= 0:
            return 0
        else:
            return max((choices - desired) / choices, 0) # if probability is negative, then change to 0



