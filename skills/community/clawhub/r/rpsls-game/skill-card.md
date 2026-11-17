## Description:

Play the classic Rock Paper Scissors Lizard Spock game (popularized by The Big Bang Theory) with an AI opponent, including decorated terminal and interactive GUI modes with score tracking, statistics, and animations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[akhmittra](https://clawhub.ai/user/akhmittra)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to play Rock Paper Scissors Lizard Spock through an agent-generated terminal script, browser GUI artifact, or quick-play chat flow. The skill supports rules explanations, tournament play, and local score and statistics tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance includes an unsafe Python package installation command that can alter protected system packages.

Mitigation: Review install instructions before use, prefer a virtual environment with a pinned rich version, and avoid --break-system-packages.

Risk: Terminal-mode statistics are stored locally at ~/.rpsls_stats.json.

Mitigation: Delete ~/.rpsls_stats.json or avoid terminal-mode statistics if retained local game history is not desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/akhmittra/skills/rpsls-game)
- [README](artifact/README.md)
- [Quick Start Guide](artifact/QUICKSTART.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown chat responses with Python, HTML, JavaScript, and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local game files and persist terminal-mode statistics at ~/.rpsls_stats.json.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
