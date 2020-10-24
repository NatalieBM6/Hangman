
HANGMAN_ASCII_ART = """
  _    _                                         
 | |  | |                                        
 | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
 |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
 | |  | | (_| | | | | (_| | | | | | | (_| | | | |
 |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                      __/ |                      
                     |___/ """
MAX_TRIES = 6

# Different levels of the hangman:
picture_1 = """    x-------x"""
picture_2 = """    x-------x
    |
    |
    |
    |
    |
"""
picture_3 = """    x-------x
    |       |
    |       0
    |
    |
    |"""
picture_4 = """    x-------x
    |       |
    |       0
    |       |
    |
    |"""
picture_5 = """    x-------x
    |       |
    |       0
    |      /|\\
    |
    |"""
picture_6 = """    x-------x
    |       |
    |       0
    |      /|\\
    |      /
    |
"""
picture_7 = """    x-------x
    |       |
    |       0
    |      /|\\
    |      / \\
    |"""
HANGMAN_PHOTOS = {0: picture_1, 1: picture_2, 2: picture_3, 3: picture_4, 4: picture_5, 5: picture_6, 6: picture_7}


''' This function prints the logo of the game.
:param logo: the logo of the game.'''
def print_opening_screen(logo):
    print(logo)
    print(MAX_TRIES)

''' This function prints the current situation of HANGMAN_PHOTOS (one of seven).
:param num_of_tries: an int that represents how many failed tries the user has had.'''
def print_hangman(num_of_tries):
    print(HANGMAN_PHOTOS[num_of_tries])


''' This function checks if the input from the user is valid or not.
:param letter_guessed: the letter the user has chosen as input.
:param old_letters_guessed: the letters the user already tried to guess.
:return boolean'''
def check_valid_input(letter_guessed, old_letters_guessed):
    # If the input is longer than a single letter and is not from the alphabet.
    if (len(letter_guessed) > 1) and (not letter_guessed.isalpha()):
        return False
    # If the input is longer than a single letter
    elif len(letter_guessed) > 1:
        return False
    # If the input is not from the alphabet.
    elif not letter_guessed.isalpha():
        return False
    return True


''' This function checks if the user has guessed the current input before.
:param letter_guessed: the letter the user has chosen as input.
:param old_letters: the letters the user already tried to guess
:return boolean'''
def try_update_letter_guessed(letter_guessed, old_letters):
    if not check_valid_input(letter_guessed, old_letters):
        old_letters.sort()
        print("X")
        print_guessed_list = " -> ".join(old_letters)
        if len(old_letters) > 0:
            print(print_guessed_list)
        return False

    # If user tried to guess a letter he has guessed before.
    elif letter_guessed in old_letters:
        old_letters.sort()
        print("X")
        print_guessed_list = " -> ".join(old_letters)
        print(print_guessed_list)
        return False

    else:
        global old_letters_guessed
        old_letters_guessed = old_letters + [letter_guessed]
        return True

''' This function checks how many letters the user guessed correctly and returns
the current state of how much of the word is revealed.
:param secret_word: the word the user needs to guess.
:param old_letters_guessed: the letters the user already tried to guess.
:return str that represents how much of the secret word was successfully guessed.'''
def show_hidden_word(secret_word, old_letters_guessed):
    current_state = "_ " * (len(secret_word) - 1) + "_"
    current_state = list(current_state.split())
    for letter in old_letters_guessed:
        for index in range(len(secret_word)):
            if secret_word[index] == letter:
                current_state[index] = letter
    current_state = " ".join(current_state)
    return current_state

''' This function checks if the user has already guessed the secret word.
:param secret_word: the word the user needs to guess.
:param old_letters_guessed: the letters the user already tried to guess.
:return boolean: True if the user guessed the word, False if not.'''
def check_win(secret_word, old_letters_guessed):
    current_state = show_hidden_word(secret_word, old_letters_guessed)
    # Clear spaces so that there will be only guessed letters and "_".
    current_state = current_state.replace(" ","")
    # If there are still letters missing.
    if "_" in current_state:
        return False
    else:
        return True

''' This function counts how many different words there are in a file and finds
a word in a file according to a given index.
:param file_path: a path to a file of words.
:param index: the index of a word in the file.
:return tuple: (num of different words in the file, the word in the given index).'''
def choose_word(file_path, index):
    try:
        words_file = open(file_path, 'r')
    except OSError:
        file_path = input("File_path not valid, please enter a new file path: ")
        index = choose_index()
        return choose_word(file_path, index)


    words = words_file.read()
    words = words.split(" ")
    not_duplicate_words = []
    count_different_words = 0
    for word in words:
        if word not in not_duplicate_words:
            not_duplicate_words.append(word)
    count_different_words = len(not_duplicate_words)
    indexed_word = words[(index - 1) % len(words)]

    return (count_different_words, indexed_word)

''' This function checks if the user entered a valid index
:param index: the index the user chose.
:return valid_index: a valid index the user chose.'''
def choose_index():
    try:
        valid_index = int(input("Please choose an index for a word to guess: "))
        return valid_index
    except ValueError:
        return choose_index()


def main():
    # Opening screen.
    print_opening_screen(HANGMAN_ASCII_ART)
    file_path = input("Welcome, please enter a path to txt file: ")
    index = choose_index()
    tuple_word_to_guess = choose_word(file_path, index)
    secret_word = tuple_word_to_guess[1]
    print("\n")
    print("Let's start!")
    print_hangman(0)
    initial_state = "_ " * (len(secret_word) - 1) + "_"
    print(initial_state)
    old_letters_guessed = []
    num_of_tries = 0
    while not check_win(secret_word, old_letters_guessed):
        guessed_letter = input("Please guess a letter: ")
        guessed_letter = guessed_letter.lower()

        # If the input is not valid, try and guess again.
        if not try_update_letter_guessed(guessed_letter, old_letters_guessed):
            #if guessed_letter in old_letters:
            continue
        old_letters_guessed = old_letters_guessed + [guessed_letter]
        if guessed_letter in secret_word:
            # If the user guessed a letter that's in the word,
            # print current state of the secret word.
            print(show_hidden_word(secret_word, old_letters_guessed))
        else:
            print(":(")
            num_of_tries = num_of_tries + 1
            print_hangman(num_of_tries)
            print(show_hidden_word(secret_word, old_letters_guessed))
            if num_of_tries == MAX_TRIES:
                print("LOSE")
                return

    print("WIN")



if __name__ == "__main__":
    main()