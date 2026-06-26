# Example RPSLS Skill Interaction

This document shows how Claude uses the RPSLS skill to help users play the game.

## Example 1: Terminal Mode Request

**User**: "Let's play rock paper scissors lizard spock"

**Claude**: "I'll create a beautiful terminal version of Rock Paper Scissors Lizard Spock for you! 🎮

This enhanced version includes:
- ✨ Colored terminal UI with emojis
- 📊 Persistent statistics tracking
- 🏆 Win streak monitoring  
- 🎯 In-game rules display
- 💾 Auto-saves to ~/.rpsls_stats.json

Would you like me to create the terminal version or an interactive GUI?"

**User**: "Terminal version please"

**Claude**: [Creates `rpsls_terminal.py` file with the full Python code]

"Perfect! I've created your RPSLS game with the `rich` library for beautiful terminal graphics.

**To play**:
```bash
python3 rpsls_terminal.py
```

**Game Commands**:
- Choose: `rock`, `paper`, `scissors`, `lizard`, or `spock`
- Stats: Type `stats` anytime to see your record
- Rules: Type `rules` to display game rules
- Quit: Type `q` or `quit` to exit

**Game Features**:
- Each choice beats exactly 2 others
- Computer makes truly random choices
- Your statistics persist between sessions
- Track your best winning streak!

Have fun! May the odds be ever in your favor! 🖖"

---

## Example 2: GUI Mode Request

**User**: "Show me a visual RPSLS game I can click"

**Claude**: "Here's an interactive Rock Paper Scissors Lizard Spock game with a beautiful GUI! 🎨

[Creates HTML artifact with the full interactive game]

**How to Play**:
1. Click any choice: 🪨 Rock, 📄 Paper, ✂️ Scissors, 🦎 Lizard, or 🖖 Spock
2. Computer instantly makes its choice
3. See the result with animations!
4. Your score updates automatically

**Features**:
- ✨ Beautiful gradient design
- 🖱️ One-click gameplay
- 📊 Live scoreboard
- 🎭 Animated results
- 📋 Built-in rules
- 📱 Works on mobile too!

Just click any choice to start playing! The computer is ready to challenge you! 🎮"

---

## Example 3: Stats Request

**User**: "Show my RPSLS stats"

**Claude**: [Reads ~/.rpsls_stats.json]

"Here are your Rock Paper Scissors Lizard Spock statistics! 📊

**All-Time Record**:
- Total Games: 47
- Wins: 18 (38.3%)
- Losses: 21 (44.7%)  
- Ties: 8 (17.0%)

**Performance**:
- Best Winning Streak: 5 games
- Current Streak: 2 wins

**Choice Analysis**:
- Most Used: 🪨 Rock (15 times)
- Least Used: 🦎 Lizard (7 times)
- Your rock usage: 31.9% of all choices

**Pro Tip**: Try mixing up your choices more! You're using Rock quite often, which could make you predictable. Lizard and Spock are great choices too! 🎯"

---

## Example 4: Rules Explanation

**User**: "Explain the RPSLS rules"

**Claude**: "Let me explain Rock Paper Scissors Lizard Spock! This game was invented by Sam Kass and Karen Bryla, and popularized by The Big Bang Theory. 🎮

**The Rules** (as explained by Sheldon Cooper):

🪨 **Rock**:
- Crushes Scissors ✂️
- Crushes Lizard 🦎

📄 **Paper**:
- Covers Rock 🪨
- Disproves Spock 🖖

✂️ **Scissors**:
- Cuts Paper 📄
- Decapitates Lizard 🦎

🦎 **Lizard**:
- Eats Paper 📄
- Poisons Spock 🖖

🖖 **Spock**:
- Smashes Scissors ✂️
- Vaporizes Rock 🪨

**The Beauty of the Game**:
- Each choice defeats exactly 2 others
- Each choice loses to exactly 2 others
- Perfectly balanced!

**Why it's better than regular RPS**:
Traditional Rock Paper Scissors has only 3 choices, which can lead to ties. RPSLS adds Lizard and Spock, making ties less likely (20% vs 33%) and adding more strategy!

Ready to play? 🎲"

---

## Example 5: Tournament Mode

**User**: "Best of 5 RPSLS match"

**Claude**: "Let's do a Best of 5 tournament! First to win 3 rounds takes the championship! 🏆

[Creates tournament version with modified code]

