## Description: <br>
Enables AI agents to adopt a consistent persona, remember user relationships, and express opinions beyond generic assistant responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xhrisfu](https://clawhub.ai/user/xhrisfu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent builders use this skill to shape an agent's persona, relationship memory, and response style using SOUL.md, USER.md, and MEMORY.md conventions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reshape an agent's persona and response style in strongly opinionated ways. <br>
Mitigation: Review the persona instructions before installation and confirm that the resulting tone and behavior are appropriate for the intended environment. <br>
Risk: The skill encourages persistent subjective notes about the user in memory files. <br>
Mitigation: Require explicit opt-in for memory writes, store only task-relevant non-sensitive information, and keep USER.md and MEMORY.md easy to inspect, edit, and delete. <br>


## Reference(s): <br>
- [Soul Framework on ClawHub](https://clawhub.ai/xhrisfu/soul-framework) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with file naming conventions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to read and update SOUL.md, USER.md, and MEMORY.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
