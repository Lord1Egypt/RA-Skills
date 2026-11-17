## Description:

Cross-tool golden rules for an autonomous Scrapfly web agent connected to the Scrapfly MCP server (web_scrape, screenshot, extract, classify_block, the Cloud Browser lifecycle, snapshot/click/fill/type/press/scroll/select/drag, and WebMCP).

This skill is ready for commercial/non-commercial use.

## Publisher:

[scrapfly](https://clawhub.ai/user/scrapfly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to choose and sequence Scrapfly MCP tools for scraping, screenshots, antibot handling, stateful Cloud Browser interaction, WebMCP calls, and alert setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent alerts can create noisy or unintended monitoring behavior if committed without reviewing the rule details.

Mitigation: Preview alerts before creation and require explicit approval for the metric, threshold, project, notification behavior, and expected firing rate before using confirm=true.

Risk: Cloud Browser sessions can continue consuming credits while open.

Mitigation: Use stateless tools when interaction is unnecessary and monitor active Cloud Browser sessions so paid sessions are closed when work is complete.

## Reference(s):

- [Scrapfly MCP endpoint](https://mcp.scrapfly.io/mcp)
- [Scrapfly agent bootstraps](https://github.com/scrapfly/agent-ai)
- [Scrapfly Agent Rules on ClawHub](https://clawhub.ai/scrapfly/skills/scrapfly-agent-rules)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code is bundled; output guides tool selection and sequencing for Scrapfly MCP workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
