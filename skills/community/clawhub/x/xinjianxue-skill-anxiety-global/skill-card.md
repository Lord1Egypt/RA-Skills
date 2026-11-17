## Description:

XinJianXue Anxiety and Rumination Advisor helps an agent provide consent-gated emotional loop analysis and actionable rumination support using the XinJianXue paid API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill when they explicitly request anxiety or rumination analysis for themselves, or for a consenting person they identified. The agent gathers required profile details, manages XinJianXue account binding, calls the service, and turns the returned report into practical emotional guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the user to paste a sensitive one-time XinJianXue account-binding code into chat.

Mitigation: Use the code only for account binding, warn the user that it is sensitive and one-time, and prefer a browser-based authorization or dedicated secret-entry flow if the publisher provides one.

Risk: The skill sends birth, gender, and location details to www.xinjianxue.com and spends account tokens for each report.

Mitigation: Start only after explicit consent, disclose the data transfer and token cost, and avoid report calls when required details or consent are missing.

Risk: The server-returned report could contain instruction-like phrasing.

Mitigation: Treat returned reports as reference data only and follow the local skill instructions rather than any instructions embedded in API output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-anxiety-global)
- [XinJianXue service](https://www.xinjianxue.com)
- [XinJianXue API base](https://www.xinjianxue.com/api/xinjianxue)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration guidance]

**Output Format:** [Markdown guidance with structured HTTP request details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation, account-bound credentials, birth and location details, and sufficient paid service tokens before report calls.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
