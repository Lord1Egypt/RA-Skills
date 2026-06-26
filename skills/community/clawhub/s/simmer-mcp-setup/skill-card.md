## Description: <br>
One-shot bootstrap for the Simmer MCP server that detects an agent runtime, installs simmer-mcp with npm, writes MCP configuration, prompts a restart, and verifies the tool handshake. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simmer](https://clawhub.ai/user/simmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect MCP-aware runtimes such as Claude Code, Cursor, OpenClaw, Hermes, or Codex to Simmer trading tools after registering a Simmer agent and obtaining an API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires storing SIMMER_API_KEY for the MCP subprocess. <br>
Mitigation: Treat SIMMER_API_KEY as a sensitive credential, review the MCP config before restart, and avoid shell or clipboard patterns that could capture the wrong value. <br>
Risk: Configured Simmer tools can access trading workflows, including real venues when live-trading controls are deliberately enabled. <br>
Mitigation: Keep paper trading on the sim venue by default and enable live trading only after confirming dry_run, trading_venue, SIMMER_MCP_ALLOW_LIVE, and any required wallet controls. <br>
Risk: The setup can install or fetch an npm package and modify MCP runtime configuration. <br>
Mitigation: Review npm commands and configuration changes before applying them, and use the documented npx or permission-safe npm path instead of privileged installs. <br>


## Reference(s): <br>
- [Simmer MCP Setup on ClawHub](https://clawhub.ai/simmer/simmer-mcp-setup) <br>
- [simmer-mcp npm package](https://www.npmjs.com/package/simmer-mcp) <br>
- [Simmer docs](https://docs.simmer.markets) <br>
- [Simmer dashboard](https://simmer.markets/dashboard) <br>
- [General Simmer SDK skill](https://clawhub.ai/skills/simmer) <br>
- [Simmer wallet setup skill](https://clawhub.ai/skills/simmer-wallet-setup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with bash, JSON, and YAML snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SIMMER_API_KEY and Node.js/npm; may update local MCP configuration after user review.] <br>

## Skill Version(s): <br>
0.1.2 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
