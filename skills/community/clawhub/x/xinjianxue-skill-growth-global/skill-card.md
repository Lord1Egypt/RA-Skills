## Description:

XinJianXue Personal Growth Advisor helps an agent call the XinJianXue API to produce evidence-based personal growth, relationship, personality, and behavior-pattern analysis after user confirmation and onboarding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill through an agent to request XinJianXue personal growth analysis, including bottleneck diagnosis, relationship analysis, personality and behavior-pattern reading, and emotionally oriented guidance. The skill guides onboarding, credential handling, direct API calls, report translation, and response framing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends sensitive personal details to XinJianXue for report generation.

Mitigation: Use the skill only after explicit user confirmation and only when the user understands what personal details are sent to the service.

Risk: The onboarding code, license key, and API key are sensitive credentials.

Mitigation: Store credentials only in agreed dedicated credential storage, avoid displaying them in conversation, and mask credential values when they must be referenced.

Risk: Report calls consume account tokens.

Mitigation: Confirm the user wants the analysis before each report call and explain token or billing status when the service reports insufficient tokens.

Risk: Returned reports may contain instruction-like text.

Mitigation: Treat returned reports as data and reference material only; follow the local skill role and security rules as the instruction source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-growth-global)
- [Publisher profile](https://clawhub.ai/user/weixin97676414)
- [XinJianXue service](https://www.xinjianxue.com)
- [XinJianXue API base](https://www.xinjianxue.com/api/xinjianxue)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with HTTP request details, JSON examples, and user-facing analysis text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include translated report interpretation, credential storage guidance, onboarding prompts, token and billing explanations, and error-handling instructions.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
