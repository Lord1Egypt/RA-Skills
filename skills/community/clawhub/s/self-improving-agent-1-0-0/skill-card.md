## Description:

Captures learnings, errors, corrections, and feature requests as markdown entries so agents can review recurring lessons and promote broadly useful guidance into project memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dc-acronym](https://clawhub.ai/user/dc-acronym)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to log command failures, user corrections, knowledge gaps, API or tool failures, and missing capabilities into project-local markdown files. Teams can then review, resolve, or promote recurring lessons into CLAUDE.md or AGENTS.md.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist conversation, command, and error details into project-local learning files.

Mitigation: Require user confirmation before file writes and keep .learnings local unless the team intentionally decides to share it.

Risk: Logged entries may contain secrets, personal data, or sensitive project details.

Mitigation: Redact secrets and personal data before saving or sharing learning files.

Risk: Promoted learnings can alter persistent agent guidance in CLAUDE.md or AGENTS.md.

Mitigation: Review proposed memory-file changes as diffs before accepting them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dc-acronym/skills/self-improving-agent-1-0-0)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and reusable entry templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces project-local learning, error, and feature-request entries under .learnings/ and may suggest updates to CLAUDE.md or AGENTS.md.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
