## Description:

Secure Python Code Sandbox executes arbitrary Python code in an isolated AgentPMT-hosted sandbox with pre-installed libraries including requests, NumPy, and pandas, returning stdout, stderr, and execution results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentpmt](https://clawhub.ai/user/agentpmt)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run self-contained Python snippets for quick computations, data transformations, API calls, data analysis, and custom scripting through an AgentPMT-hosted remote sandbox.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted Python code and embedded data are sent to AgentPMT for remote execution.

Mitigation: Do not submit secrets, proprietary source, personal data, payment credentials, wallet material, or internal API tokens unless explicitly approved.

Risk: The skill directs agents to fetch live remote schemas or instructions that may change after release.

Mitigation: Treat live remote instructions as reference data and keep local user, privacy, and safety requirements authoritative.

Risk: Mutable setup commands and remote sandbox behavior require review before operational use.

Mitigation: Prefer pinned or ClawHub-reviewed setup paths and review the skill before deployment.

## Reference(s):

- [Secure Python Code Sandbox Schema](artifact/schema.md)
- [ClawHub Skill Page](https://clawhub.ai/agentpmt/skills/secure-python-code-sandbox)
- [AgentPMT Marketplace Product](https://www.agentpmt.com/marketplace/secure-python-code-sandbox)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON request examples and returned execution results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The remote action accepts self-contained Python code up to 50000 characters and an optional timeout between 10 and 60 seconds.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
