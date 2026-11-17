## Description:

Helps agents search for low-cost flight options by checking nearby-airport combinations, then summarize the cheapest routes and ground-transport tradeoffs.

This skill is for research and development only.

## Publisher:

[xiaoyiyebuaijianghua](https://clawhub.ai/user/xiaoyiyebuaijianghua)

### License/Terms of Use:

MIT

## Use Case:

Developers, agents, and travel researchers use this skill to query nearby-airport flight combinations, compare low-price options, and present concise route guidance. The artifact states it is for technical learning and research use and should not be used for commercial services or purchasing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser automation against travel platforms can create account or policy-compliance issues and stores reusable login cookies on disk.

Mitigation: Install only if comfortable with those behaviors; use a secondary account, avoid payment or account-management actions through automation, and delete ~/.qvxian and ~/.qvxianjiuguo when done.

Risk: Flight prices, availability, and route details may be inaccurate or stale.

Mitigation: Verify prices, booking details, and account-sensitive actions through official travel sites or apps before purchasing or relying on results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaoyiyebuaijianghua/skills/qvxianjiuguo-skills)
- [uv documentation](https://docs.astral.sh/uv/)
- [Qunar flight search](https://flight.qunar.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and summarized flight-search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include top flight results, login guidance, and nearby-airport ground-transport notes.]

## Skill Version(s):

3.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
