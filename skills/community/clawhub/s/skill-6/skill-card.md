## Description:

AI-powered browser automation using the AIPex Chrome Extension via MCP bridge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[buttercannfly](https://clawhub.ai/user/buttercannfly)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to connect to an AIPex MCP bridge and automate Chrome workflows such as navigation, form interaction, screenshots, tab management, downloads, and browser-assisted testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a browser extension and MCP bridge with broad access to browser tabs, screenshots, form fields, downloads, and editor contents.

Mitigation: Install and use it only in trusted environments, avoid sensitive tabs unless needed, and require explicit user intent before reading editors, entering passwords, capturing screenshots for LLM analysis, or saving downloads.

Risk: The setup examples use unpinned `npx -y aipex-mcp-bridge`, which may fetch whatever bridge version is current at runtime.

Mitigation: Prefer pinning and reviewing a specific bridge package version before deployment.

## Reference(s):

- [AIPex homepage](https://aipex.ai)
- [AIPex Browser Tools Reference](artifact/references/tools-reference.md)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands, code, markdown]

**Output Format:** [Markdown with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to register an MCP bridge and use browser automation tools for tabs, UI interaction, screenshots, downloads, and human intervention.]

## Skill Version(s):

0.1.0 (source: server release metadata); artifact frontmatter reports 1.0.0

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
