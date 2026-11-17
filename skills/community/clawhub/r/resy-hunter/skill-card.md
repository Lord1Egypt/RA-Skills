## Description:

Monitor hard-to-get restaurant reservations on Resy, OpenTable, and Tock. Check availability, manage a watchlist, and get Telegram alerts when tables open up.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shahedkhan30](https://clawhub.ai/user/shahedkhan30)

### License/Terms of Use:


## Use Case:

External users use this skill to find available restaurant reservation slots, manage a watchlist, and set up alerts for openings across Resy, OpenTable, and Tock. It is intended to surface availability and booking links, not to book reservations automatically.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles restaurant account credentials, a static Resy API key, Telegram alert access, and reusable OpenTable session data.

Mitigation: Keep the skill data directory private, avoid committing or sharing stored tokens or session files, and rotate credentials if exposure is suspected.

Risk: Browser automation uses Playwright for OpenTable and Tock and the security evidence recommends caution around sandboxing and secret-file permissions.

Mitigation: Run browser-based checks in a contained environment and review execution settings before installing or scheduling automated monitoring.

Risk: Scheduled monitoring can continue checking services and sending alerts after the user no longer needs it.

Mitigation: Disable or remove the cron job when active monitoring is no longer required.

## Reference(s):

- [OpenTable & Tock Reference](references/platforms.md)
- [Resy API Reference](references/resy-api.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON availability results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Availability checks are read-only; monitoring may maintain local watchlist, token, timestamp, and session files under the user's OpenClaw data directory.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
