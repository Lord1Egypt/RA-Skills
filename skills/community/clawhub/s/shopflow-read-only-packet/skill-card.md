## Description: <br>
Guides agents through installing, attaching, and using Shopflow's local read-only MCP packet surface for submission-readiness checks without live store claims. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaojiou176](https://clawhub.ai/user/xiaojiou176) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to attach a local Shopflow stdio MCP server and inspect read-only integration, readiness, runtime, and distribution-truth packets. It helps agents separate repo-ready evidence from unsupported live listing, store, or hosted-runtime claims. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Repo-local command guidance can run package-manager scripts or MCP server commands. <br>
Mitigation: Review the exact command, working directory, and target repository before approving execution. <br>
Risk: Authenticated ClawHub or GitHub workflows may publish or moderate content if misapplied. <br>
Mitigation: Require explicit operator approval for publishing, moderation, or registry actions and verify the target before execution. <br>
Risk: The packet can be overstated as a live public listing or hosted runtime. <br>
Mitigation: Keep responses limited to read-only packet evidence and require fresh receipts before claiming ClawHub, OpenHands, registry, store, or hosted-runtime status. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaojiou176/shopflow-read-only-packet) <br>
- [Artifact README](README.md) <br>
- [Skill instructions](SKILL.md) <br>
- [Install and attach guide](references/INSTALL.md) <br>
- [Capability map](references/CAPABILITIES.md) <br>
- [First-success demo](references/DEMO.md) <br>
- [OpenHands MCP config](references/OPENHANDS_MCP_CONFIG.json) <br>
- [OpenClaw MCP config](references/OPENCLAW_MCP_CONFIG.json) <br>
- [Troubleshooting](references/TROUBLESHOOTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only MCP packet guidance; no live store or hosted-runtime claims.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and manifest.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
