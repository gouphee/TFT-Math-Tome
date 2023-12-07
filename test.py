import numpy as np
from generic_calculator import GenericCalculator

def main():
    prob_list = []
    for i in range(0, 4):
        board = GenericCalculator(2, i, 23)
        probs = board.find_probability()
        prob_list.append(probs)
    print(prob_list)

if __name__ == "__main__":
    main()