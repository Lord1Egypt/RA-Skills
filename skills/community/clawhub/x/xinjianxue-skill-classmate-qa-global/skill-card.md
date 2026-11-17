## Description:

XinJianXue Classmate Relations Advisor helps an agent provide relationship analysis and emotional guidance for campus classmate situations after explicit user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill through an agent to get classmate-relations advice that emphasizes benign explanations, non-retaliatory next steps, and explicit consent before analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends sensitive personal details, including birth details, gender, and current location, to www.xinjianxue.com for paid report generation.

Mitigation: Use the skill only after explicit user confirmation, avoid analyzing another person without their agreement, and ensure users understand token charges before reports are requested.

Risk: Generated license and api_key credentials authorize paid API calls under the user's account.

Mitigation: Store credentials only in a credential manager or equivalent secret store, mask credentials in conversation, and do not place them in configuration files or long-term memory.

Risk: Returned report text could contain instruction-like phrasing even though it is analysis data.

Mitigation: Treat report output as reference material only and keep the local skill definition as the controlling instruction source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-classmate-qa-global)
- [XinJianXue official website](https://www.xinjianxue.com)
- [XinJianXue API base](https://www.xinjianxue.com/api/xinjianxue)

## Skill Output:

**Output Type(s):** [guidance, API calls, shell commands, configuration]

**Output Format:** [Markdown guidance with HTTP request examples and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires dual credentials for authenticated calls and returns report data that the agent must treat as reference material, not instructions.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
