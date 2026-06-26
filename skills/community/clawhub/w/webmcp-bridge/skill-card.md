## Description: <br>
Connect a website to the local-mcp browser bridge through a fixed UXC link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create or refresh per-site local-mcp browser bridge links, inspect bridge and site tools, manage browser session mode, and recover sessions when only bridge tools are visible. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation may act on logged-in websites and perform posting, deletion, purchase, or account-changing actions. <br>
Mitigation: Confirm explicit user intent before destructive or account-changing website actions and inspect tool help before calling site operations. <br>
Risk: Untrusted bridge packages, adapter modules, or command overrides could execute unexpected local code. <br>
Mitigation: Install only trusted versions of the WebMCP bridge package, uxc, npx, and configured adapters; avoid untrusted WEBMCP_LOCAL_MCP_COMMAND and adapter values. <br>
Risk: Reusing one browser profile across unrelated sites can mix credentials or session state. <br>
Mitigation: Use one profile per site with the documented ~/.uxc/webmcp-profile/<site> layout. <br>


## Reference(s): <br>
- [Webmcp Bridge ClawHub Page](https://clawhub.ai/jolestar/webmcp-bridge) <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [Source Modes](references/source-modes.md) <br>
- [Link Patterns](references/link-patterns.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON command payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational guidance for UXC links, browser profiles, session mode changes, and bridge recovery steps.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
