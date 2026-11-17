## Description:

Search source code with the sngs sparse n-gram index. Use for fast literal or regex searches, repeated repository searches, machine-readable code-search results, index initialization, incremental Git updates, and search diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[albert-lv](https://clawhub.ai/user/albert-lv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to search repositories for literal strings, regular expressions, symbols, and configuration values, and to retrieve concise or machine-readable results across repeated searches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill involves building and installing a command-line executable in a local bin directory.

Mitigation: Review the source and build instructions, and install only from a trusted copy.

Risk: The security scan did not include a referenced installed file, so its evidence is incomplete.

Mitigation: Review the installed file before running the tool.

## Reference(s):

- [Sparse N-gram Search project homepage](https://github.com/nano-harness/sparse-ngram-search)
- [ClawHub skill release](https://clawhub.ai/albert-lv/skills/sngs-helper)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON or grep-style text search results, with Markdown guidance and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search output can include file paths, match counts, and contextual lines; result freshness depends on index synchronization and caching.]

## Skill Version(s):

1.0.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
