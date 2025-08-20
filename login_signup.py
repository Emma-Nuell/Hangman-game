import json
import os
import random
import string

# Global variable to store current user data
current_user = None

def load_users():
    """Load user data from JSON file"""
    if os.path.exists('users.json'):
        try:
            with open('users.json', 'r') as file:
                data = json.load(file)
                # Validate data structure
                if not isinstance(data, dict):
                    print("Warning: Invalid user data format. Creating new file.")
                    return {}
                
                # Validate each user entry
                for username, user_data in data.items():
                    if not isinstance(user_data, dict):
                        print(f"Warning: Invalid data for user {username}. Skipping.")
                        continue
                    
                    # Ensure required fields exist and are correct types
                    required_fields = {'password': str, 'wins': int, 'losses': int, 'plays': int}
                    for field, expected_type in required_fields.items():
                        if field not in user_data:
                            user_data[field] = 0 if expected_type == int else ""
                        elif not isinstance(user_data[field], expected_type):
                            try:
                                user_data[field] = expected_type(user_data[field])
                            except (ValueError, TypeError):
                                user_data[field] = 0 if expected_type == int else ""
                
                return data
        except (json.JSONDecodeError, FileNotFoundError, TypeError, KeyError) as e:
            print(f"Error loading user data: {e}. Creating new file.")
            return {}
    return {}



# def generate_password(length=8):
#     """Generate a random password"""
#     characters = string.ascii_letters + string.digits
#     return ''.join(random.choice(characters) for _ in range(length))

def save_users(users_data) -> bool:
    """Save user data to JSON file"""
    try:
        with open('users.json', 'w') as file:
            json.dump(users_data, file, indent=2)
    except (IOError, TypeError) as e:
        print(f"Error saving user data: {e}")
        return False
    return True

def generate_password(length=8) -> str:
    """Generate a random password with at least 1 uppercase letter and 1 number"""
    
    # Ensure minimum requirements
    if length < 8:
        length = 8
    
    # Generate password with guaranteed requirements
    password = []
    
    # Add at least 1 uppercase letter
    password.append(random.choice(string.ascii_uppercase))
    
    # Add at least 1 number
    password.append(random.choice(string.digits))
    
    # Fill the rest with random characters (lowercase, uppercase, digits)
    characters = string.ascii_letters + string.digits
    for _ in range(length - 2):
        password.append(random.choice(characters))
    
    # Shuffle the password to randomize positions
    random.shuffle(password)
    
    return ''.join(password)


def register() -> bool:
    """Register a new user"""
    global current_user
    print("\n==== REGISTRATION ====")
    
    while True:
        try:
            username: str = input("Enter username (or 'quit'/'exit' to return): ").strip()
            
            if username.lower() in ['quit', 'exit']:
                return False
            
            if not username:
                print("Username cannot be empty. Please try again.")
                continue
                
            # Load existing users
            users = load_users()
            
            if username in users:
                print("Username already exists. Please choose a different username.")
                continue
                
            # Password selection
            print("\nPassword Options:")
            print("1. Auto-generate password")
            print("2. Enter password manually (minimum 8 characters, 1 uppercase, 1 number)")
            
            while True:
                try:
                    choice: str = input("Choose option (1 or 2): ").strip()
                    
                    if choice == '1':
                        password: str = generate_password()
                        print(f"Your auto-generated password is: {password}")
                        print("Please save this password somewhere safe!")
                        break
                    elif choice == '2':
                        while True:
                            password = input("Enter your password (min 8 chars, 1 uppercase, 1 number): ").strip()
                            if not password:
                                print("Password cannot be empty. Please try again.")
                                continue
                            elif len(password) < 8:
                                print("⚠️ Password must be at least 8 characters long! Please try again.")
                                continue
                            elif not any(c.isupper() for c in password):
                                print("⚠️ Password must contain at least 1 uppercase letter! Please try again.")
                                continue
                            elif not any(c.isdigit() for c in password):
                                print("⚠️ Password must contain at least 1 number! Please try again.")
                                continue
                            else:
                                print("✅ Password accepted!")
                                break
                        break
                    else:
                        print("Invalid choice. Please enter 1 or 2.")
                except (KeyboardInterrupt, EOFError):
                    print("\nOperation cancelled.")
                    return False
            
            # Create new user record
            users[username] = {
                'password': password,
                'wins': 0,
                'losses': 0,
                'plays': 0
            }
            
            # Save to file
            if not save_users(users):
                print("Error saving user data. Please try again.")
                continue
                
            current_user = {'username': username, 'data': users[username]}
            
            print(f"\nRegistration successful! Welcome, {username}!")
            display_user_stats(username, users[username])
            return True
            
        except (KeyboardInterrupt, EOFError):
            print("\nRegistration cancelled.")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Please try again.")
            continue
        
def login() -> bool:
    """Login existing user"""
    global current_user
    print("\n==== LOGIN ====")
    
    while True:
        try:
            username: str = input("Enter username (or 'quit'/'exit' to return): ").strip()
            
            if username.lower() in ['quit', 'exit']:
                return False
            
            if not username:
                print("Username cannot be empty. Please try again.")
                continue
                
            # Load existing users
            users = load_users()
            
            if username not in users:
                print("Username not found. Please check your username or register first.")
                continue
            
            # Get password
            password: str = input("Enter password: ").strip()
            
            # Check password
            try:
                if users[username]['password'] != password:
                    print("Invalid password. Please try again.")
                    continue
            except (KeyError, TypeError):
                print("Error accessing user data. Please try again or re-register.")
                continue
            
            current_user = {'username': username, 'data': users[username]}
            
            print(f"\nLogin successful! Welcome back, {username}!")
            display_user_stats(username, users[username])
            return True
            
        except (KeyboardInterrupt, EOFError):
            print("\nLogin cancelled.")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}. Please try again.")
            continue
        
        
def display_user_stats(username, user_data) -> None:
    """Display user statistics"""
    print(f"====== Record for {username} ======")
    print(f"    SESSION WINS     : {user_data['wins']}")
    print(f"    SESSION LOSSES   : {user_data['losses']}")
    print(f"    SESSION PLAYS    : {user_data['plays']}")
    
def update_user_stats(won=False) -> bool:
    """Update user statistics after a game"""
    global current_user
    
    if current_user is None:
        return False
    
    try:
        users = load_users()
        username = current_user['username']
        
        if username not in users:
            print("Error: User not found in database.")
            return False
        
        # Update stats with type checking
        try:
            users[username]['plays'] = int(users[username].get('plays', 0)) + 1
            
            if won:
                users[username]['wins'] = int(users[username].get('wins', 0)) + 1
            else:
                users[username]['losses'] = int(users[username].get('losses', 0)) + 1
        except (ValueError, TypeError) as e:
            print(f"Error updating stats: {e}")
            return False
        
        # Save updated stats
        if not save_users(users):
            print("Error saving updated stats.")
            return False
            
        current_user['data'] = users[username]
        return True
        
    except Exception as e:
        print(f"Unexpected error updating stats: {e}")
        return False