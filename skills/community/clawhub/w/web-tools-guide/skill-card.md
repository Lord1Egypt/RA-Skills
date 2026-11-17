## Description:

Guides agents in choosing web_search, web_fetch, OpenCLI, or browser automation for web research, including fallback behavior, search API configuration, and site-specific login references.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fmls](https://clawhub.ai/user/fmls)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to select an appropriate web access path, recover from web search or fetch failures, configure search provider keys when needed, and use OpenCLI or browser automation with explicit user confirmation for login or sensitive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path can download OpenCLI code and a browser extension from external sources.

Mitigation: Install only after confirming trust in the OpenCLI npm package and GitHub release source.

Risk: The OpenCLI setup script can change browser state by loading an extension and restarting Chrome.

Mitigation: Run setup only in an environment where browser extension loading and browser restarts are acceptable.

Risk: Search API keys may be exposed if pasted into chat or surfaced in logs, process arguments, or configuration output.

Mitigation: Prefer local secret setup outside chat and rotate any key already shared through the agent conversation.

## Reference(s):

- [OpenCLI Usage Guide](artifact/references/opencli-guide.md)
- [Web Search API Configuration](artifact/references/web-search-config.md)
- [Well-Known Sites Index](artifact/references/well-known-sites.json)
- [OpenCLI GitHub Releases](https://github.com/jackwener/opencli/releases)
- [ClawHub Skill Page](https://clawhub.ai/fmls/skills/web-tools-guide)
- [Publisher Profile](https://clawhub.ai/user/fmls)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown, json]

**Output Format:** [Markdown guidance with inline shell commands and JSON reference data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes fallback decision guidance for web tools and setup instructions for OpenCLI.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
