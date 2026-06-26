## Description: <br>
Workplace wellness for stress, anxiety, and burnout - mindfulness exercises, breathing techniques, mood check-ins, notifications, timeline, and a full wellbeing catalogue from Zen+ Health. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ollieparsley](https://clawhub.ai/user/ollieparsley) <br>

### License/Terms of Use: <br>
Proprietary <br>


## Use Case: <br>
Employees and Zen+ Health users use this skill in OpenClaw to view wellness notifications, activity timeline, profile preferences, and the wellbeing catalogue. It can help select mindfulness or breathing exercises when users ask for support with stress, anxiety, relaxation, or burnout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wellness notifications, timeline, profile, and preference data may be exposed in shared chats, logs, or poorly scoped OpenClaw environments. <br>
Mitigation: Use the skill only in trusted environments, avoid sharing API responses in public or shared contexts, and review local logging settings before deployment. <br>
Risk: ZEN_API_KEY exposure could allow read access to the user's Zen+ Health data within the key's scopes. <br>
Mitigation: Store ZEN_API_KEY as a secret, do not hardcode or paste it into chat logs, and revoke or rotate the key immediately if exposure is suspected. <br>
Risk: Requests sent to an unintended API host could disclose the API key or wellness data. <br>
Mitigation: Keep ZEN_API_BASE_URL set to the official Zen+ Health API host: https://api.zenplus.health. <br>


## Reference(s): <br>
- [Zen+ Health API Documentation](https://zenplus.health/api/docs) <br>
- [Zen+ Health OpenClaw Skill](https://zenplus.health/openclaw) <br>
- [Zen+ Health API Key Settings](https://zenplus.health/settings/api-keys) <br>
- [Security Guidelines](SECURITY.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ollieparsley/zenplus-health) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with curl commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ZEN_API_KEY, ZEN_API_BASE_URL, curl, and jq; API access is documented as read-only and rate-limited.] <br>

## Skill Version(s): <br>
1.0.4 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
