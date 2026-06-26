---
name: Rock Paper Scissors Lizard Spock
description: Play the classic Rock Paper Scissors Lizard Spock game (popularized by The Big Bang Theory) with an AI opponent. Includes both decorated terminal and interactive GUI modes with score tracking, statistics, and animations.
version: 1.0.0
author: AM (akm626)
tags: [game, entertainment, interactive, python, gui, terminal]
requires:
  bins: [python3]
  packages: [rich]
---

# Rock Paper Scissors Lizard Spock Game

An enhanced implementation of Rock Paper Scissors Lizard Spock with beautiful UI, statistics tracking, and multiple play modes.

## Game Rules

**Classic RPSLS Rules** (from The Big Bang Theory):
- 🪨 **Rock** crushes Scissors and crushes Lizard
- 📄 **Paper** covers Rock and disproves Spock
- ✂️ **Scissors** cuts Paper and decapitates Lizard
- 🦎 **Lizard** eats Paper and poisons Spock
- 🖖 **Spock** smashes Scissors and vaporizes Rock

Each choice defeats exactly 2 others and loses to exactly 2 others.

## Skill Capabilities

This skill provides three ways to play:

1. **Decorated Terminal Mode** - Beautiful ASCII art UI with colors and animations
2. **Interactive GUI Mode** - HTML/JavaScript artifact with click-based gameplay
3. **Quick Play Mode** - Single command for fast games

## Usage

### Start a Game

**Terminal Mode (Recommended)**:
```
"Let's play Rock Paper Scissors Lizard Spock"
"Play RPSLS in terminal mode"
"Start a decorated RPSLS game"
```

**GUI Mode**:
```
"Show me the RPSLS GUI"
"Play RPSLS with a visual interface"
"Create an interactive RPSLS game"
```

### Quick Commands

```
"Play rock" / "Choose rock" → Makes a move
"RPSLS stats" → View game statistics
"RPSLS rules" → Display game rules
"Best of 3" / "Best of 5" → Start tournament mode
```

## Implementation

When the user requests to play Rock Paper Scissors Lizard Spock, follow these steps:

### Step 1: Determine Mode

Ask which mode they prefer (or default to terminal if not specified):
- Terminal mode (decorated, colorful CLI)
- GUI mode (interactive HTML artifact)
- Quick play (single round)

### Step 2: Create the Game

#### For Terminal Mode:

Create a Python script using `rich` library for beautiful terminal UI:

