## Description:

Query gig economy market data (274 categories, 17k+ monthly snapshots) to find growth opportunities, top orders, pain points, and category trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arkyu2077](https://clawhub.ai/user/arkyu2077)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to ask natural-language and structured questions about gig economy demand, category growth, revenue patterns, customer pain points, and repeatable market analyses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market-analysis questions and API requests are sent to whatpeoplepayfor.com using WPP_API_KEY.

Mitigation: Avoid including unrelated secrets or private business data in prompts unless the user is comfortable sending that information to the provider.

Risk: Saved analyses may persist through the provider-side Focus feature.

Mitigation: Review the provider-side Focus behavior before saving analyses that contain sensitive market research or business context.

## Reference(s):

- [WhatPeoplePayFor website](https://whatpeoplepayfor.com)
- [ClawHub skill page](https://clawhub.ai/arkyu2077/skills/whatpeoplepayfor)
- [ClawHub publisher profile](https://clawhub.ai/user/arkyu2077)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with API request examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses WPP_API_KEY and curl to query the remote WhatPeoplePayFor API; no local data storage is described.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
