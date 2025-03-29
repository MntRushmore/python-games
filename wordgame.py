import random

word_bank = ['rizz', 'ohio', 'sigma', 'tiktok', 'skibidi', 'sussy', 'sus', 'drip', 'lit', 'vibe', 'slay', 'bussin', 'goofy', 'yeet', 'cap', 'no cap']
word = random.choice(word_bank)
guessedWord = ['_'] * len(word)
attempts = 10
while attempts > 0:
    guess = input('Guess a letter: ')
    if len(guess) != 1 or not guess.isalpha():
        print('Please enter a single letter.')
        continue
    if guess in word:
        for i in range(len(word)):
            if word[i] == guess:
                guessedWord[i] = guess
        print('Correct!')
    else:
        attempts -= 1
        print('Incorrect! Attempts left: ' + str(attempts))
    if '_' not in guessedWord:
        print('Congratulations! You guessed the word: ' + word)
        break
    if attempts == 0:
        print('Game Over! The word was: ' + word)
print('\nCurrent word: ' + ' '.join(guessedWord))
print('Thanks for playing!')
# wordgame.py
# This is a simple word guessing game where the player has to guess a word letter by letter.
# The player has a limited number of attempts to guess the word.
# The game will provide feedback on whether the guessed letter is correct or not.
# The game will also display the current state of the word after each guess.
# The game ends when the player either guesses the word or runs out of attempts.
# The player can only guess one letter at a time.
# The game will randomly select a word from a predefined word bank.
# The word bank contains words that are commonly used in internet slang and memes.
# The game will display the current state of the word with underscores for unguessed letters.
# The game will also display the number of attempts left after each incorrect guess.
# The game will display a message when the player wins or loses.
# The game will also display the correct word when the player loses.
# The game will ask the player to guess a letter and will validate the input.
# The game will continue until the player either guesses the word or runs out of attempts.
# The game will also display a message when the player wins or loses.