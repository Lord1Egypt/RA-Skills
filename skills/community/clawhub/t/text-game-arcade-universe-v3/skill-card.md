## Description: <br>
A chat-based ASCII and Unicode text game arcade for board, puzzle, word, and number games with rule-aware rendering, move validation, difficulty settings, undo support, and judge modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[52YuanChangXing](https://clawhub.ai/user/52YuanChangXing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to play text-based games directly in chat, including board games, puzzles, word games, and number games. It helps the agent render readable boards, maintain game state, validate legal moves, and provide concise next-step prompts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad game-related triggers may activate the arcade when a user is only discussing games or using casual Chinese phrases about playing. <br>
Mitigation: Use a clarification step or narrower routing when the user intent is ambiguous, and start gameplay only when the user clearly asks to play, render a board, or run a game session. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/52YuanChangXing/text-game-arcade-universe-v3) <br>
- [README](artifact/README.md) <br>
- [Rendering and State](artifact/references/rendering-and-state.md) <br>
- [Triggers and Routing](artifact/references/triggers-and-routing.md) <br>
- [Gomoku](artifact/references/gomoku.md) <br>
- [Go](artifact/references/go.md) <br>
- [Tic-Tac-Toe](artifact/references/tictactoe.md) <br>
- [Othello](artifact/references/othello.md) <br>
- [Connect Four](artifact/references/connect-four.md) <br>
- [Battleship](artifact/references/battleship.md) <br>
- [Minesweeper](artifact/references/minesweeper.md) <br>
- [Sudoku](artifact/references/sudoku.md) <br>
- [2048](artifact/references/2048.md) <br>
- [Xiangqi](artifact/references/xiangqi.md) <br>
- [Chess](artifact/references/chess.md) <br>
- [Sokoban](artifact/references/sokoban.md) <br>
- [Maze](artifact/references/maze.md) <br>
- [Word and Number Games](artifact/references/word-and-number-games.md) <br>
- [Puzzle Classics](artifact/references/puzzle-classics.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown with monospace text/code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces chat-based game state, boards, move validation feedback, and next-step prompts; no external tool output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter and changelog describe 3.0.0 content) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
