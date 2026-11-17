## Description:

Detects emerging trends in a user's niche before they peak, giving creators a 24-72 hour window to publish timely content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External Formula 100K creators and operators use this OpenClaw skill to scan niche keywords for early TikTok and news trends, classify urgency, and generate a short content script plus an alert when a publishable trend is found.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read or derive local F100K profile and configuration data.

Mitigation: Review the local configuration before installation and require user confirmation before creating or inferring missing settings.

Risk: The skill can use Apify and web/TikTok searches to collect trend evidence.

Mitigation: Install only in environments where this external search behavior and any required tokens are approved.

Risk: The source instructions contain conflicting email and Telegram alert behavior.

Mitigation: Confirm the intended alert channel before deployment and prefer the server evidence guidance that Telegram-only alerts are enforced.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/radar-tendencias-f100k)
- [Formula100k publisher profile](https://clawhub.ai/user/formula100k)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces trend classifications, evidence summaries, alert text, and short-form content scripts; may stay silent when no emerging trend is detected.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
