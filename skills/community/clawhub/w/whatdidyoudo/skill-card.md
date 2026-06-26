## Description: <br>
Reconstruct and display a plain-language log of recent agent tool calls, actions taken, and decisions made. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openauthority](https://clawhub.ai/user/openauthority) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users and agents use this skill to review recent assistant activity after autonomous work, including tool calls, file operations, shell commands, decisions, and high-level session summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The activity summary can still reveal tool names, file paths, commands, and operational context after sensitive work. <br>
Mitigation: Avoid invoking the skill immediately after highly sensitive work unless that operational context is acceptable to disclose. <br>
Risk: The skill reconstructs actions from conversation context rather than a structured audit log, so long sessions may omit early activity or lose exact details. <br>
Mitigation: Use the output for situational review, not compliance auditing, and rely on an authoritative audit log when exact arguments, timestamps, and policy decisions are required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/openauthority/whatdidyoudo) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain-text action summaries with numbered lists and compact summary tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Redacts credential-like values when detected; no external services are contacted.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
