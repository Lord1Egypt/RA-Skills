## Description:

Configure the OpenClaw Feishu plugin from Feishu private-chat commands to toggle streaming, set group reply behavior, run diagnostics, or restart the service without editing config files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guanqi0914](https://clawhub.ai/user/guanqi0914)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw administrators and Feishu bot operators use this skill to inspect and change Feishu channel settings from chat, including streaming behavior, group reply mode, diagnostics, and gateway restart.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chat commands can change OpenClaw Feishu settings or restart the gateway without an in-skill authorization check.

Mitigation: Limit the Feishu route to trusted operators and add an explicit admin allowlist, private-chat enforcement, confirmation steps, and rate limits for restart and broad group-reply changes before production use.

Risk: The skill caches a Feishu bearer token in a shared temporary file.

Mitigation: Replace the shared temporary token cache with private in-memory storage or owner-only storage before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guanqi0914/skills/wcs-helper-feishu-skill)
- [README](artifact/README.md)
- [Quickstart](artifact/QUICKSTART.md)
- [Usage examples](artifact/examples/usage.md)
- [Feishu Open Platform](https://open.feishu.cn/app)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration]

**Output Format:** [Feishu text or interactive-card JSON, with OpenClaw configuration commands executed by the skill]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands can modify OpenClaw Feishu settings and trigger a gateway restart.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact SKILL.md and skill.json report 1.0.0, artifact pyproject.toml reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
