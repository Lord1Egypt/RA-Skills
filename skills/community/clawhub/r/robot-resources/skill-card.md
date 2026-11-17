## Description:

Robot Resources helps agents propose setup for local LLM routing and web-content scraping to reduce model API costs and token usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manuelsobrino](https://clawhub.ai/user/manuelsobrino)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill when a human wants lower LLM API costs or compressed web context. It guides human-approved installation and configuration of a local routing proxy and scraper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Future model traffic may be routed through a local proxy that can observe prompts, responses, and provider-key-backed traffic.

Mitigation: Proceed only after the human approves the proxy behavior and trusts the publisher and installer.

Risk: Installation may create persistent local software, register services, or change agent configuration.

Mitigation: Review expected file, service, and configuration changes before installation and confirm how to uninstall or revert them.

Risk: The installation command uses an unpinned npm package.

Mitigation: Verify the package and publisher before running the installer, especially in production or sensitive environments.

## Reference(s):

- [Robot Resources website](https://robotresources.ai)
- [Robot Resources full docs](https://robotresources.ai/llms-full.txt)
- [ClawHub skill page](https://clawhub.ai/manuelsobrino/skills/robot-resources)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, JSON, HTTP, and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces installation and configuration guidance; does not execute the installer by itself.]

## Skill Version(s):

1.0.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
