# 🎮 Rock Paper Scissors Lizard Spock - OpenClaw Skill

An interactive OpenClaw skill for playing the classic Rock Paper Scissors Lizard Spock game (from The Big Bang Theory) with beautiful terminal UI and GUI modes!

## 🌟 Features

### Dual Play Modes
- **🖥️ Decorated Terminal**: Beautiful ASCII art with colors, animations, and emojis
- **🎨 Interactive GUI**: Click-based HTML interface with gradients and animations

### Game Features
- 📊 **Persistent Statistics**: Track all-time wins, losses, and ties
- 🏆 **Win Streak Tracking**: Monitor your best and current streaks
- 📈 **Choice Analysis**: See which moves you use most
- 🎯 **In-Game Rules**: Display rules anytime during play
- 💾 **Auto-Save Stats**: Statistics saved to `~/.rpsls_stats.json`
- 🎭 **Animated Results**: Shake animations and colorful feedback

## 🎲 Game Rules

From The Big Bang Theory - created by Sam Kass and Karen Bryla:

- 🪨 **Rock** crushes Scissors and crushes Lizard
- 📄 **Paper** covers Rock and disproves Spock
- ✂️ **Scissors** cuts Paper and decapitates Lizard
- 🦎 **Lizard** eats Paper and poisons Spock
- 🖖 **Spock** smashes Scissors and vaporizes Rock

Each choice defeats exactly 2 others and loses to exactly 2 others!

## 📦 Installation

### For ClawHub

```bash
# Install the skill
clawhub skill install rpsls-game

# Or from this directory
clawhub skill publish ./rpsls-skill
```

### Manual Installation

```bash
# Copy SKILL.md to your skills directory
cp SKILL.md ~/.openclaw/skills/rpsls-game.md

# Restart OpenClaw gateway
openclaw gateway restart
```

## 🚀 Usage

### In OpenClaw Chat

**Start a Game**:
```
"Let's play Rock Paper Scissors Lizard Spock"
"Play RPSLS in terminal mode"
"Show me the RPSLS GUI"
"Start a decorated RPSLS game"
```

**Quick Commands**:
```
"Play rock" / "Choose scissors"
"RPSLS stats" → View game statistics
"RPSLS rules" → Display game rules
"Best of 3" → Start tournament mode
```

### Terminal Mode

Claude will create a Python script with the `rich` library for beautiful terminal UI:

```bash
# Claude creates: rpsls_terminal.py
python3 rpsls_terminal.py
```

**Features**:
- ✨ Colored output with emojis
- 📊 Real-time stats display
- 🎯 In-game commands (stats, rules, quit)
- 💾 Persistent storage

### GUI Mode

Claude will create an interactive HTML artifact you can use directly in the browser:

**Features**:
- 🖱️ Click any choice to play
- 📊 Live scoreboard
- 🎭 Animated results
- 📱 Mobile-responsive
- 📋 Built-in rules

## 🎯 Example Session

```
You: "Let's play rock paper scissors lizard spock in terminal mode"

Claude: "I'll create a beautiful terminal version for you!"
[Creates rpsls_terminal.py with rich library]

"Here's your decorated RPSLS game! Run with:
 python3 rpsls_terminal.py
 
 Features:
 - Beautiful colored UI
 - Emoji icons for each choice
 - Statistics tracking
 - Win streaks
 - Type 'stats' anytime for your record
 - Type 'rules' to see game rules"

You: [Runs the game]

╔═══════════════════════════════════════════════════╗
║  🎮 ROCK PAPER SCISSORS LIZARD SPOCK 🎮          ║
║                                                   ║
║  🪨 Rock    📄 Paper    ✂️ Scissors              ║
║  🦎 Lizard  🖖 Spock                             ║
║                                                   ║
║  "A game of strategic brilliance!" - Sheldon     ║
╚═══════════════════════════════════════════════════╝

Your move: 🪨 rock | 📄 paper | ✂️ scissors | 🦎 lizard | 🖖 spock
Choose your weapon: rock

Choices:
┌────────────────────┬─────┬────────────────────┐
│ 🪨 Rock            │ VS  │ ✂️ Scissors        │
└────────────────────┴─────┴────────────────────┘

╔══════════════════════════════════════════════╗
║ 🎉 YOU WIN! 🎉                               ║
║ 🪨 Rock crushes ✂️ Scissors!                 ║
╚══════════════════════════════════════════════╝

Session Score: Wins: 1 | Losses: 0 | Ties: 0
```

## 📊 Statistics Tracking

The terminal version saves statistics to `~/.rpsls_stats.json`:

```json
{
  "total_games": 47,
  "wins": 18,
  "losses": 21,
  "ties": 8,
  "choice_freq": {
    "rock": 15,
    "paper": 9,
    "scissors": 8,
    "lizard": 7,
    "spock": 8
  },
  "best_streak": 5,
  "current_streak": 2
}
```

View stats anytime:
- In-game: Type `stats`
- Ask Claude: "Show my RPSLS stats"

## 🎨 Screenshots

### Terminal Mode
```
╔═══════════════════════════════════════════════════╗
║  🎮 ROCK PAPER SCISSORS LIZARD SPOCK 🎮          ║
╚═══════════════════════════════════════════════════╝

📊 Game Statistics
All-Time Record:
  Total Games: 47
  Wins: 18 (38.3%)
  Losses: 21 (44.7%)
  Ties: 8 (17.0%)
  
Best Streak: 5 wins
Current Streak: 2 wins
```

### GUI Mode
- Beautiful gradient background (purple to blue)
- Large emoji buttons for each choice
- Animated result display
- Live scoreboard (wins/losses/ties)
- Responsive design works on mobile

## 🛠️ Requirements

### For Terminal Mode
- Python 3.7+
- `rich` library: `pip install rich --break-system-packages`

### For GUI Mode
- No requirements! Just open the HTML artifact

## 🎮 Advanced Features

### Tournament Mode
Ask for "best of 3" or "best of 5" to play tournament-style matches.

### Adaptive AI (Future)
Coming soon: An AI that learns from your patterns and adapts its strategy!

### Multiplayer (Future)
Coming soon: Play against friends instead of just the computer!

## 🤝 Contributing

Want to enhance the skill? Here are some ideas:
- Add more game modes
- Create different AI difficulty levels
- Add sound effects
- Create custom themes
- Add achievement system

## 📝 License

MIT License - Feel free to use, modify, and share!

## 🌟 Credits

- **Game Concept**: Sam Kass and Karen Bryla
- **Popularized By**: The Big Bang Theory (Sheldon Cooper)
- **OpenClaw Skill**: AM (akm626)
- **Inspiration**: Original rpsls.py provided by user

## 🔗 Links

- **OpenClaw**: https://openclaw.ai
- **ClawHub**: https://clawhub.ai
- **Original Game Info**: https://www.samkass.com/theories/RPSSL.html

---

**"In a world where scissors can decapitate a lizard and a lizard can poison Spock, anything is possible!"** - Sheldon Cooper

🎮 Have fun playing! May the odds be ever in your favor! 🖖
