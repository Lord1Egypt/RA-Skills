## Description: <br>
Guide to install, connect, and use Switchyard's read-only MCP runtime diagnostics for analyzing provider or runtime boundaries safely. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaojiou176](https://clawhub.ai/user/xiaojiou176) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to attach a local Switchyard MCP server and run read-only runtime, provider, and catalog diagnostics before taking human-directed action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to clone and run an external Switchyard repository with pnpm scripts. <br>
Mitigation: Review the referenced repository and pnpm scripts before installation, then run them from the intended local clone only. <br>
Risk: Host configuration snippets contain a placeholder working directory. <br>
Mitigation: Replace the placeholder cwd with the exact local Switchyard clone path before starting the MCP server. <br>
Risk: Diagnostics can overstate support or live readiness if read-only, partial signals are treated as complete proof. <br>
Mitigation: Use only the documented read-only tools and avoid supported, live-ready, package-published, or registry-listed claims without fresh evidence. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiaojiou176/switchyard-runtime-diagnostics) <br>
- [Install And Attach Switchyard MCP](references/INSTALL.md) <br>
- [Switchyard MCP Capabilities](references/CAPABILITIES.md) <br>
- [Switchyard MCP First-Success Demo](references/DEMO.md) <br>
- [Switchyard MCP Troubleshooting](references/TROUBLESHOOTING.md) <br>
- [OpenHands MCP Config](references/OPENHANDS_MCP_CONFIG.json) <br>
- [OpenClaw MCP Config](references/OPENCLAW_MCP_CONFIG.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only diagnostic posture; outputs should keep readiness claims partial and evidence-grounded.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and manifest.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
