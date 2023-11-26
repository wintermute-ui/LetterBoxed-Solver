# -*- coding: utf-8 -*-
from typing import List, Set, Tuple
import argparse,heapq
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

def prune_words(sigma: List[str], accept_ls: Set[str], sides: List[set], exclude:List[str]=[]) -> List[str]:

    # Get compliment of set of letters
    comple_letters = sigma
    for letter in accept_ls:
        comple_letters.remove(letter)

        
    # Get list of accepted words according to letters allowed
    new_list = []

    with open("words.txt", "r") as f:
        for word in f:  
            w = word.strip()
            if w in exclude:
                continue
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

    def __init__(self, word: str, accepted_letters: Set[str]):
        self.score = self.get_score(word, accepted_letters)
        self.word = word
        self.letters = set([letter for letter in self.word])

    # The smaller the score, the higher value the word is
    def get_score(self, word, accepted_letters: Set[str]) -> int:
        unique_letters_used = set([letter for letter in word])
        total = len(accepted_letters) - len(unique_letters_used)

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
    def encode(self):
        return {'score':self.score, 'word':self.word, 'letters':self.letters}

def compile_solution(accepted_words: List[str], accept_ls: Set[str], t_all:bool=False, n_words:int = -1) -> List[Tuple[str]]:

    # Sort accepted words into dict where the starting character is the key to values of class letterboxd_word (dict(letter:[word1,word2,...]))
    letter_dict = {letter:[letterboxd_word(word, accept_ls) for word in accepted_words if word[0] == letter] for letter in accept_ls}
    for letter in accept_ls:
        heapq.heapify(letter_dict[letter])
    
    best_word_heap = [letterboxd_word(word, accept_ls) for word in accepted_words]
    heapq.heapify(best_word_heap)

    
    # Log past first guesses and solved orders to compare
    completed_letters = set()
    solved_orders = []

    max_iterations = 0

    # Repeat Until Solution
    while (max_iterations < len(accepted_words)): 
        
        # Start on the word with the greatest score
        best_guess = heapq.heappop(best_word_heap)
        
        completed_letters = set()
        solved_order = []
        tmp_dict = {letter:[] for letter in accept_ls}
        for letter in letter_dict:
            for word in letter_dict[letter]:
                tmp_dict[letter].append(word)

        if n_words <= -1:
            rep = 3
        else:
            rep = n_words

        start_letter = best_guess.word[0]
        completed_letters.update(best_guess.letters)
        solved_order.append(best_guess)
        
        if completed_letters == accept_ls and len(solved_order) <= n_words:
                if t_all:
                    if n_words < 0:
                        print(tuple(solved_order))
                        solved_orders.append(solved_order)
                    elif len(solved_order) <= n_words:
                        print(tuple(solved_order))
                        solved_orders.append(solved_order)
                else:
                    count = rep + 1
        
        while len(solved_order) < rep:
            #print(solved_orders)
            start_letter = best_guess.word[-1]
            prev = best_guess

            try:
                best_guess = heapq.heappop(tmp_dict[start_letter])

            except IndexError:
                break


            for word in tmp_dict[start_letter]:
                if len(best_guess.letters - completed_letters) <= len(word.letters - completed_letters):
                    best_guess = word


            solved_order.append(best_guess)
            add_letters = best_guess.letters.difference(completed_letters)
            completed_letters.update(add_letters)

            if completed_letters == accept_ls and len(solved_order) <= n_words:
                if t_all:
                    print(tuple(solved_order))
                    solved_orders.append(solved_order)
                    completed_letters.difference_update(add_letters)
                    solved_order.remove(best_guess)
                    best_guess = prev

                else:
                    break
            
        if completed_letters == accept_ls and not t_all:
            if n_words < 0:
                print(tuple(solved_order))
                solved_orders.append(solved_order)
            elif len(solved_order) <= n_words:
                print(tuple(solved_order))
                solved_orders.append(solved_order)

        max_iterations+=1

    return solved_orders

def solve(letterbox_set: List[List[str]] = [], t_all:bool=False, n:int=0, exclude:List[str]=[]):
    """
    letterbox_set: List of the sides of a letterboxed puzzle (format: [['a','b','c], ['d','e','f], ...])
    """
    if letterbox_set == []:

        # Get User Input (Game Layout, Format: s1 = "abc", s2 = "def", ...)
        ls1 = input("Letters of Side 1: ").strip()
        ls2 = input("Letters of Side 2: ").strip()
        ls3 = input("Letters of Side 3: ").strip()
        ls4 = input("Letters of Side 4: ").strip()
        
        s2 = [l.lower() for l in ls2]
        s1 = [l.lower() for l in ls1]
        s3 = [l.lower() for l in ls3]
        s4 = [l.lower() for l in ls4]

    elif len(letterbox_set) >= 4:
        s1 = letterbox_set[0]
        s2 = letterbox_set[1]
        s3 = letterbox_set[2]
        s4 = letterbox_set[3]

    else:
        print("Invaild Input!")
        exit(1)
    
    accept_letters = set(s1+s2+s3+s4)

    sides = [set(s1),set(s2),set(s3),set(s4)]

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
    prune_list = prune_words(alpha, accept_letters, sides, exclude)

    if n > 0:
        compile_solution(prune_list, accept_letters, t_all, n)
    else:
        compile_solution(prune_list, accept_letters, t_all)

class CommandLine:
    def __init__(self):
        parser = argparse.ArgumentParser(description = "Solves a LetterBoxed square")
        parser.add_argument("side", metavar="S", help="The letters on a side of a Letterboxed square", nargs='*', type=str, default="")
        parser.add_argument("-a", "--all", help= "Find all solutions combinations", required=False, action="store_true", default="")
        parser.add_argument("-n", "--num", help = "Find solution in n words", required = False, type=int, default = 0)
        parser.add_argument("-e", "--exclude", help = "Words excluded from master word list", nargs="+", type=str, default = "")

        argument = parser.parse_args()
        sides = []
        exclusion = []

        if argument.side:
            for s in argument.side:
                sides.append([l.lower() for l in s])
        
        if argument.exclude:
            exclusion = [ex.strip().lower() for ex in argument.exclude]

        solve(sides, argument.all, argument.num, exclusion)
        
        

if __name__ == "__main__":
    app = CommandLine()
