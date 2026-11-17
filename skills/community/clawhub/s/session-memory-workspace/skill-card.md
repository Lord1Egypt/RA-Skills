## Description:

Write session summaries to daily memory files and search session history so OpenClaw can recall and cite past conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[breezezephyr](https://clawhub.ai/user/breezezephyr)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to summarize dated chat sessions into workspace memory and search past session transcripts by keyword or date range.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads private OpenClaw session logs and may persist sensitive or near-verbatim chat content into long-term workspace memory.

Mitigation: Use it only on sessions that are appropriate for persistent memory, then review, edit, or delete generated memory/YYYY-MM-DD.md files that contain secrets, personal data, or misleading instructions.

Risk: Generated session summaries can carry incorrect, outdated, or unwanted conversational context into future memory-backed replies.

Mitigation: Review the generated daily memory file before relying on it, and remove stale or inaccurate excerpts from the Session summary section.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/breezezephyr/skills/session-memory-workspace)
- [Artifact README](artifact/README.md)
- [Artifact skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [markdown, json, shell commands, guidance]

**Output Format:** [Markdown memory files, JSON search results, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and local OpenClaw session logs; summaries are written to memory/YYYY-MM-DD.md and search results are emitted as JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, README.md, and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
