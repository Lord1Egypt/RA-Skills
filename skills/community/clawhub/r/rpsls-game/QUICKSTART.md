# 🚀 RPSLS Skill - Quick Start Guide

Get playing Rock Paper Scissors Lizard Spock in 60 seconds!

## ⚡ Fastest Way to Play

### Option 1: Ask Claude (Easiest!)

Just say:
```
"Let's play rock paper scissors lizard spock"
```

Claude will create the game for you instantly!

### Option 2: Install the Skill

```bash
# Install from ClawHub
clawhub skill install rpsls-game

# Or copy manually
cp SKILL.md ~/.openclaw/skills/rpsls-game.md
openclaw gateway restart
```

## 🎮 Choose Your Mode

### Terminal Mode (Recommended)
```
"Play RPSLS in terminal mode"
```

**You get**:
- Beautiful colored terminal UI
- Persistent statistics
- Win streak tracking
- In-game rules and stats

**To play**:
```bash
python3 rpsls_terminal.py
```

### GUI Mode (Visual)
```
"Show me the RPSLS GUI"
```

**You get**:
- Click-to-play interface
- Gradient design
- Animated results
- Real-time scoreboard

**To play**: 
Just click the choices in the artifact!

## 🎯 Making Moves

### Terminal Commands
```
rock / r
paper / p
scissors / s
lizard / l
spock / sp

stats       → View statistics
rules       → Show game rules
q / quit    → Exit game
```

### GUI Commands
Just **click** any choice button:
- 🪨 Rock
- 📄 Paper
- ✂️ Scissors
- 🦎 Lizard
- 🖖 Spock

## 📊 Viewing Stats

### In Terminal Game
Type `stats` during play

### Ask Claude
```
"Show my RPSLS stats"
"What's my win rate?"
"How many games have I played?"
```

## 🎲 Game Cheat Sheet

**What Beats What**:
```
🪨 Rock      → ✂️ Scissors, 🦎 Lizard
📄 Paper     → 🪨 Rock, 🖖 Spock
✂️ Scissors  → 📄 Paper, 🦎 Lizard
🦎 Lizard    → 📄 Paper, 🖖 Spock
🖖 Spock     → ✂️ Scissors, 🪨 Rock
```

## 🏆 Pro Tips

1. **Mix it up**: Don't get predictable!
2. **Use all 5**: Lizard and Spock add strategy
3. **Watch patterns**: Computer is random (no patterns)
4. **Check stats**: See which moves you overuse
5. **Have fun**: It's a game of chance!

## 🔧 Troubleshooting

**Issue**: "rich module not found"
```bash
pip install rich --break-system-packages
```

**Issue**: Stats not saving
```bash
# Check permissions
touch ~/.rpsls_stats.json
chmod 644 ~/.rpsls_stats.json
```

**Issue**: No colors in terminal
```bash
# Force colors
FORCE_COLOR=1 python3 rpsls_terminal.py
```

## 💬 Example Conversations

### Play a Quick Game
```
You: "Let's play RPSLS"
Claude: [Creates terminal game]
You: [Runs game, plays a few rounds]
You: "Show my stats"
Claude: "You've played 5 games: 2 wins, 2 losses, 1 tie!"
```

### Get the GUI
```
You: "I want a visual RPSLS game"
Claude: [Creates HTML artifact with click interface]
You: [Clicks choices, plays in browser]
```

### Tournament Mode
```
You: "Best of 5 RPSLS"
Claude: [Creates tournament version]
"First to 3 wins takes the match!"
```

## 📚 Learn More

- Full rules: Ask "Explain RPSLS rules"
- Strategy tips: Ask "RPSLS strategy tips"
- Stats format: Check ~/.rpsls_stats.json
- Skill docs: See SKILL.md

## 🎉 Ready to Play!

That's it! You're ready to play Rock Paper Scissors Lizard Spock!

**Just ask Claude**:
```
"Let's play rock paper scissors lizard spock"
```

And enjoy! 🎮🖖

---

**Remember**: "Scissors cuts paper, paper covers rock, rock crushes lizard, lizard poisons Spock, Spock smashes scissors, scissors decapitates lizard, lizard eats paper, paper disproves Spock, Spock vaporizes rock, and as it always has, rock crushes scissors!" - Sheldon Cooper
