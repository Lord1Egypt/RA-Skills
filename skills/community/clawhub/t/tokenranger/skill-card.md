## Description:

Install, configure, and operate the TokenRanger OpenClaw plugin. Use when you want to reduce cloud LLM token costs by 50-80% via local Ollama context compression, or when diagnosing TokenRanger sidecar issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[synchronic1](https://clawhub.ai/user/synchronic1)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to install, configure, upgrade, uninstall, and troubleshoot the TokenRanger OpenClaw plugin for local context compression with Ollama.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and updates third-party components that may run as a persistent local service and process conversation history.

Mitigation: Use pinned versions, inspect the plugin repository and generated service file before setup, and install only when that local processing model is acceptable.

Risk: The local sidecar service could expose conversation processing beyond the intended local host boundary if configured incorrectly.

Mitigation: Confirm the service binds only to localhost unless remote access is intended, and review uninstall steps so the background service can be disabled later.

## Reference(s):

- [TokenRanger ClawHub Skill Page](https://clawhub.ai/synchronic1/skills/tokenranger)
- [TokenRanger Plugin Repository](https://github.com/peterjohannmedina/openclaw-plugin-tokenranger)
- [openclaw-plugin-tokenranger npm Package](https://www.npmjs.com/package/openclaw-plugin-tokenranger)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include install, setup, status, upgrade, uninstall, and troubleshooting commands.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
