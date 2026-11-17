## Description:

A high-performance Agent subsystem for complex multi-agent orchestration. It provides a visual workflow canvas (OASIS) to coordinate OpenClaw agents, automated computer use tasks, and real-time monitoring via a dedicated Web UI. Supports Telegram/QQ bot integrations and Cloudflare Tunnel for secure remote access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[avalon-467](https://clawhub.ai/user/avalon-467)

### License/Terms of Use:


## Use Case:

Developers and external users can use TeamClaw to run an OpenAI-compatible local agent service, coordinate multi-agent OASIS workflows, monitor activity through a Web UI, and connect optional Telegram, QQ, Bark, OpenClaw, and Cloudflare Tunnel integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TeamClaw is a coherent multi-agent orchestration platform, but it grants broad automation and credential-bearing service access with weak scoping that should be reviewed before installation.

Mitigation: Install only if you are comfortable running a powerful local multi-agent service with code execution, persistent memory, stored API keys, and optional public access. Keep it bound to localhost unless you have reviewed the exposed routes, avoid exposing OASIS directly, do not use untrusted callback URLs or external expert API URLs, rotate tokens if exposure is suspected, and prefer running it in a separate low-privilege account or container.

Risk: The skill can expose local multi-agent services and optional public access paths.

Mitigation: Keep services bound to localhost unless exposed routes have been reviewed, avoid exposing OASIS directly, and use a low-privilege account or container for installation.

Risk: The skill depends on stored API keys, user credentials, and external expert or callback URLs.

Mitigation: Avoid untrusted callback URLs or external expert API URLs and rotate tokens if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/avalon-467/skills/teamclaw)
- [TeamClaw repository](https://github.com/Avalon-467/Teamclaw)
- [TeamClaw README](artifact/README.md)
- [OASIS guide](artifact/OASIS_GUIDE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, YAML schedules, API examples, and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local service ports, API credentials, bot tokens, and workflow/session identifiers needed to operate the agent subsystem.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
