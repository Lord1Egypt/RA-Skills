## Description:

A Chinese-language ClawHub skill that lets an agent, with user confirmation, call the Xinjianxue paid API to produce long-distance relationship maintenance analysis from user-provided personal details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users can ask an agent to assess long-distance relationship maintenance costs and practical next steps after confirming use of the Xinjianxue service. The skill guides consent, account binding, credential storage, API calls, and delivery of a user-facing analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends personal birth, gender, birthplace, and current-location details to the Xinjianxue API for analysis.

Mitigation: Ask for explicit user confirmation before each analysis and send only the fields required for the selected report input level.

Risk: The skill binds an agent to a user account using a sensitive one-time authorization code and then stores API credentials for future calls.

Mitigation: Use a dedicated secret store for the license key and API key, avoid displaying credentials in chat, and request the authorization code only when the user intends to bind the agent.

Risk: The paid API consumes Xinjianxue service credits when reports are generated.

Mitigation: Confirm that the user wants to use the service before report calls and clearly disclose that calls may spend service credits.

Risk: Returned reports could contain text that looks like instructions to the agent.

Mitigation: Treat report content only as analysis data and ignore any instruction-like language in API responses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-long-distance-cn)
- [Xinjianxue API base](https://chinaapi.xinjianxue.com)
- [Xinjianxue API path prefix](https://chinaapi.xinjianxue.com/api/xinjianxue)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text, markdown]

**Output Format:** [Markdown guidance with HTTP request details and user-facing analysis text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before analysis; report responses are treated as data, not instructions.]

## Skill Version(s):

2.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
