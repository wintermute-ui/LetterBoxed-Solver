# -*- coding: utf-8 -*-
from typing import List, Set, Tuple
"""
GAME RULES (according to NYT)
------------------------------------------------------------------
1.  Connect letters to spell words.
2.  Words must be at least 3 letters long.
3.  Letters can be reused.
4.  Consecutive letters cannot be from the same side.
5.  The last letter of a word becomes the first letter of the next word.
6.  Use all letters to solve!
------------------------------------------------------------------
"""
def filter_words(filename: str) -> None:
    """
    Takes a text filename containing a list of words (format: w1\nw2\n...) and writes a new file with words formatted to follow the rules of NYT's LetterBoxd Game
    """
    word_list = []

    with open(filename, "r") as f:
        for word in f:
            w = word.strip()
            l = len(w.strip())

            if l >= 3:
                index = 0
                consecutive = False
                while index < l-1:
                    if w[index] == w[index+1]:
                        consecutive = True
                        break
                    index += 1
                
                if not consecutive:
                    word_list.append(w)
        
    with open("words.txt", "w") as f:
        for word in word_list:
            f.write(word.lower() + "\n")

def prune_words(sigma: List[str], accept_ls: Set[str], sides: List[set]) -> List[str]:

    # Get compliment of set of letters
    comple_letters = sigma
    for letter in accept_ls:
        comple_letters.remove(letter)

        
    # Get list of accepted words according to letters allowed
    new_list = []
        
    with open("words.txt", "r") as f:
        for word in f:
            w = word.strip()
            not_in = False
            for letter in comple_letters:
                if letter in w:
                    not_in = True
                    break
            
            if not not_in:
                new_list.append(w)

    return_list = []
    
    # Remove words that cannot be reached (consecutive letters on the same side)
    for word in new_list:

        removed = False
        for side in sides:
            if removed:
                break
            i = 0
            while i < len(word)-1:

                if (word[i] in side) and (word[i+1] in side):

                    removed = True
                    break
                i += 1
        
        if not removed:
            return_list.append(word)
                

    return return_list

class letterboxd_word:

    def __init__(self, word: str):
        self.score = self.get_score(word)
        self.word = word
        self.letters = set([letter for letter in self.word])

    def get_score(self, word) -> int:
        unique_letters_used = set([letter for letter in word])
        total = len(word) + len(unique_letters_used)

        return total

    def __lt__(self, other):
        return self.score < other.score
    def __le__(self, other):
        return self.score <= other.score
    def __eq__(self, other):
        return self.score == other.score and self.word == other.word
    def __ne__(self, other):
        return self.score != other.score and self.word != other.word
    def __gt__(self, other):
        return self.score > other.score
    def __ge__(self, other):
        return self.score >= other.score
    
    def __repr__(self):
        return f"'{self.word}' ({self.score})"
    def __str__(self):
        return f"'{self.word}' ({self.score})"

def compile_solution_in_n(accepted_words: List[str], accept_ls: Set[str], n_words:int) -> List[Tuple[str]]:

    # Sort accepted words into dict where the starting character is the key to values of class letterboxd_word (dict(letter:[word1,word2,...]))
    letter_dict = {letter:[letterboxd_word(word) for word in accepted_words if word[0] == letter] for letter in accept_ls}

    for key in letter_dict:
        letter_dict[key].sort(reverse=True)

    # Log past first guesses and solved orders to compare
    completed_letters = set()
    first_guesses = []
    solved_orders = []

    max_iterations = 0

    # Repeat Until Solution
    while (max_iterations < len(accepted_words)): 
        # Start on the word with the greatest score
        best_guess = letterboxd_word("")
        for key in letter_dict:
            for word in letter_dict[key]:
                if word in first_guesses:
                    continue
                if best_guess.score > word.score:
                    continue
                else:
                    best_guess = word

        completed_letters = set()
        solved_order = []
        count = 0

        start_letter = best_guess.word[0]
        # add best_guess to first_guesses as to not reuse when retrying
        first_guesses.append(best_guess)
        completed_letters.update(best_guess.letters)
        solved_order.append(best_guess)

        while completed_letters != accept_ls and count < 3:
            #print(completed_letters, ":", accept_ls, completed_letters==accept_ls)

            start_letter = best_guess.word[-1]
            if letter_dict[start_letter]:
                best_guess = letter_dict[start_letter][0]
            else:
                break

            for word in letter_dict[start_letter]:
                if len(best_guess.letters - completed_letters) < len(word.letters - completed_letters):
                    best_guess = word

            #letter_dict[start_letter].remove(best_guess)
            completed_letters.update(best_guess.letters)
            solved_order.append(best_guess)

            count += 1

        if completed_letters == accept_ls:
            if len(solved_order) <= n_words:
                solved_orders.append(solved_order)

        max_iterations+=1
    
    return solved_orders

