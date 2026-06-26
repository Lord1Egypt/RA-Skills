## Description: <br>
Task Killer helps an agent recognize explicit stop or cancel requests, interrupt the current task, and clean up related subagents, processes, or temporary state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shiker1996](https://clawhub.ai/user/shiker1996) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent users and developers use this skill to stop misdirected or obsolete work quickly, provide interruption feedback, and prepare the agent for a new instruction. It is intended for workflows where saving time, tokens, and active resources matters more than continuing the current task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can terminate running agents and process sessions too broadly when common stop phrases trigger it. <br>
Mitigation: Limit activation to explicit commands, require confirmation before killing processes or subagents, and restrict cleanup to resources created by the current task or session. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/shiker1996/task-killer) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with status text, code snippets, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include counts of terminated subagents, killed process sessions, and cleaned temporary files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
