## Description:

Text Game Arcade Universe V3 is a Chinese-first chat skill for running an ASCII text game lobby with board games, puzzles, word games, rule checks, difficulty settings, undo, AI opponent, and referee modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to play or host Chinese-first text games inside chat, including board games, puzzles, and word or number games with rendered boards and turn validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad casual-game trigger phrases may open the game lobby when the user intended a general conversation.

Mitigation: Review trigger behavior during deployment and narrow routing or ask a clarifying question for ambiguous game-related requests.

Risk: Chinese-first output may be less usable for English-only users.

Mitigation: Ask for English responses when needed or localize the skill instructions before deploying to English-first audiences.

Risk: Complex board-game adjudication may use casual legal-mode handling rather than professional engine-grade analysis.

Mitigation: Use referee mode for transparent move validation and require human review for competitive, rated, or high-stakes game decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/52yuanchangxing/skills/text-game-arcade-universe-v3)
- [README](README.md)
- [Changelog](CHANGELOG.md)
- [Rendering and State](references/rendering-and-state.md)
- [Triggers and Routing](references/triggers-and-routing.md)
- [Gomoku](references/gomoku.md)
- [Go](references/go.md)
- [Tic-Tac-Toe](references/tictactoe.md)
- [Othello](references/othello.md)
- [Connect Four](references/connect-four.md)
- [Battleship](references/battleship.md)
- [Minesweeper](references/minesweeper.md)
- [Sudoku](references/sudoku.md)
- [2048](references/2048.md)
- [Xiangqi](references/xiangqi.md)
- [Chess](references/chess.md)
- [Sokoban](references/sokoban.md)
- [Maze](references/maze.md)
- [Word and Number Games](references/word-and-number-games.md)
- [Puzzle Classics](references/puzzle-classics.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text with fenced ASCII or Unicode board diagrams]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-first interactive chat output; board state, legal moves, hints, and mode changes are maintained within the conversation.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and changelog describe v3 content)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
