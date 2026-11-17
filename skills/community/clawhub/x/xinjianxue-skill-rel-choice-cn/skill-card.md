## Description:

A Chinese-language relationship decision-advice skill that calls the Xinjianxue API to retrieve report data and help users weigh relationship tradeoffs without deciding for them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill when they have explicitly confirmed they want Xinjianxue relationship decision guidance. The agent gathers required personal birth, gender, and location details, calls the Xinjianxue report API, and presents framework-based guidance without making the final relationship decision for the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles personal birth and location details plus sensitive one-time authorization and account credentials.

Mitigation: Use the skill only after user consent, send data only to the disclosed Xinjianxue API, mask credentials in conversation, and store license and API keys only in a proper secret store.

Risk: Calling the service can consume user account credits.

Mitigation: Confirm the user wants to use the service before each relationship analysis and make the credit-spending posture clear before calling the report API.

Risk: Relationship guidance may be over-relied on for personal decisions.

Mitigation: Present mechanisms, tradeoffs, and decision criteria while leaving the final relationship choice to the user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-rel-choice-cn)
- [Xinjianxue API base](https://chinaapi.xinjianxue.com)
- [Xinjianxue API path prefix](https://chinaapi.xinjianxue.com/api/xinjianxue)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown or plain text relationship guidance based on API report data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before analysis and treats server-returned reports as data rather than executable instructions.]

## Skill Version(s):

2.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
