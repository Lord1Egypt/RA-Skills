## Description:

街机 is an ASCII text-game arcade that helps an agent host, render, and referee board games, puzzle games, and casual chat games in conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run text-based games in an agent chat, including chess-like board games, Minesweeper, Sudoku, 2048, Sokoban, word games, and number guessing. The agent produces turn-by-turn prompts, ASCII boards, move validation, and game-state guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release asks for broad read, write, and command execution tools that are not necessary for normal chat-based game play.

Mitigation: Scope activation and permissions to game-related chat behavior and remove or justify any file access, write access, or command execution capability before installation.

Risk: The artifact includes unrelated file, API, command-execution, and API-key guidance that can confuse users about the skill's actual behavior and risk profile.

Mitigation: Review the skill text before use and remove unrelated file/API/command claims and API-key guidance unless those capabilities are explicitly required and safely scoped.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/text-rpg-arcade-v3)
- [Publisher profile](https://clawhub.ai/user/thcjp)
- [Artifact homepage](https://skillhub.cn/skill/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown and ASCII text game boards]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Interactive turn-by-turn responses may include rendered boards, move prompts, rule checks, status messages, and JSON examples.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
