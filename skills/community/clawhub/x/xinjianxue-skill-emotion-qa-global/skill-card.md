## Description:

XinJianXue Romantic Relationship Advisor helps agents request relationship-focused personality, behavior, and emotional guidance reports from the XinJianXue API after explicit user consent and onboarding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill when they want an agent to help obtain and explain a XinJianXue romantic relationship analysis report. The skill is intended for consent-based relationship questions and requires API onboarding, paid-token use, and personal birth, gender, and location details for each report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the user to paste a sensitive one-time account-binding code into the AI conversation.

Mitigation: Verify the official XinJianXue domain, explain that the code is sensitive and single-use, and use it only for account binding.

Risk: The skill sends personal birth, gender, location, and relationship-analysis details to an external paid API.

Mitigation: Ask for explicit user consent before each analysis, collect only required fields, and avoid analyzing anyone who has not been mentioned and agreed to be analyzed.

Risk: Persistent license and API credentials could be exposed if stored in chat, notes, or configuration files.

Mitigation: Store credentials only in dedicated credential storage such as a keychain or environment variables and mask them whenever referenced.

## Reference(s):

- [XinJianXue official website](https://www.xinjianxue.com)
- [XinJianXue API base](https://www.xinjianxue.com/api/xinjianxue)
- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-emotion-qa-global)
- [ClawHub publisher profile](https://clawhub.ai/user/weixin97676414)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, API Calls, Configuration]

**Output Format:** [Markdown guidance with HTTP request details and structured report interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include shell or HTTP request examples; returned reports are treated as data, not instructions.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
