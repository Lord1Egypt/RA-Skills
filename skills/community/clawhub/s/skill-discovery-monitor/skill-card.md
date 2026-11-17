## Description:

Skill Discovery Monitor helps agents discover popular skills across ClawHub, GitHub Actions, and npm, then summarize findings with metrics, usage flowcharts, and optional notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhdryanchang](https://clawhub.ai/user/zhdryanchang)

### License/Terms of Use:

MIT

## Use Case:

Developers, automation teams, skill creators, and learners use this skill to monitor skill ecosystems, compare popular tools, and receive scheduled discovery reports through configured notification channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release ships a live-looking SkillPay API key.

Mitigation: Rotate the exposed key, remove it from the artifact, and require operators to provide their own secret through environment configuration.

Risk: Subscription and payment operations are exposed without adequate access control.

Mitigation: Add authentication and avoid public deployment until subscription endpoints are protected.

Risk: Payment callback handling may trust caller-supplied status data.

Mitigation: Verify signed payment callbacks before activating subscriptions or recording payment state.

Risk: Contact and payment-related data handling is not documented clearly enough for operators.

Mitigation: Document what contact and payment data is stored, how it is used, and how operators should protect it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhdryanchang/skills/skill-discovery-monitor)
- [ClawHub publisher profile](https://clawhub.ai/user/zhdryanchang)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON API responses, Markdown notification summaries, Mermaid usage-flow text, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May contact ClawHub, GitHub, npm, SkillPay, Telegram, Discord, and SMTP services when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata, skill.json, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
