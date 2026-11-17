## Description:

Access and manage a persistent knowledge graph for storing, retrieving, linking, and summarizing facts, decisions, goals, and observations across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atmsamma](https://clawhub.ai/user/atmsamma)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to retain and retrieve project memory across sessions, including facts, decisions, goals, observations, relationships, and contradiction-resolution notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guidance encourages storing credentials in long-lived memory without safeguards.

Mitigation: Revise usage guidance so agents never store passwords, API keys, access tokens, private keys, session cookies, recovery codes, or other secrets; store only non-sensitive summaries or references to a separate secret manager.

Risk: Persistent memory can expose sensitive project context if isolation and deletion controls are unclear.

Mitigation: Use only with a memory backend that provides clear user and project isolation, deletion controls, and policies restricting storage to non-sensitive content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/atmsamma/skills/thecede)

## Skill Output:

**Output Type(s):** [guidance, markdown, API calls]

**Output Format:** [Markdown guidance with structured tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
