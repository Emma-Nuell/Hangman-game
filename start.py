from game import HangmanGame
from login_signup import login, register

name = None

def welcome_interface() -> None:
    """
    Welcome interface for the user
    """
    print("""
        ==================================
          Welcome to the Hangman game 🎮
        ==================================
          """)
    
    print("Enter ('quit/'Exit') to quit the current operation")
    global name
    name = input("Enter your name:\n").title()
    if name.lower() not in ['quit', 'exit']:
        print(f"====== Welcome {name} ======")
    else:
        print("Goodbye!")
        # Exit the terminal
        exit()

def main_game() -> None:
    """
    Main game function to handle game logic
    """
    while True:
        try:
            print("Select an option:")
            print("1. Quick Game")
            print("2. Login")
            print("3. Register")
            print("4. Quit")
            choice: str = input("Enter your choice (1-4):\n")
            if choice == '1':
                game = HangmanGame()
                game.run()
            elif choice == '2':
                if login():
                    game = HangmanGame()
                    game.run()
                else:
                    return
            elif choice == '3':
                if register():
                        game = HangmanGame()
                        game.run()
                else:
                    return
                # Logic for registration
            elif choice == '4':
                print(f"Good bye! {name}")
                exit()
            else:
                print("Invalid choice. Please select a valid option (1-4).")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 4.")
            continue

