## Description:

Install and verify the SafeClaw safety proxy for OpenClaw and other OpenAI-compatible clients, including setup, traffic routing, dashboard debugging, and adaptation for provider configs, agent models.json, or shell-launched clients.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aceteam-ai](https://clawhub.ai/user/aceteam-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to set up a local or hosted SafeClaw proxy, route OpenClaw or OpenAI-compatible client traffic through it, and verify that traffic appears in the dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has broad setup authority and may directly change OpenClaw, agent model, or shell routing configuration.

Mitigation: Review the identified routing mode and changed files before relying on the setup; keep backups of edited configuration files and confirm whether a restart or new session is required.

Risk: Credentials and model traffic may pass through mutable third-party proxy components.

Mitigation: Use pinned and verified proxy artifacts where possible, avoid production API keys during setup validation, and confirm the proxy endpoint before routing real clients through it.

Risk: Wildcard elevated execution could grant more authority than the setup requires.

Mitigation: Do not enable wildcard elevated execution by default; scope elevated permissions to the active provider and only for commands needed to start or verify the proxy.

## Reference(s):

- [Safeclaw Proxy ClawHub listing](https://clawhub.ai/aceteam-ai/skills/safeclaw-proxy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include the proxy URL, dashboard URL, configured routing path, safety test result, dashboard call status, files changed, and restart requirements.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
