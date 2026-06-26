## Description: <br>
Cross-session memory sync protocol. Ensures memory consistency across Feishu, webchat, and any other channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdt328606](https://clawhub.ai/user/sdt328606) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to keep task context, recent decisions, and long-term memory synchronized across Feishu, webchat, and new sessions by reading and updating shared memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can copy recent conversation history into shared long-term memory files, which may expose sensitive or channel-specific information. <br>
Mitigation: Use explicit opt-in commands, review memory changes before writing, and define rules that prevent secrets, personal data, or confidential channel content from being persisted. <br>
Risk: The cleanup script archives daily memory logs older than seven days, which can move records before useful details have been summarized. <br>
Mitigation: Review daily logs and extract durable information into MEMORY.md before running cleanup or enabling startup cleanup behavior. <br>


## Reference(s): <br>
- [Session Sync on ClawHub](https://clawhub.ai/sdt328606/stitch-session-sync) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with inline file paths and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read recent session history and write or archive shared memory files when used as directed.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