```python
#!/usr/bin/env python3
"""
Rock Paper Scissors Lizard Spock - Decorated Terminal Edition
Beautiful ASCII art game with colors, animations, and statistics
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt
from rich import box
import random
import json
import os
from datetime import datetime

console = Console()

# Game rules: what each choice defeats
DEFEATS = {
    "rock": {"scissors": "crushes", "lizard": "crushes"},
    "paper": {"rock": "covers", "spock": "disproves"},
    "scissors": {"paper": "cuts", "lizard": "decapitates"},
    "lizard": {"paper": "eats", "spock": "poisons"},
    "spock": {"scissors": "smashes", "rock": "vaporizes"}
}

# Emojis for choices
EMOJIS = {
    "rock": "🪨",
    "paper": "📄",
    "scissors": "✂️",
    "lizard": "🦎",
    "spock": "🖖"
}

# Colors for choices
COLORS = {
    "rock": "red",
    "paper": "blue",
    "scissors": "yellow",
    "lizard": "green",
    "spock": "cyan"
}

class RPSLSGame:
    def __init__(self):
        self.stats = self.load_stats()
        self.session_wins = 0
        self.session_losses = 0
        self.session_ties = 0
        
    def load_stats(self):
        """Load game statistics from file"""
        stats_file = os.path.expanduser("~/.rpsls_stats.json")
        if os.path.exists(stats_file):
            try:
                with open(stats_file, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {
            "total_games": 0,
            "wins": 0,
            "losses": 0,
            "ties": 0,
            "choice_freq": {choice: 0 for choice in DEFEATS.keys()},
            "best_streak": 0,
            "current_streak": 0
        }
    
    def save_stats(self):
        """Save game statistics to file"""
        stats_file = os.path.expanduser("~/.rpsls_stats.json")
        try:
            with open(stats_file, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except:
            pass
    
    def show_banner(self):
        """Display game banner"""
        banner = """
╔═══════════════════════════════════════════════════╗
║  🎮 ROCK PAPER SCISSORS LIZARD SPOCK 🎮          ║
║                                                   ║
║  🪨 Rock    📄 Paper    ✂️ Scissors              ║
║  🦎 Lizard  🖖 Spock                             ║
║                                                   ║
║  "A game of strategic brilliance!" - Sheldon     ║
╚═══════════════════════════════════════════════════╝
"""
        console.print(banner, style="bold cyan")
    
    def show_rules(self):
        """Display game rules"""
        rules_table = Table(title="🎯 Game Rules", box=box.ROUNDED, style="cyan")
        rules_table.add_column("Choice", style="bold")
        rules_table.add_column("Defeats", style="green")
        rules_table.add_column("Action", style="yellow")
        
        rules_table.add_row("🪨 Rock", "✂️ Scissors, 🦎 Lizard", "crushes both")
        rules_table.add_row("📄 Paper", "🪨 Rock, 🖖 Spock", "covers, disproves")
        rules_table.add_row("✂️ Scissors", "📄 Paper, 🦎 Lizard", "cuts, decapitates")
        rules_table.add_row("🦎 Lizard", "📄 Paper, 🖖 Spock", "eats, poisons")
        rules_table.add_row("🖖 Spock", "✂️ Scissors, 🪨 Rock", "smashes, vaporizes")
        
        console.print(rules_table)
    
    def show_stats(self):
        """Display game statistics"""
        stats_panel = Panel(
            f"""[bold cyan]📊 Game Statistics[/bold cyan]

[yellow]All-Time Record:[/yellow]
  Total Games: {self.stats['total_games']}
  Wins: [green]{self.stats['wins']}[/green]
  Losses: [red]{self.stats['losses']}[/red]
  Ties: [blue]{self.stats['ties']}[/blue]
  Win Rate: {self.stats['wins'] / max(1, self.stats['total_games']) * 100:.1f}%
  
[yellow]Best Streak:[/yellow] {self.stats['best_streak']} wins
[yellow]Current Streak:[/yellow] {self.stats['current_streak']} wins

[yellow]This Session:[/yellow]
  Wins: [green]{self.session_wins}[/green]
  Losses: [red]{self.session_losses}[/red]
  Ties: [blue]{self.session_ties}[/blue]

[yellow]Most Used Choice:[/yellow] {max(self.stats['choice_freq'], key=self.stats['choice_freq'].get)} 
({self.stats['choice_freq'][max(self.stats['choice_freq'], key=self.stats['choice_freq'].get)]} times)
""",
            border_style="cyan",
            title="Statistics",
            expand=False
        )
        console.print(stats_panel)
    
    def get_player_choice(self):
        """Get player's choice with nice prompt"""
        choices = list(DEFEATS.keys())
        choice_display = " | ".join([f"{EMOJIS[c]} {c}" for c in choices])
        
        console.print(f"\n[bold yellow]Your move:[/bold yellow] {choice_display}")
        
        while True:
            choice = Prompt.ask(
                "Choose your weapon",
                choices=choices + ['q', 'quit', 'stats', 'rules'],
                default="rock"
            ).lower()
            
            if choice in ['q', 'quit']:
                return None
            elif choice == 'stats':
                self.show_stats()
                continue
            elif choice == 'rules':
                self.show_rules()
                continue
            elif choice in choices:
                return choice
    
    def get_computer_choice(self):
        """AI opponent's choice"""
        return random.choice(list(DEFEATS.keys()))
    
    def determine_winner(self, player_choice, computer_choice):
        """Determine the winner and return result"""
        if player_choice == computer_choice:
            return "tie", None
        elif computer_choice in DEFEATS[player_choice]:
            action = DEFEATS[player_choice][computer_choice]
            return "win", action
        else:
            # Find what action the computer used
            action = DEFEATS[computer_choice][player_choice]
            return "loss", action
    
    def show_choices(self, player_choice, computer_choice):
        """Display choices with animation"""
        console.print("\n[bold]Choices:[/bold]")
        
        choice_table = Table(box=box.ROUNDED, show_header=False)
        choice_table.add_column("Player", style="bold green", width=20)
        choice_table.add_column("VS", style="bold white", width=5, justify="center")
        choice_table.add_column("Computer", style="bold red", width=20)
        
        player_display = f"{EMOJIS[player_choice]} {player_choice.capitalize()}"
        computer_display = f"{EMOJIS[computer_choice]} {computer_choice.capitalize()}"
        
        choice_table.add_row(player_display, "VS", computer_display)
        console.print(choice_table)
    
    def show_result(self, result, action, player_choice, computer_choice):
        """Display game result with style"""
        if result == "tie":
            console.print(Panel(
                "[bold yellow]🤝 IT'S A TIE! 🤝[/bold yellow]\nGreat minds think alike!",
                border_style="yellow",
                expand=False
            ))
        elif result == "win":
            console.print(Panel(
                f"[bold green]🎉 YOU WIN! 🎉[/bold green]\n"
                f"{EMOJIS[player_choice]} {player_choice.capitalize()} {action} "
                f"{EMOJIS[computer_choice]} {computer_choice.capitalize()}!",
                border_style="green",
                expand=False
            ))
        else:
            console.print(Panel(
                f"[bold red]😞 YOU LOSE! 😞[/bold red]\n"
                f"{EMOJIS[computer_choice]} {computer_choice.capitalize()} {action} "
                f"{EMOJIS[player_choice]} {player_choice.capitalize()}!",
                border_style="red",
                expand=False
            ))
    
    def update_stats(self, result, player_choice):
        """Update game statistics"""
        self.stats['total_games'] += 1
        self.stats['choice_freq'][player_choice] += 1
        
        if result == "win":
            self.stats['wins'] += 1
            self.session_wins += 1
            self.stats['current_streak'] += 1
            if self.stats['current_streak'] > self.stats['best_streak']:
                self.stats['best_streak'] = self.stats['current_streak']
        elif result == "loss":
            self.stats['losses'] += 1
            self.session_losses += 1
            self.stats['current_streak'] = 0
        else:
            self.stats['ties'] += 1
            self.session_ties += 1
        
        self.save_stats()
    
    def show_score(self):
        """Display current session score"""
        console.print(f"\n[bold]Session Score:[/bold] "
                     f"[green]Wins: {self.session_wins}[/green] | "
                     f"[red]Losses: {self.session_losses}[/red] | "
                     f"[blue]Ties: {self.session_ties}[/blue]")
    
    def play_round(self):
        """Play one round"""
        player_choice = self.get_player_choice()
        
        if player_choice is None:
            return False  # User wants to quit
        
        console.print("\n[dim]🎲 Computer is thinking...[/dim]")
        computer_choice = self.get_computer_choice()
        
        self.show_choices(player_choice, computer_choice)
        
        result, action = self.determine_winner(player_choice, computer_choice)
        self.show_result(result, action, player_choice, computer_choice)
        
        self.update_stats(result, player_choice)
        self.show_score()
        
        return True  # Continue playing
    
    def play(self):
        """Main game loop"""
        self.show_banner()
        console.print("\n[dim]Type 'stats' to see statistics, 'rules' for game rules, or 'q' to quit[/dim]\n")
        
        while True:
            if not self.play_round():
                break
            
            console.print()  # Spacing between rounds
        
        # Show final stats
        console.print("\n[bold cyan]Thanks for playing![/bold cyan]")
        self.show_stats()

def main():
    game = RPSLSGame()
    game.play()

if __name__ == "__main__":
    main()
```