I've created a tournament version where:
- Match is **Best of 5** (first to 3 wins)
- Score is tracked per round
- Shows tournament progress
- Declares the champion at the end

Run with:
```bash
python3 rpsls_tournament.py
```

**Tournament Format**:
- Round 1, 2, 3... until someone wins 3
- If you win a round, you get a point
- Ties don't count toward the 3 wins
- May go beyond 5 rounds if close!

Good luck! Show that computer who's boss! 💪"

---

## Example 6: Quick Play

**User**: "Play rock"

**Claude**: "🪨 You chose Rock!

🎲 Computer is thinking...

Computer chose: ✂️ Scissors

**Result**: 🎉 YOU WIN!
🪨 Rock crushes ✂️ Scissors!

Great choice! Rock is a classic and it paid off!

Want to play again? Try:
- 'Play paper'
- 'Choose lizard'  
- 'Pick spock'
- Or start a full game with 'Play RPSLS'"

---

## Example 7: Strategy Question

**User**: "What's the best RPSLS strategy?"

**Claude**: "Great question! Here's the strategic truth about RPSLS: 🎯

**The Mathematical Reality**:
Since the computer plays truly random (each choice has exactly 20% probability), there is **no single best strategy**. The game is perfectly balanced!

**However, here are some strategic tips**:

1. **Mix It Up**: Don't fall into patterns. If you always play Rock, a smart opponent would notice. Keep your choices unpredictable.

2. **Use All 5 Choices**: Many players stick to Rock, Paper, Scissors and forget about Lizard and Spock. This makes them predictable!

3. **Against Human Opponents** (not our random computer):
   - Humans tend to favor Rock
   - New players often forget Lizard and Spock
   - Look for patterns in their choices
   - Counter their most-used choice

4. **Psychology** (vs humans):
   - After losing, people often switch to what would have won
   - After winning, people often stick with their choice
   - Use this against human opponents!

5. **Remember the Defeats**:
   - Know what beats what instantly
   - Rock beats Scissors AND Lizard
   - Paper beats Rock AND Spock
   - Etc.

**Fun Fact**: Sam Kass (game creator) says beginners should use Spock more - it's psychologically intimidating! 🖖

Want to test these strategies? Let's play! 🎮"

---

## Example 8: Error Recovery

**User**: "My RPSLS game won't show colors"

**Claude**: "Let me help you fix the color display! 🎨

**Try these solutions**:

1. **Force Color Mode**:
```bash
FORCE_COLOR=1 python3 rpsls_terminal.py
```

2. **Check Terminal Support**:
```bash
echo $TERM
# Should show something like: xterm-256color
```

3. **Update Terminal**:
If using Windows CMD, colors may not work. Try:
- Git Bash
- Windows Terminal
- PowerShell 7+
- WSL (Linux subsystem)

4. **Install Rich Properly**:
```bash
pip install --upgrade rich --break-system-packages
```

5. **Test Rich**:
```bash
python3 -c "from rich.console import Console; Console().print('[bold red]Test[/]')"
```

If colors still don't work, you can use the **GUI mode** instead:
```
'Show me the RPSLS GUI'
```

The GUI works in any web browser with full colors! 🌈

Need more help? Let me know what error message you're seeing!"

---

## Example 9: Custom Request

**User**: "Create an RPSLS game but make the computer easier to beat"

**Claude**: "I'll create a modified version where the computer has some exploitable patterns! 😄

[Creates modified version with biased AI]

In this version, the computer:
- Chooses Rock 30% of the time (more than the fair 20%)
- Chooses Scissors least often (only 15%)
- After losing, tends to pick what would have won (70% chance)

**Strategy to Exploit**:
1. Since computer likes Rock, use **Paper** more often
2. Since computer rarely uses Scissors, **Rock** is safer
3. After you win, predict the counter and beat that!

Example: You play Rock and win (computer played Scissors)
→ Computer will likely play Rock next (beats Scissors)
→ So you should play Paper!

**Ethical Note**: This is just for fun and practice! In a real fair game, there's no way to predict a truly random opponent. 🎲

Run with:
```bash
python3 rpsls_easy_mode.py
```

Have fun exploiting the patterns! 🎯"

---

These examples show how the RPSLS skill enables Claude to:
- Create games in multiple formats (terminal/GUI)
- Provide strategic advice
- Track and display statistics
- Explain rules clearly
- Troubleshoot issues
- Customize the experience

The skill makes Claude an expert RPSLS game master! 🎮🖖
