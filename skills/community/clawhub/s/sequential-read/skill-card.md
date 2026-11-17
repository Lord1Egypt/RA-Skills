## Description:

Read prose sequentially with structured reflections to simulate the reading experience

This skill is ready for commercial/non-commercial use.

## Publisher:

[horace-claw](https://clawhub.ai/user/horace-claw)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and reading-focused agents use this skill to read long prose one chunk at a time, capture interim reflections, and produce a final synthesis that preserves the reading arc.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous sub-agents process untrusted source text, which can expose the reading workflow to adversarial document content.

Mitigation: Review the skill before installation for private or adversarial documents and run it with filesystem access limited to the chosen source file and its session directory.

Risk: Source-derived chunks and generated reactions are written to persistent workspace memory.

Mitigation: Use the skill only for documents the user is allowed to process, and review or delete the session directory after use when handling sensitive material.

Risk: Longer-lived reader context may be updated from a source document and later reused.

Mitigation: Review any retained reader context before reuse, especially after processing private or adversarial texts.

## Reference(s):

- [Sequential Read ClawHub Listing](https://clawhub.ai/horace-claw/skills/sequential-read)
- [Agentic Sequential Reading](https://doi.org/10.5281/zenodo.18596456)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown synthesis plus session files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores chunk reflections and the final synthesis under memory/sequential_read/<session-id>/.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
