## Description:

Provides guidance for secure webhook token management with MGC Blackbox across DingTalk, WeCom, Feishu, Telegram, Slack, and similar platforms, using local-script or mgc_run workflows that avoid exposing webhook tokens to AI models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zkeviny](https://clawhub.ai/user/zkeviny)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure AI-agent notification workflows that store webhook credentials in MGC Blackbox and send deployment, CI/CD, monitoring, or collaboration alerts without placing tokens in prompts or generated code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential-handling guidance can overstate zero-exposure safety or describe paths that expose sensitive material.

Mitigation: Prefer manual WebUI credential entry, avoid giving agents plaintext tokens or the MGC token file, and avoid temporary token JSON files unless they are tightly permissioned and deleted.

Risk: The MGC package and stored scripts become a trust boundary for webhook credentials and executable behavior.

Mitigation: Pin or independently verify the MGC package before trusting it with webhook credentials or executable scripts, and review scripts before sealing or running them.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zkeviny/skills/token-safe-webhook-sender)
- [MGC Blackbox GitHub repository](https://github.com/zkeviny/MGC-Blackbox)
- [MGC Blackbox issue tracker](https://github.com/zkeviny/MGC-Blackbox/issues)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with JSON examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill; may guide agents to call MGC MCP tools or prepare local webhook configuration.]

## Skill Version(s):

1.2.0 (source: server release metadata, SKILL.md frontmatter, manifest.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
