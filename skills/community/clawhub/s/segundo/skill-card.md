## Description:

CLI tool for capturing and retrieving thoughts as a second brain, storing memories as daily markdown journals with optional semantic search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sorrycc](https://clawhub.ai/user/sorrycc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and individual users use this skill to operate the segundo CLI for capturing notes, searching memories, filtering journal entries, importing and exporting notes, and configuring local or cloud-backed semantic search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal notes may be stored under ~/.segundo or another configured brain path.

Mitigation: Confirm the storage location is acceptable for the sensitivity of the notes before using the skill.

Risk: Using OpenAI embeddings can send note or search data to a cloud provider.

Mitigation: Prefer local Ollama embeddings for sensitive memories, or configure OpenAI embeddings only when cloud processing is acceptable.

Risk: Delete behavior is documented, but recovery behavior is not described in the artifact.

Mitigation: Back up important notes and use delete commands carefully.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sorrycc/skills/segundo)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include optional JSON command output guidance for segundo commands that support --json.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
