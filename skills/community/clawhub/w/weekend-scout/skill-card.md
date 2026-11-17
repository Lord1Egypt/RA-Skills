## Description:

Weekend Scout discovers next-weekend outdoor events, festivals, fairs, and road-trip ideas near the user's city and nearby cities, then builds local picks and road-trip options, formats the digest, and can send it to Telegram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gooorooox](https://clawhub.ai/user/gooorooox)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this agent skill to scout next-weekend outdoor events near a configured city, rank local and nearby-city options, and receive a concise weekend digest in chat or Telegram.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs Python commands and may auto-install Python dependencies.

Mitigation: Install in an isolated virtual environment and review dependency versions before use.

Risk: The skill can search and fetch web pages while building event recommendations.

Mitigation: Review the generated digest and audit summary before acting on event details.

Risk: Telegram bot credentials may be exposed through terminal output, transcripts, or logs.

Mitigation: Treat the bot token as a password, avoid sharing logs that may contain it, and rotate the token if exposure is suspected.

Risk: The skill stores local configuration, cache files, logs, downloaded GeoNames data, and event records.

Mitigation: Use the documented reset or uninstall flows to remove local configuration and cache data when no longer needed.

## Reference(s):

- [Weekend Scout README](README.md)
- [Installation Guide](install/README.md)
- [Weekend Scout Design Document](docs/weekend-scout-design-v2.md)
- [Platform Skill Reference](docs/platform-skill-reference.md)
- [Search Workflow](.agents/skills/weekend-scout/references/search-workflow.md)
- [Scoring And Trips](.agents/skills/weekend-scout/references/scoring-and-trips.md)
- [Delivery And Audit](.agents/skills/weekend-scout/references/delivery-and-audit.md)
- [GeoNames](https://www.geonames.org/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown digest with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local event picks, road-trip options, discovery audit summaries, and Telegram delivery status.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
