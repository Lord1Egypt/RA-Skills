## Description:

ZugaShield Security Scanner is an OpenClaw plugin that scans messages, tool calls, responses, and memory for prompt injection, SSRF, command injection, data leakage, and memory poisoning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuga-luga](https://clawhub.ai/user/zuga-luga)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to add gateway-level security scanning to OpenClaw deployments before requests, tool calls, responses, and memory recalls reach or leave the agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The plugin installs and runs an external Python scanner engine that can receive OpenClaw messages, tool calls, responses, and memory content.

Mitigation: Pin exact npm and PyPI versions, verify the Python scanner package provenance, and run it under a low-privilege, sandboxed account.

Risk: If the scanner is unavailable, protection for non-tool traffic depends on fail-closed configuration.

Mitigation: Keep fail_closed enabled for normal deployments, monitor /shield status after startup and updates, and treat disconnected scanner status as an operational incident.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zuga-luga/skills/zugashield)
- [ZugaShield GitHub Homepage](https://github.com/Zuga-luga/ZugaShield)
- [ZugaShield OpenClaw Plugin on npm](https://www.npmjs.com/package/zugashield-openclaw-plugin)
- [ZugaShield on PyPI](https://pypi.org/project/zugashield/)
- [OpenClaw Project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown with shell and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May block unsafe requests or tool calls before execution depending on scanner verdict and configuration.]

## Skill Version(s):

0.1.1 (source: server release metadata, package.json, openclaw.plugin.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
