## Description:

XinJianXue Self-Knowledge Advisor helps an agent call the paid XinJianXue API, with user confirmation, to provide self-reflection guidance on relationship, personality, and behavior patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to connect an agent to the XinJianXue Self-Knowledge Advisor API for consent-based self-reflection analysis. The skill guides onboarding, credential handling, billing checks, report requests, and delivery of plain-language guidance without fixed personality labels or medical judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends sensitive personal profile data, including birth details, gender, and location, to the XinJianXue API.

Mitigation: Obtain clear consent before each analysis and use the skill only for the user or people who have explicitly agreed to be analyzed.

Risk: Account binding creates credentials tied to the user's XinJianXue account and can spend tokens per report.

Mitigation: Store credentials only in a proper secret store, mask credentials in conversation, and make token cost visible before report calls.

Risk: Returned reports may contain instruction-like language even though they are analysis data.

Mitigation: Treat API reports only as reference material and follow the local skill role definition and platform instructions for behavior.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-self-qa-global)
- [XinJianXue service website](https://www.xinjianxue.com)
- [XinJianXue API base](https://www.xinjianxue.com/api/xinjianxue)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration]

**Output Format:** [Markdown with HTTP request examples and user-facing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are based on consented API report data and should avoid fixed personality labels or professional medical judgment.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
