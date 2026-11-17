## Description:

Captures learnings, errors, and corrections to enable continuous improvement for coding agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tigertamvip](https://clawhub.ai/user/tigertamvip)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to record failures, corrections, knowledge gaps, and feature requests in structured learning logs so future agent work can reuse or promote the learning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent learning logs or shared transcripts may capture sensitive project context or personal data.

Mitigation: Use the skill only where persistent logs are acceptable, redact secrets and unnecessary transcript content, and avoid storing full conversations.

Risk: Promoting learnings into future agent instruction files can preserve incorrect or unsafe guidance.

Mitigation: Require human review before adding or updating agent memory and instruction files.

Risk: Optional hooks and inter-session sharing can change agent behavior beyond a single task.

Mitigation: Enable hooks or transcript-sharing workflows only after reviewing the referenced scripts and confirming that behavior is desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tigertamvip/skills/self-improving-agent-5)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces structured learning-log entries and setup guidance for agent memory files.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
