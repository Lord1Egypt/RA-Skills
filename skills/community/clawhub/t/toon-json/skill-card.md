## Description:

Compress, encode, and decode large JSON payloads into a compact, reversible TOON string to reduce token usage in LLM prompts and tool payloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmkkevin](https://clawhub.ai/user/zmkkevin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to convert large JSON payloads into compact TOON text for prompts or tool payloads, then decode the result back to JSON when round-trip fidelity is needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TOON output contains the same sensitive information as the original JSON and may be pasted into prompts or tool payloads.

Mitigation: Avoid encoding secrets or private data unless that content is intended for the destination prompt or tool.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zmkkevin/skills/toon-json)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands]

**Output Format:** [TOON string or JSON emitted by a local command-line script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Schema mode can embed a key dictionary; encoded output preserves the information contained in the original JSON.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
