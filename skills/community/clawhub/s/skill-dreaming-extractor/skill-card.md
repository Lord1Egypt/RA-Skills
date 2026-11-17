## Description:

Daily fact extraction from AI agent session history into a persistent learned.md memory file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to turn prior OpenClaw agent sessions into a persistent memory file of structured facts for later recall.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads broad historical agent conversations and can retain sensitive or unwanted details in persistent memory.

Mitigation: Restrict collection to intended agents or directories, review and redact extraction inputs, and require approval before appending facts to learned.md.

Risk: The daily cost cap is advisory until the budget workflow is hardened.

Mitigation: Monitor budget status and logs during initial use, keep a low daily cap, and stop scheduled runs if spend tracking is inconsistent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zero2ai-hub/skills/skill-dreaming-extractor)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and plain text with JSON-shaped fact extraction guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces extraction input under memory/.dreams and appends dated facts with confidence scores and source citations to memory/learned.md.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
