## Description: <br>
Step helps agents log daily steps, set fitness goals, chart walking trends, and manage wellness notes through terminal commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Step to run a local command-line tracker for steps, goals, reminders, trends, statistics, and exports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Step stores step, goal, reminder, and related wellness notes in plaintext under ~/.local/share/step/. <br>
Mitigation: Avoid entering highly sensitive medical details, and protect or delete exported files when they are no longer needed. <br>


## Reference(s): <br>
- [Step on ClawHub](https://clawhub.ai/bytesagain-lab/step) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal command text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create plaintext log and export files under ~/.local/share/step/ when the generated shell command is run.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release evidence; artifact files report 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
