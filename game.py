import random
import os
from hangman_art import (hangman_stages, welcome_banner, difficulty_banner, 
                        win_messages, lose_message, status_emojis, level_emojis)
from retrieve_word_fn import retrieve_word
import login_signup


def clear_screen () -> None:
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')


class HangmanGame:
    def __init__(self) -> None:
        # Word lists for different difficulty levels
        self.word_lists: dict[str, list[int]] = {
            'beginner': [
                5, 6,7
            ],
            'intermediate': [
                10, 11, 12
            ],
            'professional': [
                13, 14
            ]
        }
        
        # Difficulty stage settings
        self.difficulty_settings = {
            'beginner': {'max_attempts': 6, 'hints': (3, 3)},
            'intermediate': {'max_attempts': 5, 'hints': (2, 2)},
            'professional': {'max_attempts': 4, 'hints': (0, 1)}
        }
        
        # Game state variables
        self.difficulty: str = ""
        self.chosen_word: str = ""
        self.word_length: int = 0
        self.display: list[str] = []
        self.wrong_guesses: int = 0
        self.max_wrong_guesses = 6
        self.guessed_letters: list[str] = []
        self.correct_guesses: list[str] = []
        self.incorrect_guesses: list[str] = []
        self.game_over: bool = False
        self.last_guess: str = ""
        self.last_guess_status: str = ""
        self.quit_game:bool  = False  # New variable to track if user wants to quit

    def display_user_stats(self) -> None:
        """Display current user's statistics"""
        if login_signup.current_user and login_signup.current_user.get('data'):
            user_data = login_signup.current_user['data']
            plays = user_data.get('plays', 0)
            wins = user_data.get('wins', 0)
            losses = user_data.get('losses', 0)
            
            win_rate: float = (wins / plays * 100) if plays > 0 else 0
            
            print(f"👤 Player: {login_signup.current_user['username']}")
            print(f"🎮 Games Played: {plays} | 🏆 Wins: {wins} | 💀 Losses: {losses}")
            print(f"📊 Win Rate: {win_rate:.1f}%")
            print("═" * 60)
    
    def select_difficulty(self) -> None:
        """Let player select difficulty level"""
        clear_screen()
        print(difficulty_banner)
        
        # Show user stats if logged in
        if login_signup.current_user:
            self.display_user_stats()
            print()
        
        while True:
            choice: str = input("Enter your choice (1-3): ").strip()
            
            if choice == '1':
                self.difficulty = 'beginner'
                break
            elif choice == '2':
                self.difficulty = 'intermediate'
                break
            elif choice == '3':
                self.difficulty = 'professional'
                break
            else:
                print("⚠️  Please enter 1, 2, or 3!")
        
        # Set max attempts based on difficulty
        self.max_wrong_guesses:int = self.difficulty_settings[self.difficulty]['max_attempts']
    
    def choose_word(self) -> None:
        """Randomly choose a word from the selected difficulty list"""
        word_num: list[int] = self.word_lists[self.difficulty]
        self.chosen_word = retrieve_word(random.choice(word_num))
        self.word_length = len(self.chosen_word)
        
        # Create display words with blanks
        self.display = ["_" for letter in self.chosen_word]
        
        # Add hints based on difficulty level
        self.add_hints()
    
    def add_hints(self) -> None:
        """Add initial visible letters based on difficulty"""
        min_hints, max_hints = self.difficulty_settings[self.difficulty]['hints']
        num_hints: int = random.randint(min_hints, max_hints)
        
        # Get random positions for hints
        positions: list[int] = random.sample(range(self.word_length), num_hints)
        
        for pos in positions:
            letter: str = self.chosen_word[pos]
            self.display[pos] = letter
            if letter not in self.correct_guesses:
                self.correct_guesses.append(letter)
    
    def display_hearts(self) -> str:
        """Display remaining attempts as hearts"""
        attempts_left = self.max_wrong_guesses - self.wrong_guesses
        hearts = status_emojis['heart'] * attempts_left
        return f"Attempts Left: {attempts_left} {hearts}"
    
    def display_game_state(self) -> None:
        """Display current game state with emojis"""
        clear_screen()
        print(welcome_banner)
        
        # Show user info if logged in
        if login_signup.current_user:
            print(f"👤 Playing as: {login_signup.current_user['username']}")
        
        print(f"{level_emojis[self.difficulty]} DIFFICULTY: {self.difficulty.upper()}")
        print("═" * 60)
        
        # Display attempts
        print(self.display_hearts())
        print()
        
        # Display previous guess status
        if self.last_guess:
            if self.last_guess_status == 'correct':
                print(f"{status_emojis['correct']} Previous guess '{self.last_guess.upper()}' is correct!")
            elif self.last_guess_status == 'incorrect':
                print(f"{status_emojis['incorrect']} Previous guess '{self.last_guess.upper()}' is incorrect")
            elif self.last_guess_status == 'already_guessed':
                print(f"{status_emojis['already_guessed']} Previous guess '{self.last_guess.upper()}' has been entered")
        
        # Display correct guesses
        if self.correct_guesses:
            correct_display: str = " ".join([letter.upper() for letter in sorted(self.correct_guesses)])
            print(f"{status_emojis['correct']} Previous guesses correct: [ {correct_display} ]")
        
        # Display incorrect guesses
        if self.incorrect_guesses:
            incorrect_display: str = " ".join([letter.upper() for letter in sorted(self.incorrect_guesses)])
            print(f"{status_emojis['incorrect']} Previous guesses incorrect: [ {incorrect_display} ]")
        
        print("\nGallows:")
        print(hangman_stages[self.wrong_guesses])
        
        # Display word
        word_display: str = " ".join([letter.upper() for letter in self.display])
        print(f"{status_emojis['target']} Word to guess: {word_display}")
        print("═" * 60)
    
    def get_user_guess(self) -> str:
        """Get and validate user's letter guess"""
        while True:
            guess: str = input(f"{status_emojis['thinking']} Guess a letter (or type 'quit'/'exit' to quit): ").lower().strip()
            
            # Check if user wants to quit
            if guess in ['quit', 'exit']:
                return guess
            
            # Check if input is a single letter
            if len(guess) != 1:
                print("⚠️  Please enter only one letter!")
                continue
                
            # Check if input is a letter
            if not guess.isalpha():
                print("⚠️  Please enter a valid letter!")
                continue
                
            return guess
    
    def process_guess(self, guess) -> None:
        """Process the user's guess and update game state"""
        # Handle quit commands
        if guess in ['quit', 'exit']:
            self.quit_game = True
            return
            
        self.last_guess = guess
        
        # Check if already guessed
        if guess in self.guessed_letters:
            self.last_guess_status = 'already_guessed'
            return
        
        self.guessed_letters.append(guess)
        
        # Check if the guess reveals any new letters
        new_letters_revealed = False
        if guess in self.chosen_word:
            for i in range(self.word_length):
                if self.chosen_word[i] == guess and self.display[i] == "_":
                    self.display[i] = guess
                    new_letters_revealed = True
        
        if new_letters_revealed:
            # Correct guess - revealed new letter(s)
            self.last_guess_status = 'correct'
            self.correct_guesses.append(guess)
        else:
            # Wrong guess - either not in word or already revealed in hints
            self.last_guess_status = 'incorrect'
            self.incorrect_guesses.append(guess)
            self.wrong_guesses += 1
    
    def update_stats(self, won) -> None:
        """Update user statistics after game ends"""
        if login_signup.current_user:
            success: bool = login_signup.update_user_stats(won=won)
            if success:
                print(f"📊 Stats updated successfully!")
            else:
                print(f"⚠️  Failed to update stats.")
        else:
            print("🔒 Login to save your stats!")
    
    def check_game_over(self) -> None:
        """Check if the game has ended"""
        # Check if player won (no more blanks)
        if "_" not in self.display:
            clear_screen()
            print(win_messages[self.difficulty])
            print(f"🎯 The word was: {self.chosen_word.upper()}")
            print(f"📝 Word: {' '.join([letter.upper() for letter in self.display])}")
            print(f"🎪 You completed it in {len(self.guessed_letters)} guesses!")
            
            # Update stats for win
            self.update_stats(won=True)
            
            self.game_over = True
            
        # Check if player lost (too many wrong guesses)
        elif self.wrong_guesses >= self.max_wrong_guesses:
            clear_screen()
            print(lose_message)
            print("Final Gallows:")
            print(hangman_stages[self.wrong_guesses])
            print(f"🎯 The word was: {self.chosen_word.upper()}")
            
            # Update stats for loss
            self.update_stats(won=False)
            
            self.game_over = True
    
    def show_final_stats(self) -> None:
        """Show updated user statistics after game"""
        if login_signup.current_user and login_signup.current_user.get('data'):
            print("\n" + "═" * 60)
            print("📊 YOUR UPDATED STATISTICS:")
            self.display_user_stats()
    
    def play_again(self) -> bool:
        """Ask if player wants to play again"""
        # Show updated stats
        self.show_final_stats()
        
        while True:
            choice: str = input("\n🎮 Do you want to play again? (y/n): ").lower().strip()
            if choice in ['y', 'yes']:
                return True
            elif choice in ['n', 'no']:
                return False
            else:
                print("⚠️  Please enter 'y' for yes or 'n' for no.")
    
    def reset_game(self):
        """Reset game variables for a new game"""
        self.chosen_word = ""
        self.word_length = 0
        self.display = []
        self.wrong_guesses = 0
        self.guessed_letters = []
        self.correct_guesses = []
        self.incorrect_guesses = []
        self.game_over = False
        self.last_guess = ""
        self.last_guess_status = ""
        self.quit_game = False  # Reset quit flag
    
    def handle_quit(self) -> None:
        """Handle the quit command gracefully"""
        clear_screen()
        print("🚪 Quitting the game...")
        
        if login_signup.current_user:
            print(f"👋 Goodbye, {login_signup.current_user['username']}!")
            print("📊 Your stats have been saved!")
        else:
            print("👋 Thanks for playing the Ultimate Hangman Challenge!")
            print("🔒 Create an account next time to track your progress!")
        
        print("🎪 See you next time, champion!")
    
    def run(self) -> None:
        """Main game loop"""
        clear_screen()
        print(welcome_banner)
        
        # Check if user is logged in
        if login_signup.current_user:
            print(f"🎪 Welcome back, {login_signup.current_user['username']}! 🎪")
            print("🏆 Your progress will be tracked!")
        else:
            print("🎪 Welcome to the Ultimate Hangman Challenge! 🎪")
            print("🔒 Login to track your progress and statistics!")
        
        input("Press Enter to start your adventure...")
        
        while True:
            # Select difficulty
            self.select_difficulty()
            
            # Start new game
            self.choose_word()
            
            print(f"\n🎯 Starting {self.difficulty.upper()} level!")
            print(f"💡 Word length: {self.word_length} letters")
            print(f"💖 You have {self.max_wrong_guesses} attempts")
            print("💡 Tip: Type 'quit' or 'exit' anytime to quit the game")
            input("Press Enter to begin...")
            
            # Game loop
            while not self.game_over and not self.quit_game:
                self.display_game_state()
                guess: str = self.get_user_guess()
                self.process_guess(guess)
                
                # Check if user wants to quit
                if self.quit_game:
                    break
                    
                self.check_game_over()
            
            # Handle quit during game
            if self.quit_game:
                self.handle_quit()
                break
            
            # Ask to play again
            if not self.play_again():
                if login_signup.current_user:
                    print(f"🎪 Thanks for playing, {login_signup.current_user['username']}!")
                    print("📊 Your stats have been saved!")
                else:
                    print("🎪 Thanks for playing the Ultimate Hangman Challenge!")
                    print("🔒 Create an account to track your progress!")
                print("👋 See you next time, champion!")
                break
            
            # Reset for new game
            self.reset_game()