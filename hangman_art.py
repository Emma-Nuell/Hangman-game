# hangman_art.py
# ASCII art and emojis for the hangman game

# Hangman stages with emojis (from 0 wrong guesses to 6 wrong guesses)
hangman_stages: list[str] = [
    """
     ╔═══════╗
     ║       
     ║        
     ║        
     ║        
     ║        
    ═╩═══════
    """,
    """
     ╔═══════╗
     ║       │
     ║       😐
     ║        
     ║        
     ║        
    ═╩═══════
    """,
    """
     ╔═══════╗
     ║       │
     ║       😯
     ║       │
     ║        
     ║        
    ═╩═══════
    """,
    """
     ╔═══════╗
     ║       │
     ║       😧
     ║      /│
     ║        
     ║        
    ═╩═══════
    """,
    """
     ╔═══════╗
     ║       │
     ║       😰
     ║      /│\\
     ║        
     ║        
    ═╩═══════
    """,
    """
     ╔═══════╗
     ║       │
     ║       😩
     ║      /│\\
     ║      / 
     ║        
    ═╩═══════
    """,
    """
     ╔═══════╗
     ║       │
     ║       💀
     ║      /│\\
     ║      / \\
     ║        
    ═╩═══════
    """
]
# Welcome banner with emojis
welcome_banner = """
🎯 ═══════════════════════════════════════════════════════════ 🎯
    🎪 WELCOME TO THE ULTIMATE HANGMAN CHALLENGE! 🎪
🎯 ═══════════════════════════════════════════════════════════ 🎯
"""

# Difficulty selection banner
difficulty_banner = """
🎮 ═══════════════════════════════════════════════════════════ 🎮
                    SELECT YOUR DIFFICULTY LEVEL
🎮 ═══════════════════════════════════════════════════════════ 🎮

1. 🌱 BEGINNER     → 5-7 letters, 3 hints, 6 attempts
2. 🔥 INTERMEDIATE → 10-12 letters, 3 hints, 6 attempts  
3. 💀 PROFESSIONAL → 13-14 letters, 3 hints, 6 attempts
"""

# Game over messages with emojis
win_messages: dict[str, str] = {
    'beginner': """
🎉 ════════════════════════════════════════ 🎉
    🌟 CONGRATULATIONS BEGINNER! 🌟
    🏆 You've mastered the basics! 🏆
🎉 ════════════════════════════════════════ 🎉
    """,
    'intermediate': """
🎉 ════════════════════════════════════════ 🎉
    🔥 AMAZING INTERMEDIATE PLAYER! 🔥
    🏆 You're getting really good! 🏆
🎉 ════════════════════════════════════════ 🎉
    """,
    'professional': """
🎉 ════════════════════════════════════════ 🎉
    👑 LEGENDARY PROFESSIONAL! 👑
    🏆 YOU ARE A HANGMAN MASTER! 🏆
🎉 ════════════════════════════════════════ 🎉
    """
}

lose_message = """
💀 ════════════════════════════════════════ 💀
    😵 GAME OVER! YOU LOST! 😵
       Better luck next time! 
💀 ════════════════════════════════════════ 💀
"""

# Status emojis
status_emojis: dict[str, str] = {
    'correct': '✅',
    'incorrect': '⚠️',
    'already_guessed': '🔤',
    'heart': '❤',
    'broken_heart': '💔',
    'letters': '🔤',
    'target': '🎯',
    'thinking': '🤔'
}

# Level emojis
level_emojis: dict[str, str] = {
    'beginner': '🌱',
    'intermediate': '🔥',
    'professional': '💀'
}