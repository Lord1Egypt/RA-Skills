## Description:

Quantum Memory Graph provides quantum-enhanced long-term memory for AI agents using chunked gte-large retrieval and optional QAOA+CVaR graph optimization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dustin-a11y](https://clawhub.ai/user/dustin-a11y)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add persistent semantic memory, recall endpoints, and graph-based retrieval guidance to AI agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and run a persistent memory service with network endpoints.

Mitigation: Use a pinned and verified package version, run it in an isolated environment, and keep the service private or authenticated.

Risk: Persistent memory can retain secrets, sensitive conversations, or regulated data.

Mitigation: Avoid storing sensitive data unless retention, deletion, access control, and encryption are clearly handled.

Risk: Security evidence rates the release as suspicious because the service has little security guidance.

Mitigation: Review the skill carefully before installation and scan the package and deployment configuration before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dustin-a11y/skills/quantum-memory)
- [Project GitHub repository](https://github.com/Dustin-a11y/quantum-memory-graph)
- [PyPI package](https://pypi.org/project/quantum-memory-graph/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include package installation commands, local service commands, API endpoint guidance, and memory retrieval examples.]

## Skill Version(s):

1.2.0 (source: release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