def compile_all_solutions(accepted_words: List[str], accept_ls: Set[str]) -> List[Tuple[str]]:

    # Sort accepted words into dict where the starting character is the key to values of class letterboxd_word (dict(letter:[word1,word2,...]))
    letter_dict = {letter:[letterboxd_word(word) for word in accepted_words if word[0] == letter] for letter in accept_ls}

    for key in letter_dict:
        letter_dict[key].sort(reverse=True)

    # Log past first guesses and solved orders to compare
    completed_letters = set()
    first_guesses = []
    solved_orders = []

    max_iterations = 0

    # Repeat Until Solution
    while (max_iterations < len(accepted_words)): 
        # Start on the word with the greatest score
        best_guess = letterboxd_word("")
        for key in letter_dict:
            for word in letter_dict[key]:
                if word in first_guesses:
                    continue
                if best_guess.score > word.score:
                    continue
                else:
                    best_guess = word

        completed_letters = set()
        solved_order = []
        count = 0

        start_letter = best_guess.word[0]
        # add best_guess to first_guesses as to not reuse when retrying
        first_guesses.append(best_guess)
        completed_letters.update(best_guess.letters)
        solved_order.append(best_guess)

        while completed_letters != accept_ls and count < 3:
            #print(completed_letters, ":", accept_ls, completed_letters==accept_ls)

            start_letter = best_guess.word[-1]
            if letter_dict[start_letter]:
                best_guess = letter_dict[start_letter][0]
            else:
                break

            for word in letter_dict[start_letter]:
                if len(best_guess.letters - completed_letters) < len(word.letters - completed_letters):
                    best_guess = word

            #letter_dict[start_letter].remove(best_guess)
            completed_letters.update(best_guess.letters)
            solved_order.append(best_guess)

            count += 1

        if completed_letters == accept_ls:
            solved_orders.append(solved_order)

        max_iterations+=1

    return solved_orders
          
def print_solution_in_n(accepted_words: List[str], accept_ls: Set[str], n_words:int) -> None:

    # Sort accepted words into dict where the starting character is the key to values of class letterboxd_word (dict(letter:[word1,word2,...]))
    letter_dict = {letter:[letterboxd_word(word) for word in accepted_words if word[0] == letter] for letter in accept_ls}

    for key in letter_dict:
        letter_dict[key].sort(reverse=True)

    # Log past first guesses and solved orders to compare
    completed_letters = set()
    first_guesses = []
    solved_orders = []

    max_iterations = 0

    # Repeat Until Solution
    while (max_iterations < len(accepted_words)): 
        # Start on the word with the greatest score
        best_guess = letterboxd_word("")
        for key in letter_dict:
            for word in letter_dict[key]:
                if word in first_guesses:
                    continue
                if best_guess.score > word.score:
                    continue
                else:
                    best_guess = word

        completed_letters = set()
        solved_order = []
        count = 0

        start_letter = best_guess.word[0]
        # add best_guess to first_guesses as to not reuse when retrying
        first_guesses.append(best_guess)
        completed_letters.update(best_guess.letters)
        solved_order.append(best_guess)

        while completed_letters != accept_ls and count < 3:
            #print(completed_letters, ":", accept_ls, completed_letters==accept_ls)

            start_letter = best_guess.word[-1]
            if letter_dict[start_letter]:
                best_guess = letter_dict[start_letter][0]
            else:
                break

            for word in letter_dict[start_letter]:
                if len(best_guess.letters - completed_letters) < len(word.letters - completed_letters):
                    best_guess = word

            #letter_dict[start_letter].remove(best_guess)
            completed_letters.update(best_guess.letters)
            solved_order.append(best_guess)

            count += 1

        if completed_letters == accept_ls:
            if len(solved_order) <= n_words:
                print(tuple(solved_order))
                solved_orders.append(solved_order)

        max_iterations+=1
    
    if len(solved_orders) == 0:
        print(f"No Solution Found in {n_words} words!")

