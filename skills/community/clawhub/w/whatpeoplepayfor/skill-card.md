## Description: <br>
Query gig economy market data across freelance categories and monthly gig snapshots to identify growth opportunities, top orders, pain points, and category trends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arkyu2077](https://clawhub.ai/user/arkyu2077) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to query WhatPeoplePayFor market data, compare freelance category demand, inspect revenue and order signals, and save analyses for later reruns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends market-analysis questions and API usage to whatpeoplepayfor.com, and saved Focuses may store analysis content with the provider. <br>
Mitigation: Install only if you trust the provider with those questions and avoid saving secrets, customer data, or confidential strategy in Focuses. <br>
Risk: WPP_API_KEY grants access to the paid API and should be treated as a secret. <br>
Mitigation: Store the API key in the environment, avoid committing or logging it, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [WhatPeoplePayFor website](https://whatpeoplepayfor.com) <br>
- [ClawHub skill page](https://clawhub.ai/arkyu2077/whatpeoplepayfor) <br>
- [Publisher profile](https://clawhub.ai/user/arkyu2077) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl examples and API response interpretation guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and WPP_API_KEY; sends authenticated HTTPS requests to whatpeoplepayfor.com.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
