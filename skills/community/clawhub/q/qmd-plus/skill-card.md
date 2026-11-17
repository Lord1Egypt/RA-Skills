## Description:

QMD Plus enhances QMD search for local Markdown knowledge bases with LLM-powered query expansion to improve recall and precision for multilingual note and document lookup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thehappyboy](https://clawhub.ai/user/thehappyboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and knowledge-base users use this skill to search local Markdown collections through QMD with LLM-assisted query expansion for better multilingual recall and precision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Markdown collections and search queries may contain private or sensitive information, and LLM expansion can expose query text to an external provider.

Mitigation: Use a dedicated non-sensitive QMD collection and avoid secrets, credentials, private data, or confidential collection names in queries sent for LLM expansion.

Risk: Broad command and MCP permissions, optional npx usage, and placeholder LLM commands can increase execution and data-access risk if installed carelessly.

Mitigation: Pin reviewed package versions, restrict MCP access to intended collections, and remove broad npx or placeholder LLM command permissions unless they are explicitly required.

## Reference(s):

- [QMD MCP Server Setup](references/mcp-setup.md)
- [QMD Plus on ClawHub](https://clawhub.ai/thehappyboy/skills/qmd-plus)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local QMD queries, LLM expansion prompts, MCP setup guidance, and search workflow instructions.]

## Skill Version(s):

1.0.1 (source: server release; artifact frontmatter metadata says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
