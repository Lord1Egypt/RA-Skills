## Description:

Quick Capture helps an agent save user-provided notes into an Inbox or Journal, creating structured Markdown notes for Inbox entries and raw appended blocks for Journal entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daowuu](https://clawhub.ai/user/daowuu)

### License/Terms of Use:

MIT-0

## Use Case:

Knowledge workers and developers use Quick Capture to save fleeting ideas, source links, observations, and draft knowledge notes into an Elysia-style Markdown vault from an agent conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or append persistent Markdown files in a location derived from installation layout, which may be outside the intended note vault.

Mitigation: Review or change the script before installation so the vault root is explicit, and verify final write paths remain inside that vault.

Risk: Broad trigger phrases such as casual requests to save or remember something may cause the agent to capture and restructure content unexpectedly.

Mitigation: Use explicit destination wording for Inbox or Journal, and confirm ambiguous captures before writing persistent notes.

Risk: Inbox captures are designed to reorganize and enrich content rather than preserve the original text.

Mitigation: Use Journal for verbatim records and review Inbox notes when exact wording or source fidelity matters.

## Reference(s):

- [Quick Capture ClawHub listing](https://clawhub.ai/daowuu/skills/quick-capture)
- [Publisher profile](https://clawhub.ai/user/daowuu)
- [Project homepage](https://github.com/daowuu/elysia)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands]

**Output Format:** [Markdown files with concise text confirmation; JSON when the helper script is invoked directly.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates new Inbox Markdown notes or appends Journal Markdown blocks under year and month folders.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
