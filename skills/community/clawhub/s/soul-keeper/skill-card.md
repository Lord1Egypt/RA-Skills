## Description: <br>
Soul Keeper monitors long-lived workspace memory and agent behavior files for update triggers, then proposes focused edits for user confirmation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mfang0126](https://clawhub.ai/user/mfang0126) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent users and developers use this skill to identify when workspace files such as SOUL.md, USER.md, AGENTS.md, MEMORY.md, WORKING.md, and TOOLS.md should be updated, and to receive one-file-at-a-time proposed changes for confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect persistent workspace memory and agent behavior files, so incorrect proposals may influence future work. <br>
Mitigation: Review every proposed edit before approval and keep the one-file-at-a-time confirmation workflow. <br>
Risk: The skill may record declined update suggestions for later reference. <br>
Mitigation: Change or disable that behavior if refused suggestions should not be retained. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown recommendations with proposed file changes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before applying edits.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
