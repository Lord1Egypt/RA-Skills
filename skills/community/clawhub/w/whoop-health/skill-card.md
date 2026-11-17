## Description:

Fetches WHOOP wearable health data through OAuth-backed API calls and helps agents analyze recovery, sleep, workout, cycle, profile, and body-measurement records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jarviyin](https://clawhub.ai/user/jarviyin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to authenticate with WHOOP, fetch wearable health records, export data, and ask an agent to analyze trends such as HRV, sleep performance, strain, and recovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad access to sensitive WHOOP recovery, sleep, workout, cycle, profile, and body-measurement data.

Mitigation: Install only when that scope is acceptable, limit use to trusted machines, and revoke access when finished.

Risk: Tokens are stored locally in ~/.whoop_tokens.json and could expose health or account data if the machine or synced home directory is shared.

Mitigation: Protect the token file, avoid shared or synced machines, and delete or revoke tokens after use.

Risk: The OAuth callback flow should be hardened with state validation before use in a sensitive environment.

Mitigation: Review and strengthen OAuth state handling before deploying this skill for sensitive or managed use.

## Reference(s):

- [WHOOP API Endpoints Reference](artifact/references/api_endpoints.md)
- [WHOOP Developer Portal](https://developer.whoop.com)
- [ClawHub WHOOP Health Skill Page](https://clawhub.ai/jarviyin/skills/whoop-health)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, JSON, CSV]

**Output Format:** [Markdown guidance with shell commands and optional JSON or CSV export files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include local files containing sensitive health, profile, and body-measurement data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
