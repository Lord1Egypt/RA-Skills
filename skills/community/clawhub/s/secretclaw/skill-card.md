## Description:

SecretClaw helps agents collect API keys and other sensitive OpenClaw configuration values through a temporary HTTPS form instead of asking users to type secrets in chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apsntian](https://clawhub.ai/user/apsntian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill when an agent needs to register API keys, tokens, passwords, or other sensitive configuration values without placing the secret directly in chat history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Secrets are submitted through a temporary Cloudflare-managed public tunnel.

Mitigation: Use only for lower-risk credentials when the user accepts Cloudflare tunnel transit, and avoid high-value credentials until the release clearly warns users about this path.

Risk: Manipulated labels or configuration keys may affect the generated web form or where a submitted secret is saved.

Mitigation: Escape dynamic HTML fields and validate configuration keys against expected OpenClaw paths before accepting submissions.

Risk: Raw subprocess errors may reveal operational details in the browser response.

Mitigation: Return a generic save failure to the browser and keep detailed errors in local logs for review.

## Reference(s):

- [OpenClaw](https://github.com/openclaw/openclaw)
- [Cloudflare Tunnel downloads](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/)
- [SecretClaw ClawHub listing](https://clawhub.ai/apsntian/skills/secretclaw)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and plain status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates a temporary HTTPS form URL and saves the submitted value to OpenClaw configuration.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
