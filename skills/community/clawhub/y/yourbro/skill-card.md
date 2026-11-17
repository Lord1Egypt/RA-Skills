## Description:

Publish AI-powered web pages with end-to-end encryption on yourbro.ai.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mehanig](https://clawhub.ai/user/mehanig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to publish, update, share, and manage multi-file web pages through local page directories served by a paired yourbro-agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and run a native yourbro-agent binary that can change over time.

Mitigation: Use pinned agent versions with published checksums or signatures before running the binary.

Risk: The local agent requires access to a yourbro token, local page files, and a persistent SQLite database.

Mitigation: Run the agent with only the environment variables and filesystem access needed for the intended page directories.

Risk: The release security verdict is suspicious because the native agent is unverified.

Mitigation: Review the service design and binary source before installation, especially for sensitive or commercial page content.

## Reference(s):

- [yourbro homepage](https://yourbro.ai)
- [macOS Apple Silicon agent download](https://yourbro.ai/releases/latest/yourbro-agent-darwin-arm64)
- [macOS Intel agent download](https://yourbro.ai/releases/latest/yourbro-agent-darwin-amd64)
- [Linux x86_64 agent download](https://yourbro.ai/releases/latest/yourbro-agent-linux-amd64)
- [Linux ARM64 agent download](https://yourbro.ai/releases/latest/yourbro-agent-linux-arm64)
- [ClawHub skill page](https://clawhub.ai/mehanig/skills/yourbro)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline JSON, shell, HTML, CSS, and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local page files, optional page.json metadata, and shareable page URLs for a running yourbro-agent.]

## Skill Version(s):

0.0.11 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
