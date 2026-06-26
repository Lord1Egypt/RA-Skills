## Description: <br>
Use this skill when you need to find code in a local checkout or Git source by behavior, intent, symbol, file path, related implementation, or indexed chunk context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tristanmanchester](https://clawhub.ai/user/tristanmanchester) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to search local codebases or Git sources before broad file reads, especially for implementation discovery, behavior tracing, symbol lookup, and related-code inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a local sifs executable, so searches may fail or return no contract if the binary is missing or not on PATH. <br>
Mitigation: Run scripts/check-setup.sh or check command -v sifs and sifs --version before relying on the workflow. <br>
Risk: Searches can target the wrong checkout when the agent is not running from the intended project directory. <br>
Mitigation: Pass --source <project> for searches, file listing, chunk inspection, and related-code lookup. <br>
Risk: MCP tools may be configured but invisible or unavailable in the active agent session. <br>
Mitigation: Use the CLI immediately when MCP tools are missing or failing, and run the documented doctor commands when troubleshooting is needed. <br>
Risk: Security evidence advises installation only in trusted ClawHub or Convex development environments. <br>
Mitigation: Install and run the skill only in trusted environments, and follow local approval practices before installing missing tools. <br>


## Reference(s): <br>
- [SIFS Search skill page](https://clawhub.ai/tristanmanchester/sifs-search) <br>
- [tristanmanchester publisher profile](https://clawhub.ai/user/tristanmanchester) <br>
- [SIFS Command Recipes](references/commands.md) <br>
- [SIFS MCP Rules](references/mcp.md) <br>
- [SIFS Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the local sifs binary on PATH; MCP tools are optional and the CLI is the fallback path.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata and OpenClaw metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
