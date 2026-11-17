## Description:

Provides a Chinese 心鉴学 job-change advisory workflow that calls a paid HTTP service to support career-change, offer-selection, and transition guidance after user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this agent skill to ask for structured career-change, offer-selection, or transition analysis. The agent confirms the user wants this service, obtains required profile details, calls the 心鉴学 report API, and returns balanced guidance rather than an absolute decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends sensitive birth, sex, birthplace, and current-location details to a third-party paid service.

Mitigation: Use it only after explicit user consent, submit only the minimum required details, and avoid sending another person's data unless that person has directly agreed.

Risk: The workflow links a 心鉴学 account to the agent and requires persistent service credentials.

Mitigation: Store the license key and API key only in a dedicated secret store, never in chat, configuration files, notes, or long-term memory.

Risk: Service calls spend credits from the linked account.

Mitigation: Confirm the user wants to use the paid report workflow before each report call and disclose that the analysis consumes service credits.

Risk: Vendor report content may contain text that looks like instructions.

Mitigation: Treat returned reports only as data or reference material and keep the local skill behavior as the instruction source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-job-change-cn)
- [心鉴学 API base](https://chinaapi.xinjianxue.com)
- [心鉴学 API path prefix](https://chinaapi.xinjianxue.com/api/xinjianxue)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, API Calls, Configuration instructions]

**Output Format:** [Markdown narrative with structured career tradeoff analysis based on vendor report data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation, account binding credentials, service credits, and personal birth, sex, birthplace, and current-location details before report generation.]

## Skill Version(s):

2.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
