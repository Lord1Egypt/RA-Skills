## Description:

Quickly retrieves WeChat Official Account TOP50 comprehensive rankings across daily, weekly, and monthly charts with category filtering, engagement metrics, analysis, HTML report generation, and subscription-oriented responses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[if530770](https://clawhub.ai/user/if530770)

### License/Terms of Use:

MIT-0

## Use Case:

WeChat account operators, MCN teams, brand marketers, and content entrepreneurs use this skill to compare leading public accounts, track competitors, inspect engagement metrics, and prepare ranking reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill integrates with the third-party RedFoxHub API and requires a REDFOX_API_KEY.

Mitigation: Confirm the key source, scope, revocation process, and RedFoxHub terms before use; keep the key out of prompts, logs, source files, and shared reports.

Risk: The scripts can scan local shell profile files while looking for REDFOX_API_KEY.

Mitigation: Prefer setting REDFOX_API_KEY only in the current execution environment and review profile-file access before deployment.

Risk: Generated HTML reports execute JavaScript for export and interaction features.

Mitigation: Open generated reports only in trusted contexts and review report content before sharing or archiving.

Risk: The package claims scheduled subscriptions, but server security evidence says a real scheduler and subscription storage are not implemented.

Mitigation: Do not rely on automated subscription delivery unless the publisher adds and documents durable scheduling and storage behavior.

## Reference(s):

- [Core workflow](references/core_workflow.md)
- [RedFoxHub](https://redfox.hk)
- [RedFoxHub API keys](https://redfox.hk/settings/api-keys?source=clawhub)
- [ClawHub skill page](https://clawhub.ai/if530770/skills/wechat-power-ranking)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown ranking tables, JSON-backed script output, shell commands, and generated HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY for RedFoxHub API access; HTML reports may include client-side JavaScript for export features.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
