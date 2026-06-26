## Description: <br>
Captures learnings, errors, corrections, and feature requests in structured markdown logs so agents can improve future work and reduce repeated mistakes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dc-acronym](https://clawhub.ai/user/dc-acronym) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to capture corrections, command failures, missing capabilities, knowledge gaps, and recurring best practices as structured project learning records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent learning logs can capture conversation-derived secrets, personal data, confidential information, or incorrect guidance. <br>
Mitigation: Require confirmation before logging conversation-derived content, redact sensitive data, and review entries before sharing or committing them. <br>
Risk: Promoting learnings into durable agent memory can preserve misleading or overbroad instructions. <br>
Mitigation: Manually review proposed changes to CLAUDE.md or AGENTS.md before applying them. <br>


## Reference(s): <br>
- [ClawHub skill release page](https://clawhub.ai/dc-acronym/self-improving-agent-1-0-0) <br>
- [LEARNINGS.md](artifact/LEARNINGS.md) <br>
- [examples.md](artifact/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates .learnings markdown logs and may propose reviewed updates to persistent agent memory files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
