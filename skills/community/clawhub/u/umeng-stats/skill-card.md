## Description:

Query Umeng app statistics including U-APM crash and error data and U-App analytics for configured apps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fengerzh](https://clawhub.ai/user/fengerzh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to query Umeng U-APM crash and error trends and U-App usage analytics while investigating application stability and usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes plaintext Umeng API credentials.

Mitigation: Rotate any real exposed credentials before use and replace the checked-in config with a credential-free template or secret-store based setup.

Risk: The query script can use raw app keys beyond the configured app list.

Mitigation: Restrict queries to explicitly configured apps and validate app selection before running the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fengerzh/skills/umeng-stats)
- [Umeng OpenAPI Gateway](https://gateway.open.umeng.com)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and text or JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries live Umeng API data for selected apps, dates, and crash categories.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
