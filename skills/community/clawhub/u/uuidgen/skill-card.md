## Description:

Generates UUID v4 values and short identifiers, validates UUID strings, extracts UUIDs from text, and produces batches of UUIDs for developer workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ckchzh](https://clawhub.ai/user/ckchzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate database keys, session or batch identifiers, unique filenames, and log/search identifiers, and to validate or extract UUIDs while working in an agent-assisted shell workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill description advertises nano ID generation, but the artifact implements UUID v4 generation, batch generation, validation, extraction, and 8-character short IDs only.

Mitigation: Treat nano ID generation as unsupported for this release and use the implemented UUID and short-ID commands instead.

Risk: The 8-character short IDs are lightweight identifiers and are not appropriate as strong security tokens.

Mitigation: Use full UUID v4 values or a dedicated secret-generation tool when a token needs strong security properties.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ckchzh/skills/uuidgen)
- [BytesAgain homepage](https://bytesagain.com)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and terminal-style text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce UUID v4 values, batches up to 1000 UUIDs, validation details, extracted UUID lists, and 8-character short IDs.]

## Skill Version(s):

3.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
