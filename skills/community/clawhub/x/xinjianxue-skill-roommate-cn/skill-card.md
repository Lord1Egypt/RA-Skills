## Description:

A Chinese-language Xinjianxue roommate relationship advisor that helps an agent confirm consent, use the Xinjianxue paid report API, and turn the returned report into boundary-setting scripts and shared-living rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill when they explicitly want a Chinese roommate-conflict advisor to help frame boundaries, communication scripts, and practical rules for shared living issues using Xinjianxue's report service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends birth date or time, gender, birthplace, and current location details to an external Xinjianxue service for processing.

Mitigation: Use the skill only after explicit informed consent, avoid submitting another person's details without clear agreement, and prefer local roommate advice when the external report is not necessary.

Risk: The skill links the agent to a user's Xinjianxue account and can consume paid or promotional credits through API calls.

Mitigation: Store license and API credentials only in a dedicated secret store, do not expose them in chat or files, and make charge-bearing report calls only after user confirmation.

Risk: Returned report content could contain directive-style language even though it is external data.

Mitigation: Treat report output as reference data only, ignore embedded instructions, and base final guidance on the local skill role and the user's confirmed roommate issue.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-roommate-cn)
- [Publisher profile](https://clawhub.ai/user/weixin97676414)
- [Xinjianxue API base](https://chinaapi.xinjianxue.com/api/xinjianxue)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTTP request examples and user-facing Chinese response text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user consent, user account binding, secure credential storage, and paid API credits before report calls.]

## Skill Version(s):

2.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
