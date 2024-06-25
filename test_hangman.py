import unittest
from Hangman import get_random_word_from_wordlist,get_some_letters,draw_hangman,start_hangman_game,retry
from unittest.mock import patch
import random

class TestHangman(unittest.TestCase):
    wordlist = ['testword', 'example', 'hangman', 'python', 'unittest']
    
    @patch('Hangman.random.choice')
    # @patch('Hangman.get_random_word_from_wordlist')
    def test_get_random_word(self,mock_random_choice):
        mock_random_choice.return_value = 'python'
        word = get_random_word_from_wordlist()
        self.assertEqual(word, 'python')

class TestGetSomeLetters(unittest.TestCase):

    def test_some_letters6(self):
         word = "python"
         result = get_some_letters(word)
         self.assertEqual(result, "______")
    
    def test_some_letters7(self):
        word = "hangman"
        result = get_some_letters(word)
        self.assertEqual(result,"_______")

    def test_some_letters_empty(self):
        word = ""
        result = get_some_letters(word)
        self.assertEqual(result, "")

    def test_some_letters_single_letter(self):
        word = "a"
        result = get_some_letters(word)
        self.assertEqual(result,"_")

class TestDrawHangman(unittest.TestCase):
    def test_chance6(self):
        with patch('builtins.print') as mock_print:
            draw_hangman(6)
        self.assertIn(r"""+------+
|      |
|
|
|
|
======
========""",mock_print.call_args.args[0])
        
    def test_chance0(self):
        with patch('builtins.print') as mock_print:
            draw_hangman(0)
        self.assertIn(r"""+------+
|      |
|      0
|     /|\\
|     / \\
|
======
========""",mock_print.call_args.args[0])

class TestHangmanGame(unittest.TestCase):
    @patch('Hangman.get_random_word_from_wordlist')
    @patch('Hangman.get_some_letters')
    @patch('Hangman.draw_hangman')
    @patch('Hangman.input')
    @patch('Hangman.retry')
    def test_win_game(self, mock_retry, mock_input, mock_draw_hangman, mock_get_some_letters, mock_get_random_word_from_wordlist):
    # Mock retry to start the game
        mock_retry.return_value = True
        # Mock the random word and its initial hidden form
        mock_get_random_word_from_wordlist.return_value = 'python'
        mock_get_some_letters.return_value = '______'
        
        # Allows user inputs to guess the word correctly
        mock_input.side_effect = ['p', 'y', 't', 'h', 'o', 'n']
        
        with patch('builtins.print') as mocked_print:
            start_hangman_game()
            #To check if the game prints the winning message
            mocked_print.assert_any_call("*** Guess the word ***")
            mocked_print.assert_any_call("\nYou Won! The word was: python")

    @patch('Hangman.get_random_word_from_wordlist')
    @patch('Hangman.get_some_letters')
    @patch('Hangman.draw_hangman')
    @patch('Hangman.input')
    @patch('Hangman.retry')
    def test_lose_game(self, mock_retry, mock_input, mock_draw_hangman, mock_get_some_letters, mock_get_random_word_from_wordlist):
        # Mocking retry to return True so the game starts
        mock_retry.return_value = True
        # Mocking the random word and its initial hidden form
        mock_get_random_word_from_wordlist.return_value = 'java'
        mock_get_some_letters.return_value = '____'
        
        # Allows user inputs to guess incorrectly and exhaust all chances
        mock_input.side_effect = ['x', 'y', 'z', 'w', 'q', 'e', 'r']
        
        with patch('builtins.print') as mocked_print:
            start_hangman_game()
            mocked_print.assert_any_call("*** Guess the word ***")
            mocked_print.assert_any_call("Sorry! You Lost!, the word was: java")
            mocked_print.assert_any_call("Better luck next time")


    @patch('Hangman.get_random_word_from_wordlist')
    @patch('Hangman.get_some_letters')
    @patch('Hangman.draw_hangman')
    @patch('Hangman.input')
    @patch('Hangman.retry')
    def test_invalid_input(self, mock_retry, mock_input, mock_draw_hangman, mock_get_some_letters, mock_get_random_word_from_wordlist):
        # Mocking retry to return True so the game starts
        mock_retry.return_value = True
        # Mocking the random word and its initial hidden form
        mock_get_random_word_from_wordlist.return_value = 'ruby'
        mock_get_some_letters.return_value = '____'
        
        mock_input.side_effect = ['1', '!', 'r', 'u', 'b', 'y']
        
        with patch('builtins.print') as mocked_print:
            start_hangman_game()
            
            # Check the invalid inputs prompt
            mocked_print.assert_any_call("Please enter a single alphabet only")
            # Check the game prompt after valid inputs
            mocked_print.assert_any_call("*** Guess the word ***")

class TestRetryFunction(unittest.TestCase):
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_retry_yes(self, mock_print, mock_input):
        mock_input.side_effect = ['yes']
        
        result = retry()
        
        # Check if the function returns True
        self.assertTrue(result)
        
        mock_print.assert_any_call("**** Welcome to the Hangman Game ****")
        mock_print.assert_any_call("Do you wanna play hangman again? (yes/no): ")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_retry_no(self, mock_print, mock_input):
        #allows user to input "no"
        mock_input.side_effect = ['no']
        
        result = retry()
        
        # Check if the function returns None 
        self.assertIsNone(result)
        
        # Check if the correct messages were printed
        mock_print.assert_any_call("**** Welcome to the Hangman Game ****")
        mock_print.assert_any_call("Exiting the game...")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_retry_invalid_then_yes(self, mock_print, mock_input):

        mock_input.side_effect = ['maybe', 'yes']
        
        result = retry()
        
        # Check if the function returns True after valid input
        self.assertTrue(result)
    
        mock_print.assert_any_call("**** Welcome to the Hangman Game ****")
        mock_print.assert_any_call("Please enter a valid choice.")
        mock_print.assert_any_call("Do you wanna play hangman again? (yes/no): ")

    @patch('builtins.input')
    @patch('builtins.print')
    def test_retry_invalid_then_no(self, mock_print, mock_input):
        mock_input.side_effect = ['maybe', 'no']
        
        result = retry()
        
        # Check if the function returns None after valid input
        self.assertIsNone(result)
        
        # To check the correct messages are printed
        mock_print.assert_any_call("**** Welcome to the Hangman Game ****")
        mock_print.assert_any_call("Please enter a valid choice.")
        mock_print.assert_any_call("Exiting the game...")

    

if __name__ == '__main__':
    unittest.main()
