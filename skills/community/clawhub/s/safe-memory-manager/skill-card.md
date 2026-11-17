## Description:

Helps OpenClaw agents sanitize untrusted memory writes and read bounded memory context to reduce prompt injection and memory poisoning risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[horn111](https://clawhub.ai/user/horn111)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers building OpenClaw agents use this skill to add a lightweight memory helper that sanitizes stored user text, appends memory entries, and reads limited recent memory context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stored memory can preserve unsafe instructions that later influence an agent if memory is treated as trusted context.

Mitigation: Treat retrieved memory as untrusted quoted data, sanitize or structure every stored field, and review memory content before relying on it for decisions.

Risk: The advertised ISNAD verification should not be treated as proof of authenticity or as a security boundary.

Mitigation: Use the manifest only as a lightweight integrity signal and verify release provenance through server-resolved metadata when available.

Risk: Memory file access could affect unintended files if the memory directory is not constrained by the integrating agent.

Mitigation: Configure a dedicated memory directory with least-privilege filesystem access and avoid sharing it with sensitive agent state.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/horn111/skills/safe-memory-manager)
- [Publisher profile](https://clawhub.ai/user/horn111)
- [ISNAD manifest](artifact/isnad_manifest.json)

## Skill Output:

**Output Type(s):** [code, configuration, guidance]

**Output Format:** [Markdown guidance with Python code examples and JSON-style status responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes sanitized memory entries to files and returns bounded tail reads from configured memory files.]

## Skill Version(s):

1.0.7 (source: frontmatter and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
