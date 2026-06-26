## Description: <br>
Track vitamin and supplement intake with goals and reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain-lab](https://clawhub.ai/user/bytesagain-lab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this terminal-first skill to log supplement intake, set wellness goals, review local history, and manage reminder-style entries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wellness and supplement history is stored as plaintext on the local machine. <br>
Mitigation: Avoid entering highly sensitive medical details and review or delete ~/.local/share/vitamin/ when finished. <br>
Risk: The export command has a duplicate command bug that may make vitamin export <fmt> unreliable. <br>
Mitigation: Do not rely on vitamin export <fmt> for backups until the command behavior is fixed and verified. <br>


## Reference(s): <br>
- [Vitamin on ClawHub](https://clawhub.ai/bytesagain-lab/vitamin) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation and review of local plaintext wellness logs under ~/.local/share/vitamin/.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
