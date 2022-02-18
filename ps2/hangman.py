# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("->", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    guess = ''
    for char in secret_word:
        for letter in letters_guessed:
            if char == letter:
                guess += char
            else: continue
    return guess == secret_word


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    guess = ''
    for char in secret_word:
        if char in letters_guessed:
            guess += char
        else: guess += '_ '
    return guess


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    alph = list(string.ascii_lowercase)
    loop_alph = alph[:]
    for l in loop_alph:
        if l in letters_guessed:
            alph.remove(l)
        else: continue
    
    return ''.join(sorted(alph))
            
        

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''

    secret_letters = str(len(secret_word))
    full_alpha = list(string.ascii_letters)
    requirements = {'guesses_left': 6, 
                    'warnings_left': 3, 
                    'letters_guessed' : [], 
                    'user_input': '', 
                    'final_score' : 0}
    
    def border():
        print('--------')
    
    def invalid_input(requirements):
        if requirements['warnings_left'] > 1:
            requirements['warnings_left'] -= 1
            print('Oops! That is not a valid letter. You have ' + 
                  str(requirements['warnings_left']) + 
                  ' warnings left: ' + 
                  get_guessed_word(secret_word, requirements['letters_guessed']))
        elif requirements['warnings_left'] <= 1:
            requirements['guesses_left'] -= 1
            print('Oops! That is not a valid letter. You have ' + 
                  str(requirements['guesses_left']) + 
                  ' guesses left: ' + 
                  get_guessed_word(secret_word, requirements['letters_guessed']))
        return requirements
        
    def invalid_guess(requirements):
        if requirements['warnings_left'] > 1:
            requirements['warnings_left'] -= 1
            print("Oops! You've already guessed that letter. You now have " + 
                  str(requirements['warnings_left']) + 
                  " warnings left : " + 
                  get_guessed_word(secret_word, requirements['letters_guessed']))
        elif requirements['warnings_left'] <= 1:
            requirements['guesses_left'] -= 1
            print("Oops! You've already guessed that letter. You now have " + 
                  str(requirements['guesses_left']) + 
                  " guesses left: " + 
                  get_guessed_word(secret_word, requirements['letters_guessed']))
        return requirements       
        
    def wrong_guess(requirements):
        vowels = ['a', 'e', 'i', 'o', 'u']
        if requirements['user_input'] in vowels:
            requirements['guesses_left'] -= 2
            if requirements['guesses_left'] >= 0:
                print("Oops! That letter is not in my word. You now have " + 
                      str(requirements['guesses_left']) + 
                      " guesses left : " + 
                      get_guessed_word(secret_word, requirements['letters_guessed']))
            elif requirements['guesses_left'] < 0:
                print("Oops! That letter is not in my word. You now have no more guesses left : " + 
                      get_guessed_word(secret_word, requirements['letters_guessed']))
        else:
            requirements['guesses_left'] -= 1
            print("Oops! That letter is not in my word. You now have " + 
                  str(requirements['guesses_left']) + 
                  " guesses left : " + 
                  get_guessed_word(secret_word, requirements['letters_guessed']))
        return requirements
        
    def correct_guess(requirements):
        print('Good guess: ' + get_guessed_word(secret_word, requirements['letters_guessed']))

    def final_score(requirements):
        unique_letters = 0
        for c in requirements['letters_guessed']:
            if c in secret_word:
                unique_letters += 1
        requirements['final_score'] = requirements['guesses_left'] * unique_letters
        return requirements                      
                
    def welcomemessage(secret_letters, requirements):
        print('Welcome to the game Hangman!')
        print('I am thinking of a word that is ' + secret_letters + ' letters long')
        print('You have ' + str(requirements['warnings_left']) + ' warnings left')
        border()
    
    def preround(requirements):
        print('You have ' + str(requirements['guesses_left']) + ' guesses left')
        print('Available letters: ' + get_available_letters(requirements['letters_guessed']))
        return requirements
        
    def begin_round(requirements):      
        requirements['user_input'] = input('Please guess a letter: ')
        # check input is LETTER, else NOT letter
        if requirements['user_input'] in full_alpha and len(requirements['user_input']) == 1:
            requirements['user_input'] = requirements['user_input'].lower()
            # check input UNGUESSED, else already guessed
            if requirements['user_input'] not in requirements['letters_guessed']:
                requirements['letters_guessed'].append(requirements['user_input'])
                # check input CORRECT, else incorrect
                if requirements['user_input'] in secret_word:
                    correct_guess(requirements)
                else: wrong_guess(requirements)
            else: invalid_guess(requirements) 
        else: invalid_input(requirements)        
        border()
        # print('TEST. ', requirements)
        return requirements
    
    
    '''
    the actual running of the game
    '''
    welcomemessage(secret_letters, requirements)
    while requirements['guesses_left'] > 0 and not is_word_guessed(secret_word, requirements['letters_guessed']):
        preround(requirements)
        begin_round(requirements)
        #print('TEST. ', requirements)
     
        #check guesses left
        #check is word is guessed
        if requirements['guesses_left'] < 1 and not is_word_guessed(secret_word, requirements['letters_guessed']):
            print('L + bozo + gg + ez. The word was ' + secret_word)
            break
        elif requirements['guesses_left'] > 0 and is_word_guessed(secret_word, requirements['letters_guessed']):
            print('Congratulations, you won!')
            print('Your total score for this game is: ', final_score(requirements)['final_score'])
            break
            


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
       
    stripped_word = my_word.replace("_ ", "_")
    
    match = 0
    for i in range(len(stripped_word)):
        if len(stripped_word) == len(other_word):
            if stripped_word[i] == '_':
                if other_word[i] not in stripped_word:
                    match += 1
                    continue
                elif other_word[i] in stripped_word: continue
            elif stripped_word[i] == other_word[i]:
                match += 1
                continue
            else: continue
        else: continue
