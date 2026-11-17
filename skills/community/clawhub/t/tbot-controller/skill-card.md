## Description:

Operate TradingBoat/TBOT (TBOT runtime stack) via a controlled automation interface (DB-first queries; lifecycle control on explicit request).

This skill is ready for commercial/non-commercial use.

## Publisher:

[plusgenie](https://clawhub.ai/user/plusgenie)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to inspect TBOT SQLite data, check runtime health and logs, and control a separate TradingBoat/TBOT stack when explicitly authorized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook mode may send authenticated trade instructions without the documented confirmation guard.

Mitigation: Review before installing, do not invoke JSON mode for previews, and use it only after confirming the intended action and whether the TBOT runtime is paper or live.

Risk: Webhook keys or other secrets may be exposed through generated payloads, output, or untrusted webhook destinations.

Mitigation: Restrict TBOT_WEBHOOK_URL to trusted local endpoints, avoid sharing outputs that contain webhook keys, and require secret redaction before broader use.

Risk: Control actions can affect a separate TBOT runtime stack if the runtime location is wrong or ambiguous.

Mitigation: Run discovery first, require an explicit runtime location when discovery is ambiguous, and require explicit confirmation before start, stop, restart, or trading actions.

## Reference(s):

- [TBOT Controller ClawHub page](https://clawhub.ai/plusgenie/skills/tbot-controller)
- [Publisher profile](https://clawhub.ai/user/plusgenie)
- [TBOT Controller ops reference](artifact/references/ops.md)
- [Reference runtime implementation](https://github.com/PlusGenie/openclaw-on-tradingboat)
- [uv documentation](https://docs.astral.sh/uv/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, status tables, and schema-validated JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only status and database inspection are the default posture; JSON webhook mode can send requests when invoked.]

## Skill Version(s):

1.0.0 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
