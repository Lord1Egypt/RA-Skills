## Description: <br>
Runs shell commands inside a dedicated tmux session named claw, returns captured command output, and blocks commands that match its dangerous-command checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fresh3](https://clawhub.ai/user/fresh3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let an agent run local shell commands in a dedicated tmux session and read back terminal output. It is intended for workflows where direct local shell access is explicitly desired. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides raw local shell access through an agent tool, and the release security summary says its safety controls and tmux boundary are weak for that level of access. <br>
Mitigation: Install only when agent shell execution is intentionally required; run it in a constrained workspace with least-privilege permissions. <br>
Risk: The security guidance warns against relying on dangerous-command detection and using the skill around secrets or sensitive directories. <br>
Mitigation: Do not treat the dangerous-command checks as a sandbox; keep secrets and sensitive directories out of scope and require explicit human review for high-impact commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fresh3/taizi-claw-shell) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/fresh3) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands] <br>
**Output Format:** [JSON object containing the submitted command and captured tmux pane output, or an error object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the tmux session named claw and captures recent pane output after command execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
