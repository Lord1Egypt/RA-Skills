## Description:

XinJianXue Job-Change Decision Advisor helps an agent provide career-change guidance by calling the XinJianXue API after user consent, onboarding, and required personal context collection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill when they want a structured stay-or-leave or career-change analysis. The agent collects consent and required personal context, calls the XinJianXue service, and presents a weighing framework rather than an absolute decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow sends birth date, gender, birth or current location, and a one-time authorization code to the XinJianXue service.

Mitigation: Ask for explicit user consent before starting, collect only the required fields, and direct users to the official XinJianXue domain for authorization.

Risk: Later report calls use stored service credentials and may consume paid account tokens.

Mitigation: Store credentials only in dedicated credential storage, mask credentials in conversation, and disclose token use before report calls.

Risk: Remote report content could contain instruction-like text.

Mitigation: Treat returned reports only as analysis data and follow the local skill role definition as the instruction source.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-job-change-global)
- [Publisher Profile](https://clawhub.ai/user/weixin97676414)
- [XinJianXue Website](https://www.xinjianxue.com)
- [XinJianXue API Base](https://www.xinjianxue.com/api/xinjianxue)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Configuration]

**Output Format:** [Markdown guidance with JSON HTTP request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit consent, service credentials, and sufficient XinJianXue account tokens before report calls.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
