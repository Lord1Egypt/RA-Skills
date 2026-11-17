## Description:

Diagnose and fix bugs using runtime execution traces. Use when debugging errors, analyzing failures, or finding root causes in Python, Node.js, or Java applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dxsup](https://clawhub.ai/user/dxsup)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to instrument Python, Node.js, or Java applications, reproduce failures, inspect runtime traces, and apply evidence-based fixes. It is intended for debugging crashes, incorrect behavior, and performance issues where live execution context helps identify root cause.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent external debugging tooling may remain active after troubleshooting and affect application performance or data exposure.

Mitigation: Use the included teardown guides after debugging, remove the SDK and generated configuration, delete the .syncause folder, and verify the application runs without instrumentation.

Risk: Runtime traces can capture request data, return values, database queries, or other sensitive execution context.

Mitigation: Trace only synthetic or approved non-sensitive data unless explicit approval and redaction controls are in place.

Risk: Installation steps may introduce unpinned or remotely fetched tooling and credential-bearing configuration.

Mitigation: Prefer project-scoped MCP configuration, pin package versions, avoid curl-piped shell execution, and keep API keys out of committed files.

## Reference(s):

- [Skill Source](artifact/SKILL.md)
- [MCP Server Installation - Anonymous Mode](artifact/references/install/mcp-install-anonymous.md)
- [MCP Server Installation - Login Mode](artifact/references/install/mcp-install-login.md)
- [Syncause Python SDK Installation Guide](artifact/references/install/python.md)
- [Syncause Node.js SDK Installation Guide](artifact/references/install/nodejs.md)
- [Syncause JAVA SDK Installation Guide](artifact/references/install/java.md)
- [Syncause Python SDK Uninstallation Guide](artifact/references/uninstall/python.md)
- [Syncause Node.js SDK Uninstallation Guide](artifact/references/uninstall/nodejs.md)
- [Syncause JAVA SDK Uninstallation Guide](artifact/references/uninstall/java.md)
- [ClawHub Skill Page](https://clawhub.ai/dxsup/skills/runtime-debugging-skill)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, markdown]

**Output Format:** [Markdown guidance with inline code snippets, shell commands, configuration examples, and debugging summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose dependency, instrumentation, reproduction-test, application-code, and cleanup changes during debugging workflows.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
