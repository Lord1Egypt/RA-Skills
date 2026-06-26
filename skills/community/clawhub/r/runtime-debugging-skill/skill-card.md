## Description: <br>
Diagnose and fix bugs using runtime execution traces. Use when debugging errors, analyzing failures, or finding root causes in Python, Node.js, or Java applications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dxsup](https://clawhub.ai/user/dxsup) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to instrument Python, Node.js, or Java applications with Syncause runtime tracing, reproduce bugs, inspect live trace data, and apply verified fixes with cleanup afterward. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs remote SDKs or MCP components and changes application startup or build behavior. <br>
Mitigation: Review installers and dependency changes before execution, pin versions where possible, and verify all startup hooks and build changes during teardown. <br>
Risk: Runtime traces and API keys may expose secrets or sensitive project data outside the local machine. <br>
Mitigation: Keep API keys out of committed files, redact secrets before tracing, and use the skill only where outbound trace collection is approved. <br>
Risk: Incomplete cleanup can leave tracing dependencies, configuration, or .syncause files in the project. <br>
Mitigation: Follow the language-specific uninstall guides and confirm dependencies, MCP configuration, startup hooks, and .syncause files are removed. <br>


## Reference(s): <br>
- [Syncause Java SDK Installation Guide](artifact/references/install/java.md) <br>
- [Syncause Node.js SDK Installation Guide](artifact/references/install/nodejs.md) <br>
- [Syncause Python SDK Installation Guide](artifact/references/install/python.md) <br>
- [MCP Server Installation - Anonymous Mode](artifact/references/install/mcp-install-anonymous.md) <br>
- [MCP Server Installation - Login Mode](artifact/references/install/mcp-install-login.md) <br>
- [Syncause Java SDK Uninstallation Guide](artifact/references/uninstall/java.md) <br>
- [Syncause Node.js SDK Uninstallation Guide](artifact/references/uninstall/nodejs.md) <br>
- [Syncause Python SDK Uninstallation Guide](artifact/references/uninstall/python.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with code edits, shell commands, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup, trace analysis, fix summary, and teardown guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