def print_all_solutions(accepted_words: List[str], accept_ls: Set[str]) -> None:

    # Sort accepted words into dict where the starting character is the key to values of class letterboxd_word (dict(letter:[word1,word2,...]))
    letter_dict = {letter:[letterboxd_word(word) for word in accepted_words if word[0] == letter] for letter in accept_ls}

    for key in letter_dict:
        letter_dict[key].sort(reverse=True)

    # Log past first guesses and solved orders to compare
    completed_letters = set()
    first_guesses = []
    solved_orders = []

    max_iterations = 0

    # Repeat Until Solution
    while (max_iterations < len(accepted_words)): 
        # Start on the word with the greatest score
        best_guess = letterboxd_word("")
        for key in letter_dict:
            for word in letter_dict[key]:
                if word in first_guesses:
                    continue
                if best_guess.score > word.score:
                    continue
                else:
                    best_guess = word

        completed_letters = set()
        solved_order = []
        count = 0

        start_letter = best_guess.word[0]
        # add best_guess to first_guesses as to not reuse when retrying
        first_guesses.append(best_guess)
        completed_letters.update(best_guess.letters)
        solved_order.append(best_guess)

        while completed_letters != accept_ls and count < 3:
            #print(completed_letters, ":", accept_ls, completed_letters==accept_ls)

            start_letter = best_guess.word[-1]
            if letter_dict[start_letter]:
                best_guess = letter_dict[start_letter][0]
            else:
                break

            for word in letter_dict[start_letter]:
                if len(best_guess.letters - completed_letters) < len(word.letters - completed_letters):
                    best_guess = word

            #letter_dict[start_letter].remove(best_guess)
            completed_letters.update(best_guess.letters)
            solved_order.append(best_guess)

            count += 1

        if completed_letters == accept_ls:
            print(tuple(solved_order))
            solved_orders.append(solved_order)

        max_iterations+=1
        

if __name__ == "__main__":
    # filter_words("Collins_Scrabble_Words.txt")
        
    # Get User Input (Game Layout)
    reset = 0
    while not reset:
        ls11 = input("Letter 1 of side 1: ").strip().lower()
        ls21 = input("Letter 2 of side 1: ").strip().lower()
        ls31 = input("Letter 3 of side 1: ").strip().lower()
        reset = 1
        #reset = input(f"Side 1 = {[ls11, ls21, ls31]} [y/n] ") != "n"
    print("")

    reset = 0
    while not reset:
        ls12 = input("Letter 1 of side 2: ").strip().lower()
        ls22 = input("Letter 2 of side 2: ").strip().lower()
        ls32 = input("Letter 3 of side 2: ").strip().lower()
        reset = 1
        #reset = input(f"Side 2 = {[ls12, ls22, ls32]} [y/n] ") != "n"
    print("")

    reset = 0
    while not reset:
        ls13 = input("Letter 1 of side 3: ").strip().lower()
        ls23 = input("Letter 2 of side 3: ").strip().lower()
        ls33 = input("Letter 3 of side 3: ").strip().lower()
        reset = 1
        #reset = input(f"Side 3 = {[ls13, ls23, ls33]} [y/n] ") != "n"
    print("")

    reset = 0
    while not reset:
        ls14 = input("Letter 1 of side 4: ").strip().lower()
        ls24 = input("Letter 2 of side 4: ").strip().lower()
        ls34 = input("Letter 3 of side 4: ").strip().lower()
        reset = 1
        #reset = input(f"Side 4 = {[ls14, ls24, ls34]} [y/n] ") != "n"
    print("")

    
    s1 = set([ls11, ls21, ls31])
    s2 = set([ls12, ls22, ls32])
    s3 = set([ls13, ls23, ls33])
    s4 = set([ls14, ls24, ls34])

    accept_letters = set([ls11, ls21, ls31, ls12, ls22, ls32, ls13, ls23, ls33, ls14, ls24, ls34])

    sides = [s1,s2,s3,s4]
    # print(sides)

    # Check input follows game setup rules
    if len(accept_letters) != 12:
        print("Invaild Input!")
        exit(1)
            
    for side in sides:
        if len(side) < 3:
            print("Invaild Input!")
            exit(1)
        for letter in side:
            if len(letter) > 1 or len(letter) <= 0:
                print("Invaild Input!")
                exit(1)

    alpha = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    prune_list = prune_words(alpha, accept_letters, sides)
    
    # solution_list = compile_all_solutions(prune_list, accept_letters)

    # solution_list.sort(key=lambda s: len(s))

    # print(solution_list)

    # print(prune_list, len(prune_list))

    print_all_solutions(prune_list, accept_letters)
        
    