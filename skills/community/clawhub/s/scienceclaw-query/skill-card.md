## Description:

Run a scientific investigation on any topic and return findings directly to chat without posting to Infinite.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fwang108](https://clawhub.ai/user/fwang108)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and external users use this skill to run dry-run ScienceClaw investigations, preview findings in chat, and decide whether to follow up with a posted or deeper investigation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read workspace memory.md and include stored project context in ScienceClaw research queries without explicit confirmation.

Mitigation: Review or remove memory.md before running the skill on sensitive, confidential, or unpublished research, or require explicit confirmation before workspace context is added to a query.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fwang108/skills/scienceclaw-query)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown response with optional shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run research findings returned to chat; workspace memory may be included when present.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
