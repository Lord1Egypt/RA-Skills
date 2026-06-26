## Description: <br>
Automated context health management for OpenClaw. Monitors token usage, snapshots memory, and resets sessions to maintain performance. Authored by Sophie. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zAyresz](https://clawhub.ai/user/zAyresz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to monitor context health, archive session summaries, update long-term memory, and reset local OpenClaw session state when maintenance is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delete main OpenClaw session files and restart the gateway without enforcing its stated token threshold. <br>
Mitigation: Use it only when local session cleanup is intended, and add an enforced threshold plus manual approval before scheduling or using reset behavior. <br>
Risk: The skill can rewrite OpenClaw memory and archive session summaries. <br>
Mitigation: Review generated summaries, keep backups, and define a retention policy for archived context data before deployment. <br>


## Reference(s): <br>
- [Sophie Optimizer on ClawHub](https://clawhub.ai/zAyresz/sophie-optimizer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local JSON archives and MEMORY.md updates when the artifact scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
