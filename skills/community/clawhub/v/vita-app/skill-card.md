## Description:

VITA — Longevity Intelligence lets agents retrieve a user's VITA health data, including daily AI insights, wearable metrics from Oura/WHOOP, and active supplement protocols.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dobrinalexandru](https://clawhub.ai/user/dobrinalexandru)

### License/Terms of Use:


## Use Case:

Users and their agents use this skill to retrieve a personal daily health briefing, current sleep and recovery metrics, and active supplement protocols from VITA.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive personal health, wearable, and supplement data through the user's VITA API key.

Mitigation: Install only when comfortable granting this access, keep the API key private, and revoke or rotate it if access is no longer needed.

Risk: Broad health-related triggers can lead the agent to access VITA for ambiguous health questions.

Mitigation: For ambiguous health questions, explicitly state whether the agent should or should not access VITA before it uses the skill.

Risk: Generated outputs may include private health details.

Mitigation: Avoid sharing briefings, raw metrics, or supplement details where sensitive health information should remain private.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/dobrinalexandru/skills/vita-app)
- [Publisher profile](https://clawhub.ai/user/dobrinalexandru)
- [VITA API endpoint](https://app.vitadao.com/api/vita-api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide API calls that retrieve sensitive personal health, wearable, and supplement data.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
