## Description: <br>
Wrap up a conversation session before starting a new one by preserving context, updating memory notes, committing changes, and reporting a concise summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[branexp](https://clawhub.ai/user/branexp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill at the end of a work session to capture useful context, update memory files and notes, commit workspace changes, and receive a short handoff summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill directs the agent to stage all changed files, commit them, and push to the configured Git remote automatically. <br>
Mitigation: Use it only in an intended repository, review changed files before any push, and require explicit confirmation for remote publishing when operating in sensitive workspaces. <br>
Risk: Session summaries and memory notes may capture sensitive workspace details or secrets if they are present in the conversation or files. <br>
Mitigation: Verify .gitignore coverage, avoid storing secrets in memory files, and review generated summaries before committing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/branexp/session-wrap-up) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown summary with filesystem updates and Git shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update memory and notes files, then commit and push repository changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
