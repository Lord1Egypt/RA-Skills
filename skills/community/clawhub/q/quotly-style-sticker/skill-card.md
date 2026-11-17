## Description:

Generate QuotLy-style stickers from forwarded messages and return one MEDIA path for auto-send.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sakullla](https://clawhub.ai/user/sakullla)

### License/Terms of Use:


## Use Case:

External users and agent operators use this skill to turn selected forwarded or quoted chat messages into a QuotLy-style WebP sticker for auto-send in group conversations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected message content and sender/profile fields may be sent to the configured QuotLy rendering service.

Mitigation: Use only where users understand this data flow and avoid sensitive conversations unless the deployment has approved the external renderer.

Risk: Network protections are under-scoped for sensitive chat or cloud-hosted environments.

Mitigation: Set QUOTLY_API_ALLOW_HOSTS to the intended rendering host and review deployment network access before installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sakullla/skills/quotly-style-sticker)
- [QuotLy rendering endpoint](https://bot.lyo.su/quote/generate)

## Skill Output:

**Output Type(s):** [text, shell commands, files, configuration]

**Output Format:** [stdout status text plus MEDIA absolute path to a generated WebP file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Suppresses duplicate retries within the configured dedupe window and emits no MEDIA line when a duplicate is skipped.]

## Skill Version(s):

1.4.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
