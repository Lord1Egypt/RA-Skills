## Description:

Guides an agent through installing and connecting to Shopflow's local read-only MCP server for packet-based submission readiness and distribution checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaojiou176](https://clawhub.ai/user/xiaojiou176)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release operators use this skill to attach a local Shopflow MCP server, inspect read-only capability packets, and separate repo-ready evidence from claims that need a live registry or store receipt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup asks users to install and run external Shopflow code that is not bundled or pinned in the skill artifact.

Mitigation: Pin the exact repository commit, review package scripts and the lockfile, and run the MCP server with minimal filesystem and secret access.

Risk: The attached MCP server could expose tools that differ from the expected read-only packet surface.

Mitigation: Verify the available MCP tools before connecting the server to an agent host and use only the documented read-only packet tools.

Risk: Distribution or store-readiness claims may be overstated if they are not backed by fresh receipts.

Mitigation: Keep responses limited to repo-ready evidence unless a current ClawHub, OpenHands, registry, or store receipt is available.

## Reference(s):

- [Skill packet README](README.md)
- [Install and attach guide](references/INSTALL.md)
- [Shopflow MCP capabilities](references/CAPABILITIES.md)
- [First-success demo](references/DEMO.md)
- [OpenHands MCP config](references/OPENHANDS_MCP_CONFIG.json)
- [OpenClaw MCP config](references/OPENCLAW_MCP_CONFIG.json)
- [Troubleshooting guide](references/TROUBLESHOOTING.md)
- [ClawHub skill page](https://clawhub.ai/xiaojiou176/skills/shopflow-read-only-packet)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only MCP setup and packet review guidance; no live store or registry status is claimed without fresh receipts.]

## Skill Version(s):

1.0.0 (source: server release evidence and manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
