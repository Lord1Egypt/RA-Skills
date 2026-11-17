## Description:

Workplace wellness for stress, anxiety, and burnout - mindfulness exercises, breathing techniques, mood check-ins, notifications, timeline, and a full wellbeing catalogue from Zen+ Health.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ollieparsley](https://clawhub.ai/user/ollieparsley)

### License/Terms of Use:

Proprietary

## Use Case:

Employees and external users use this skill to access Zen+ Health wellness notifications, activity timelines, profile preferences, and catalogue exercises from an agent workflow. It supports read-only wellness check-ins, stress and anxiety support prompts, and browsing mindfulness or breathing activities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive health-adjacent account data such as wellness notifications, timeline entries, profile information, and working-hours preferences.

Mitigation: Use it only in trusted workspaces, avoid shared or logged sessions for personal wellness queries, and require user confirmation before fetching profile, notification, timeline, or schedule data.

Risk: The API key is sent to the endpoint configured in ZEN_API_BASE_URL.

Mitigation: Set ZEN_API_BASE_URL exactly to the official HTTPS API endpoint and use a dedicated, revocable read-only Zen+ Health API key.

Risk: Broad stress, anxiety, and wellness triggers may cause the agent to fetch account data when the user expected only general guidance.

Mitigation: Ask for confirmation before account-specific API calls and offer catalogue-only or general wellness guidance when account access is not needed.

## Reference(s):

- [Zen+ Health API Documentation](https://zenplus.health/api/docs)
- [Zen+ Health API Key Settings](https://zenplus.health/settings/api-keys)
- [Zen+ Health OpenClaw Skill](https://zenplus.health/openclaw)
- [ClawHub Skill Page](https://clawhub.ai/ollieparsley/skills/zenplus-health)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, ZEN_API_KEY, and ZEN_API_BASE_URL; API access is documented as read-only and rate-limited.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
