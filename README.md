# LetterBoxed-Solver

A Python-based solver for the New York Times game, created by Sam Ezersky, known as Letter Boxed. 
## What is Letterboxed?

Letter Boxed is a word forming game not disimilar to a game like _Scrabble_. 
The game is built off of tweleve unique English letters that distributed across four sides of a square (three letters per side). 

The goal of the game is to use only these letters in the words you form, with the first letter of each subsuquent word being the same as the last letter of the current; completing the game requires all the letters in the square to be used somewhere in the words created.
An additional cavet is that, for any two consecutive letters, the two letters must not be on the same side of the square.    

The actual rules below were taken from this NYT article (https://www.nytimes.com/2022/01/19/crosswords/letter-boxed-tips-and-tricks.html)

![The rules of Letter Boxed](https://static01.nyt.com/images/2022/01/11/crosswords/wordplay-lbrules/wordplay-lbrules-superJumbo.png?quality=75&auto=webp)

## Solving Letter Boxed

The solution to this task is seemingly straight-forward: 
1. Import a list of words (included words.txt in repo)
```
word_list = []    
with open("words.txt", "r") as f:
    for word in f:
        word_list.append(word) 
```
3. Input the sides and letters of a Letter Boxed game
4. Parse and remove entries in the list of words that are impossible to use in the game (i.e. don't follow the rules)

5. Score the words remaining by the unique letters used in each word
6. Sort the words into tables where the first letter of the word is the key to the word itself ('a': ['apple','acting',...], ... )
7. Start with the best scoring word and run the process below.
   - If the letters of our current word are all letters in our game: our answer is just our current word.
   - If the letters of our current word are not all letters: run process on the best word in the list of words with the first letter equal to the last letter of our current word.
   - If there is an order of words that follow the first-last letter rule that also contain all the letters in our game: our answer is the words used in order.
   - If there are no more remaining words to use and still unused letters in the game: repeat with the next best word in our list.
8. If all of that works correctly, we should get all possible soultions to the set of sides and letters of our Letter Boxed game.

 

   
