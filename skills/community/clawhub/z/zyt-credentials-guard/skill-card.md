## Description:

Guide users to configure local Chanjing credentials safely via local commands only, and validate local token status when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zuoyuting214](https://clawhub.ai/user/zuoyuting214)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Chanjing API users use this skill to configure local AK/SK credentials, refresh access tokens, and validate local credential status without pasting secrets into chat.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long-lived Chanjing AK/SK values and refreshed access tokens are stored in a predictable plaintext local file.

Mitigation: Create the credentials directory and file with restrictive permissions, keep the file out of repositories, backups, and chat, and rotate Chanjing keys if exposure is suspected.

Risk: Users may paste AK/SK values into chat during setup.

Mitigation: Keep credential entry local only; if a secret is shared in chat, treat it as exposed and rotate the Chanjing keys before continuing.

Risk: Token refresh updates the local credentials file and may write sensitive data to an unintended location if the config directory is mis-set.

Mitigation: Confirm the intended CHANJING_CONFIG_DIR path before writing credentials and avoid broad filesystem permissions on that directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zuoyuting214/skills/zyt-credentials-guard)
- [Credentials Guard Reference](reference.md)
- [Chanjing API homepage](https://open-api.chanjing.cc)
- [Chanjing documentation](https://doc.chanjing.cc)
- [Chanjing login](https://www.chanjing.cc/openapi/login)
- [Chanjing access-token endpoint](https://open-api.chanjing.cc/open/v1/access_token)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON configuration examples and occasional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local credentials file at ~/.chanjing/credentials.json, or $CHANJING_CONFIG_DIR/credentials.json when configured.]

## Skill Version(s):

0.5.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