#    print("matchedpts", match, "lenother", len(other_word), "strippedword", stripped_word)
    return match == len(other_word) 


def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''

    matches = []
    for word in wordlist:
        if match_with_gaps(my_word, word):
            matches.append(word)
        else: continue
    
    if len(matches) >= 1:
        return print(' '.join(matches))
    else: return print('No matches found')


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''

    secret_letters = str(len(secret_word))
    full_alpha = list(string.ascii_letters)
    requirements = {'guesses_left': 6, 
                    'warnings_left': 3, 
                    'letters_guessed' : [], 
                    'user_input': '', 
                    'final_score' : 0}
    
    def border():
        print('--------')
    
    def invalid_input(requirements):
        if requirements['warnings_left'] > 1:
            requirements['warnings_left'] -= 1
            print('Oops! That is not a valid letter. You have ' + 
                  str(requirements['warnings_left']) + 
                  ' warnings left: ' + 
                  get_guessed_word(secret_word, requirements['letters_guessed']))
        elif requirements['warnings_left'] <= 1:
            requirements['guesses_left'] -= 1
            print('Oops! That is not a valid letter. You have ' + 
                  str(requirements['guesses_left']) + 
                  ' guesses left: ' + 
                  get_guessed_word(secret_word, requirements['letters_guessed']))
        return requirements
        
    def invalid_guess(requirements):
        if requirements['warnings_left'] > 1:
            requirements['warnings_left'] -= 1
            print("Oops! You've already guessed that letter. You now have " + 
                  str(requirements['warnings_left']) + 
                  " warnings left : " + 
                  get_guessed_word(secret_word, requirements['letters_guessed']))
        elif requirements['warnings_left'] <= 1:
            requirements['guesses_left'] -= 1
            print("Oops! You've already guessed that letter. You now have " + 
                  str(requirements['guesses_left']) + 
                  " guesses left: " + 
                  get_guessed_word(secret_word, requirements['letters_guessed']))
        return requirements    
        
    def wrong_guess(requirements):
        vowels = ['a', 'e', 'i', 'o', 'u']
        if requirements['user_input'] in vowels:
            requirements['guesses_left'] -= 2
            if requirements['guesses_left'] >= 0:
                print("Oops! That letter is not in my word. You now have " + 
                      str(requirements['guesses_left']) + 
                      " guesses left : " + 
                      get_guessed_word(secret_word, requirements['letters_guessed']))
            elif requirements['guesses_left'] < 0:
                print("Oops! That letter is not in my word. You now have no more guesses left : " + 
                      get_guessed_word(secret_word, requirements['letters_guessed']))
        else:
            requirements['guesses_left'] -= 1
            print("Oops! That letter is not in my word. You now have " + 
                  str(requirements['guesses_left']) + 
                  " guesses left : " + 
                  get_guessed_word(secret_word, requirements['letters_guessed']))
        return requirements
        
    def correct_guess(requirements):
        print('Good guess: ' + get_guessed_word(secret_word, requirements['letters_guessed']))

    def final_score(requirements):
        unique_letters = 0
        for c in requirements['letters_guessed']:
            if c in secret_word:
                unique_letters += 1
        requirements['final_score'] = requirements['guesses_left'] * unique_letters
        return requirements                      
                
    def welcomemessage(secret_letters, requirements):
        print('Welcome to the game Hangman!')
        print('I am thinking of a word that is ' + secret_letters + ' letters long')
        print('You have ' + str(requirements['warnings_left']) + ' warnings left')
        border()
    
    def preround(requirements):
        print('You have ' + str(requirements['guesses_left']) + ' guesses left')
        print('Available letters: ' + get_available_letters(requirements['letters_guessed']))
        return requirements
        
    def begin_round(requirements):      
        requirements['user_input'] = input('Please guess a letter: ')
        # check input is LETTER, elif HINT, else NOT letter
        if requirements['user_input'] in full_alpha and len(requirements['user_input']) == 1:
            requirements['user_input'] = requirements['user_input'].lower()
            # check input UNGUESSED, else already guessed
            if requirements['user_input'] not in requirements['letters_guessed']:
                requirements['letters_guessed'].append(requirements['user_input'])
                # check input CORRECT, else incorrect
                if requirements['user_input'] in secret_word:
                    correct_guess(requirements)
                else: wrong_guess(requirements)
            else: invalid_guess(requirements) 
        elif requirements['user_input'] == '*':
            show_possible_matches(get_guessed_word(secret_word, requirements['letters_guessed']))
        else: invalid_input(requirements)        
        border()
        # print('TEST. ', requirements)
        return requirements
    
    
    '''
    the actual running of the game
    '''
    welcomemessage(secret_letters, requirements)
    while requirements['guesses_left'] > 0 and not is_word_guessed(secret_word, requirements['letters_guessed']):
        preround(requirements)
        begin_round(requirements)
        #print('TEST. ', requirements)
     
        #check guesses left
        #check is word is guessed
        if requirements['guesses_left'] < 1 and not is_word_guessed(secret_word, requirements['letters_guessed']):
            print('L + bozo + gg + ez. The word was ' + secret_word)
            break
        elif requirements['guesses_left'] > 0 and is_word_guessed(secret_word, requirements['letters_guessed']):
            print('Congratulations, you won!')
            print('Your total score for this game is: ', final_score(requirements)['final_score'])
            break
#    pass



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    # secret_word = choose_word(wordlist)
    # secret_word = 'apple'
    # hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
