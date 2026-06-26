## Description: <br>
Play the classic Rock Paper Scissors Lizard Spock game with an AI opponent, decorated terminal and GUI modes, score tracking, statistics, and animations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[akhmittra](https://clawhub.ai/user/akhmittra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to have an agent create and run a local Rock Paper Scissors Lizard Spock game in terminal, GUI, quick-play, or tournament modes. It is intended for entertainment, lightweight interaction, and showing game rules or saved gameplay statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The terminal mode stores gameplay history in ~/.rpsls_stats.json. <br>
Mitigation: Tell users about the local stats file before use and delete ~/.rpsls_stats.json when they want to clear saved gameplay history. <br>
Risk: The documentation suggests installing the rich package with --break-system-packages. <br>
Mitigation: Prefer installing rich in a virtual environment or other isolated Python environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/akhmittra/rpsls-game) <br>
- [Original Rock Paper Scissors Lizard Spock game information](https://www.samkass.com/theories/RPSSL.html) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [ClawHub](https://clawhub.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Python, HTML, JavaScript, JSON, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a local Python game script, an interactive HTML artifact, and a small local stats JSON file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
