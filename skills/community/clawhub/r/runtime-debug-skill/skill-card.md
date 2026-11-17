## Description:

Diagnose and fix bugs using runtime execution traces. Use when debugging errors, analyzing failures, or finding root causes in Python, Node.js, or Java applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dxsup](https://clawhub.ai/user/dxsup)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to collect runtime traces, reproduce failures, inspect execution state, and guide fixes in Python, Node.js, and Java applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs persistent tracing tools and changes application dependencies during debugging.

Mitigation: Use it in non-production environments with test data, review proposed changes before execution, and complete the documented teardown after debugging.

Risk: Installer guidance includes remote package installation and curl-to-bash patterns.

Mitigation: Pin and verify packages, inspect installer contents before running them, and avoid curl-to-bash execution where policy requires audited install steps.

Risk: Instrumentation can send detailed runtime trace data to an external service.

Mitigation: Confirm what trace data leaves the machine, avoid sensitive production data, and keep API keys out of project files.

Risk: The Java installation guide contains repository token material.

Mitigation: Do not copy embedded token values into projects; use approved secrets handling and rotate credentials if exposure is confirmed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dxsup/skills/runtime-debug-skill)
- [Syncause Java SDK Installation Guide](references/install/java.md)
- [Syncause Node.js SDK Installation Guide](references/install/nodejs.md)
- [Syncause Python SDK Installation Guide](references/install/python.md)
- [MCP Server Installation - Anonymous Mode](references/install/mcp-install-anonymous.md)
- [MCP Server Installation - Login Mode](references/install/mcp-install-login.md)
- [Syncause Java SDK Uninstallation Guide](references/uninstall/java.md)
- [Syncause Node.js SDK Uninstallation Guide](references/uninstall/nodejs.md)
- [Syncause Python SDK Uninstallation Guide](references/uninstall/python.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code, shell commands, configuration snippets, and diagnostic guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose project dependency changes, runtime instrumentation setup, reproduction scripts, trace inspection steps, code fixes, and teardown instructions.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
