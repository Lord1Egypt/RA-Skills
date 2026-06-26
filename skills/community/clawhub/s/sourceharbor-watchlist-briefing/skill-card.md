## Description: <br>
Use SourceHarbor watchlists, briefings, Ask, MCP, and HTTP API to answer one question with current story context and evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaojiou176](https://clawhub.ai/user/xiaojiou176) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and external users use this skill to inspect one SourceHarbor watchlist, reuse the current briefing or story payload, and answer one operator question with evidence and a concrete next action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use an external SourceHarbor MCP server or local HTTP API, so an untrusted setup could return misleading briefing evidence. <br>
Mitigation: Install only with a trusted SourceHarbor MCP/API setup, review the external SourceHarbor repository before running its MCP server, and keep the API base URL pointed at a trusted local endpoint. <br>
Risk: Optional report-send or workflow-run capabilities may affect operator workflows if used without review. <br>
Mitigation: Require explicit user approval before any report is sent or workflow is run. <br>


## Reference(s): <br>
- [SourceHarbor Watchlist Briefing ClawHub Listing](https://clawhub.ai/xiaojiou176/sourceharbor-watchlist-briefing) <br>
- [SourceHarbor Capability Map](references/CAPABILITIES.md) <br>
- [SourceHarbor MCP And HTTP Setup](references/INSTALL.md) <br>
- [OpenHands MCP Config](references/OPENHANDS_MCP_CONFIG.json) <br>
- [OpenClaw MCP Config](references/OPENCLAW_MCP_CONFIG.json) <br>
- [SourceHarbor HTTP Fallback](references/http-fallback.md) <br>
- [Example Output](references/example-output.md) <br>
- [SourceHarbor Troubleshooting](references/TROUBLESHOOTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown briefing with structured fields and optional shell commands or API calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes current_story, what_changed, evidence_used, suggested_next_action, and runtime_gap when access is partial.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata and manifest.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
