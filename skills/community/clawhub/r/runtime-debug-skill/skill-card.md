## Description: <br>
Diagnose and fix bugs using runtime execution traces. Use when debugging errors, analyzing failures, or finding root causes in Python, Node.js, or Java applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dxsup](https://clawhub.ai/user/dxsup) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to instrument Python, Node.js, and Java applications, reproduce bugs, inspect runtime traces, identify root causes, apply fixes, and remove instrumentation after debugging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make broad project changes, including dependency, instrumentation, and configuration edits. <br>
Mitigation: Use a disposable branch or non-sensitive development environment and review every dependency, installer, source edit, and configuration change before running it. <br>
Risk: API keys, generated instrumentation, .syncause files, or runtime traces may expose sensitive data. <br>
Mitigation: Do not commit secrets or generated debugging files, treat traces as sensitive, and remove SDK hooks, MCP entries, credentials, and generated files after debugging. <br>
Risk: Remote installers and external trace collection are part of the debugging workflow. <br>
Mitigation: Review installers and dependency sources before execution and limit use to projects where external trace collection is acceptable. <br>


## Reference(s): <br>
- [Runtime Debug Skill release page](https://clawhub.ai/dxsup/runtime-debug-skill) <br>
- [MCP Server Installation - Anonymous Mode](references/install/mcp-install-anonymous.md) <br>
- [MCP Server Installation - Login Mode](references/install/mcp-install-login.md) <br>
- [Syncause Python SDK Installation Guide](references/install/python.md) <br>
- [Syncause Node.js SDK Installation Guide](references/install/nodejs.md) <br>
- [Syncause Java SDK Installation Guide](references/install/java.md) <br>
- [Syncause Python SDK Uninstallation Guide](references/uninstall/python.md) <br>
- [Syncause Node.js SDK Uninstallation Guide](references/uninstall/nodejs.md) <br>
- [Syncause Java SDK Uninstallation Guide](references/uninstall/java.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code, shell commands, configuration snippets, and proposed source edits] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include project instrumentation steps, runtime trace analysis, reproduction scripts, code changes, verification results, and teardown instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
