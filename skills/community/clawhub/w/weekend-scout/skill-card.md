## Description: <br>
Weekend Scout discovers next-weekend outdoor events, festivals, fairs, and road-trip ideas near the user's city and nearby cities, then builds home-city picks and road-trip options, formats the digest, and can send it to Telegram. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gooorooox](https://clawhub.ai/user/gooorooox) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to scout outdoor weekend events near a configured home city, rank local and nearby-city options, and produce a digest suitable for chat or Telegram delivery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores city, coordinates, event cache, logs, and optional Telegram bot token and chat ID locally. <br>
Mitigation: Use it only on systems where that local state is acceptable, protect the runtime profile, and use the documented reset or uninstall commands when the stored state should be removed. <br>
Risk: The skill performs web searches, downloads GeoNames data, and may send generated digests to Telegram when configured. <br>
Mitigation: Review the configured city, radius, Telegram destination, and generated digest before delivery, especially when using shared chats or channels. <br>


## Reference(s): <br>
- [Weekend Scout ClawHub page](https://clawhub.ai/gooorooox/weekend-scout) <br>
- [README](README.md) <br>
- [Installation guide](install/README.md) <br>
- [Platform skill reference](docs/platform-skill-reference.md) <br>
- [Weekend Scout design document](docs/weekend-scout-design-v2.md) <br>
- [Search workflow](.agents/skills/weekend-scout/references/search-workflow.md) <br>
- [Scoring and trips](.agents/skills/weekend-scout/references/scoring-and-trips.md) <br>
- [Delivery and audit](.agents/skills/weekend-scout/references/delivery-and-audit.md) <br>
- [Onboarding](.agents/skills/weekend-scout/references/onboarding.md) <br>
- [Platform transport](.agents/skills/weekend-scout/references/platform-transport.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown digest and operational guidance with shell commands and JSON-backed CLI payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce a Telegram-ready HTML message file through the Weekend Scout CLI when Telegram delivery is configured.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
