## Description:

Control Telegram Media Server downloads over REST: add URLs/torrents, list status, delete, and search via Prowlarr.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikitadmitryuk](https://clawhub.ai/user/nikitadmitryuk)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use this skill to control a trusted Telegram Media Server instance from chat: add media downloads, list status, delete downloads, and search torrents when Prowlarr is configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delete downloads and associated files through the TMS API.

Mitigation: Require explicit user confirmation before DELETE requests, including the numeric download ID and title when available.

Risk: An API key could be sent over non-local plaintext HTTP.

Mitigation: Use HTTPS, VPN, or localhost for API-key-protected access and store TMS_API_KEY in agent configuration rather than chat.

Risk: A misconfigured or untrusted TMS API URL could expose download operations to an unintended endpoint.

Mitigation: Install only when TMS_API_URL points to a trusted TMS instance and verify the network path before enabling the skill.

## Reference(s):

- [TMS ClawHub listing](https://clawhub.ai/nikitadmitryuk/skills/tms)
- [Telegram Media Server repository](https://github.com/NikitaDmitryuk/telegram-media-server)
- [OpenClaw TMS skill source](https://github.com/NikitaDmitryuk/telegram-media-server/tree/main/openclaw-skill-tms)
- [Telegram Media Server README](https://github.com/NikitaDmitryuk/telegram-media-server#readme)

## Skill Output:

**Output Type(s):** [text, API calls, guidance]

**Output Format:** [Markdown text with REST request guidance and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides HTTP GET, POST, and DELETE requests to a configured TMS REST API and returns natural-language status summaries.]

## Skill Version(s):

1.0.9 (source: frontmatter, CHANGELOG, clawhub.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