**Key Features**:
- 🎨 Beautiful colored terminal UI with rich library
- 📊 Persistent statistics tracking
- 🏆 Win streak tracking
- 🎯 Choice frequency analysis
- 📋 In-game rules and stats display
- 💾 Stats saved to ~/.rpsls_stats.json

**To run**: Save as `rpsls_terminal.py` and execute with `python3 rpsls_terminal.py`

#### For GUI Mode:

Create an interactive HTML artifact:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rock Paper Scissors Lizard Spock</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .game-container {
            background: white;
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 800px;
            width: 100%;
        }
        
        h1 {
            text-align: center;
            color: #667eea;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-style: italic;
        }
        
        .choices {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 20px;
            margin: 30px 0;
        }
        
        .choice-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            border-radius: 15px;
            padding: 30px 20px;
            cursor: pointer;
            transition: all 0.3s ease;
            color: white;
            font-size: 3em;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .choice-btn:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        }
        
        .choice-btn:active {
            transform: translateY(-2px);
        }
        
        .choice-label {
            display: block;
            font-size: 0.4em;
            margin-top: 10px;
            font-weight: bold;
        }
        
        .game-area {
            margin: 30px 0;
            min-height: 200px;
        }
        
        .result-display {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 30px;
            text-align: center;
            margin: 20px 0;
        }
        
        .result-display.hidden {
            display: none;
        }
        
        .choices-comparison {
            display: flex;
            justify-content: space-around;
            align-items: center;
            margin: 20px 0;
        }
        
        .choice-display {
            text-align: center;
        }
        
        .choice-icon {
            font-size: 4em;
            margin-bottom: 10px;
        }
        
        .choice-name {
            font-size: 1.2em;
            font-weight: bold;
            color: #667eea;
        }
        
        .vs-text {
            font-size: 2em;
            font-weight: bold;
            color: #999;
        }
        
        .result-text {
            font-size: 2em;
            font-weight: bold;
            margin: 20px 0;
        }
        
        .result-text.win {
            color: #28a745;
        }
        
        .result-text.loss {
            color: #dc3545;
        }
        
        .result-text.tie {
            color: #ffc107;
        }
        
        .result-explanation {
            font-size: 1.1em;
            color: #666;
            margin-top: 10px;
        }
        
        .scoreboard {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin: 20px 0;
        }
        
        .score-item {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        
        .score-label {
            font-size: 0.9em;
            opacity: 0.9;
        }
        
        .score-value {
            font-size: 2.5em;
            font-weight: bold;
            margin-top: 5px;
        }
        
        .controls {
            display: flex;
            gap: 15px;
            justify-content: center;
            margin-top: 20px;
        }
        
        .btn {
            padding: 12px 30px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            font-weight: bold;
            transition: all 0.3s ease;
        }
        
        .btn-primary {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .btn-secondary {
            background: #f8f9fa;
            color: #667eea;
            border: 2px solid #667eea;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .rules {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 20px;
            margin-top: 20px;
        }
        
        .rules h3 {
            color: #667eea;
            margin-bottom: 15px;
        }
        
        .rules ul {
            list-style: none;
            padding-left: 0;
        }
        
        .rules li {
            padding: 8px 0;
            color: #666;
        }
        
        .rules li strong {
            color: #333;
        }
        
        @keyframes shake {
            0%, 100% { transform: translateX(0); }
            25% { transform: translateX(-10px); }
            75% { transform: translateX(10px); }
        }
        
        .shake {
            animation: shake 0.5s ease;
        }
    </style>
</head>
<body>
    <div class="game-container">
        <h1>🎮 Rock Paper Scissors Lizard Spock</h1>
        <p class="subtitle">"A game of strategic brilliance!" - Sheldon Cooper</p>
        
        <div class="scoreboard">
            <div class="score-item">
                <div class="score-label">Wins</div>
                <div class="score-value" id="wins">0</div>
            </div>
            <div class="score-item">
                <div class="score-label">Losses</div>
                <div class="score-value" id="losses">0</div>
            </div>
            <div class="score-item">
                <div class="score-label">Ties</div>
                <div class="score-value" id="ties">0</div>
            </div>
        </div>
        
        <div class="choices">
            <button class="choice-btn" onclick="play('rock')">
                🪨
                <span class="choice-label">Rock</span>
            </button>
            <button class="choice-btn" onclick="play('paper')">
                📄
                <span class="choice-label">Paper</span>
            </button>
            <button class="choice-btn" onclick="play('scissors')">
                ✂️
                <span class="choice-label">Scissors</span>
            </button>
            <button class="choice-btn" onclick="play('lizard')">
                🦎
                <span class="choice-label">Lizard</span>
            </button>
            <button class="choice-btn" onclick="play('spock')">
                🖖
                <span class="choice-label">Spock</span>
            </button>
        </div>
        
        <div class="result-display hidden" id="result-display">
            <div class="choices-comparison">
                <div class="choice-display">
                    <div class="choice-icon" id="player-icon"></div>
                    <div class="choice-name">You</div>
                </div>
                <div class="vs-text">VS</div>
                <div class="choice-display">
                    <div class="choice-icon" id="computer-icon"></div>
                    <div class="choice-name">Computer</div>
                </div>
            </div>
            <div class="result-text" id="result-text"></div>
            <div class="result-explanation" id="result-explanation"></div>
        </div>
        
        <div class="controls">
            <button class="btn btn-primary" onclick="playAgain()">Play Again</button>
            <button class="btn btn-secondary" onclick="resetScore()">Reset Score</button>
            <button class="btn btn-secondary" onclick="toggleRules()">Rules</button>
        </div>
        
        <div class="rules" id="rules" style="display: none;">
            <h3>📋 Game Rules</h3>
            <ul>
                <li>🪨 <strong>Rock</strong> crushes Scissors and crushes Lizard</li>
                <li>📄 <strong>Paper</strong> covers Rock and disproves Spock</li>
                <li>✂️ <strong>Scissors</strong> cuts Paper and decapitates Lizard</li>
                <li>🦎 <strong>Lizard</strong> eats Paper and poisons Spock</li>
                <li>🖖 <strong>Spock</strong> smashes Scissors and vaporizes Rock</li>
            </ul>
        </div>
    </div>
    
    <script>
        const EMOJIS = {
            rock: '🪨',
            paper: '📄',
            scissors: '✂️',
            lizard: '🦎',
            spock: '🖖'
        };
        
        const DEFEATS = {
            rock: {scissors: 'crushes', lizard: 'crushes'},
            paper: {rock: 'covers', spock: 'disproves'},
            scissors: {paper: 'cuts', lizard: 'decapitates'},
            lizard: {paper: 'eats', spock: 'poisons'},
            spock: {scissors: 'smashes', rock: 'vaporizes'}
        };
        
        let wins = 0;
        let losses = 0;
        let ties = 0;
        
        function play(playerChoice) {
            const choices = ['rock', 'paper', 'scissors', 'lizard', 'spock'];
            const computerChoice = choices[Math.floor(Math.random() * choices.length)];
            
            document.getElementById('player-icon').textContent = EMOJIS[playerChoice];
            document.getElementById('computer-icon').textContent = EMOJIS[computerChoice];
            
            const result = determineWinner(playerChoice, computerChoice);
            displayResult(result, playerChoice, computerChoice);
            updateScore(result);
            
            const resultDisplay = document.getElementById('result-display');
            resultDisplay.classList.remove('hidden');
            resultDisplay.classList.add('shake');
            setTimeout(() => resultDisplay.classList.remove('shake'), 500);
        }
        
        function determineWinner(player, computer) {
            if (player === computer) {
                return {outcome: 'tie', action: null};
            }
            
            if (DEFEATS[player] && DEFEATS[player][computer]) {
                return {outcome: 'win', action: DEFEATS[player][computer]};
            }
            
            return {outcome: 'loss', action: DEFEATS[computer][player]};
        }
        
        function displayResult(result, playerChoice, computerChoice) {
            const resultText = document.getElementById('result-text');
            const resultExplanation = document.getElementById('result-explanation');
            
            resultText.className = 'result-text ' + result.outcome;
            
            if (result.outcome === 'tie') {
                resultText.textContent = "🤝 It's a Tie!";
                resultExplanation.textContent = "Great minds think alike!";
            } else if (result.outcome === 'win') {
                resultText.textContent = "🎉 You Win!";
                resultExplanation.textContent = `${capitalize(playerChoice)} ${result.action} ${capitalize(computerChoice)}!`;
            } else {
                resultText.textContent = "😞 You Lose!";
                resultExplanation.textContent = `${capitalize(computerChoice)} ${result.action} ${capitalize(playerChoice)}!`;
            }
        }
        
        function updateScore(result) {
            if (result.outcome === 'win') {
                wins++;
                document.getElementById('wins').textContent = wins;
            } else if (result.outcome === 'loss') {
                losses++;
                document.getElementById('losses').textContent = losses;
            } else {
                ties++;
                document.getElementById('ties').textContent = ties;
            }
        }
        
        function playAgain() {
            document.getElementById('result-display').classList.add('hidden');
        }
        
        function resetScore() {
            wins = 0;
            losses = 0;
            ties = 0;
            document.getElementById('wins').textContent = wins;
            document.getElementById('losses').textContent = losses;
            document.getElementById('ties').textContent = ties;
            document.getElementById('result-display').classList.add('hidden');
        }
        
        function toggleRules() {
            const rules = document.getElementById('rules');
            rules.style.display = rules.style.display === 'none' ? 'block' : 'none';
        }
        
        function capitalize(str) {
            return str.charAt(0).toUpperCase() + str.slice(1);
        }
    </script>
</body>
</html>
```

**GUI Features**:
- 🎨 Beautiful gradient design
- 🖱️ Click-based gameplay
- 📊 Real-time score tracking
- 🎭 Animated results
- 📱 Responsive design
- 📋 Built-in rules display

### Step 3: Provide Instructions

After creating the game, provide clear instructions:
- How to make choices
- How to view stats/rules
- How to exit
- Tips for playing

### Step 4: Support Follow-up Actions

Handle these common requests:
- "Play again" → Start new round
- "Show stats" → Display statistics
- "Reset score" → Clear session stats
- "Explain the rules" → Show rules table
- "What beats rock?" → Explain game logic

## Game Strategy Tips

Share these tips with players:
- Each choice wins against exactly 2 others
- Computer choice is truly random (no pattern)
- Lizard and Spock add complexity to traditional RPS
- Mix up your choices - patterns are exploitable
- There's no "best" choice - it's balanced!

## Advanced Features

### Tournament Mode

For "best of N" requests:
```python
def tournament(rounds=3):
    game = RPSLSGame()
    player_score = 0
    computer_score = 0
    
    for round_num in range(1, rounds + 1):
        console.print(f"\n[bold]Round {round_num} of {rounds}[/bold]")
        result = game.play_round()
        # Track tournament progress
    
    # Declare tournament winner
```

### Adaptive AI

For advanced mode, create an AI that learns from player patterns:
```python
class AdaptiveAI:
    def __init__(self):
        self.player_history = []
        self.pattern_length = 3
    
    def predict_next_move(self):
        if len(self.player_history) < self.pattern_length:
            return random.choice(choices)
        
        # Look for patterns in recent history
        recent = tuple(self.player_history[-self.pattern_length:])
        # Predict and counter
```

## Troubleshooting

### Issue: "rich" module not found
**Solution**: Install with `pip install rich --break-system-packages`

### Issue: Stats file permission error
**Solution**: Stats save to ~/.rpsls_stats.json - ensure write permissions

### Issue: Terminal doesn't show colors
**Solution**: Try running with `FORCE_COLOR=1 python3 script.py`

## Example Interactions

**Example 1: Quick Game**
```
User: "Let's play rock paper scissors lizard spock"
Claude: [Creates terminal game script]
"I've created a beautiful terminal version of RPSLS! 
 Run it with: python3 rpsls_terminal.py
 
 Features:
 - Colored UI with emojis
 - Statistics tracking
 - Win streaks
 - In-game rules
 
 Just choose rock, paper, scissors, lizard, or spock!"
```

**Example 2: GUI Request**
```
User: "Show me a visual RPSLS game"
Claude: [Creates HTML artifact]
"Here's an interactive RPSLS game! Click any choice to play:
 🪨 Rock  📄 Paper  ✂️ Scissors  🦎 Lizard  🖖 Spock
 
 The computer will make its choice instantly and show the result!"
```

**Example 3: Stats Request**
```
User: "Show my RPSLS stats"
Claude: [Reads ~/.rpsls_stats.json]
"Your RPSLS Statistics:
 
 Total Games: 47
 Wins: 18 (38.3%)
 Losses: 21 (44.7%)
 Ties: 8 (17.0%)
 
 Best Streak: 5 wins
 Most Used: Rock (15 times)"
```

## Notes for Claude

- Always ask which mode (terminal/GUI) unless user specifies
- For terminal mode, ensure `rich` is available or offer to install it
- For GUI mode, create as an HTML artifact (not a file)
- Include emojis and colors for better UX
- Save stats persistently for long-term tracking
- Explain the rules if user seems unfamiliar with RPSLS
- Make it fun and engaging! This is entertainment.

## Credits

Based on the Rock Paper Scissors Lizard Spock game popularized by:
- **The Big Bang Theory** TV show (Sheldon Cooper's game)
- **Original concept**: Sam Kass and Karen Bryla
- **Enhanced by**: AM (akm626) for OpenClaw

## Version History

- v1.0.0 (2026-04-03): Initial release with terminal and GUI modes
