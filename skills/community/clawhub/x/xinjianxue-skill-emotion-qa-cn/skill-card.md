## Description:

Xinjianxue Skill Emotion QA CN helps agents, after explicit user consent, call Xinjianxue's Chinese relationship-advice report API and turn the returned report data into user-facing relationship guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to request Xinjianxue relationship-advice reports for the user or an explicitly consenting subject, then receive concise guidance based on the returned report data. The skill also guides onboarding, credential handling, consent checks, credit-cost disclosure, and relevant API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends sensitive personal details, including birth date or time, gender, birthplace, and current location, to Xinjianxue's external service for report generation.

Mitigation: Request only the required fields after explicit consent, disclose the external service and purpose before calling it, and avoid storing returned reports.

Risk: The skill relies on a one-time authorization code plus license and API credentials that can grant account-bound service access.

Mitigation: Use the authorization code only for binding, store license and API credentials in a secure local secret store, and never write or echo credentials in chat, configuration files, or long-term memory.

Risk: Report generation consumes service credits and may fail if credits are insufficient.

Mitigation: Confirm the user wants the paid report before each call, disclose the credit cost, and follow the documented insufficient-credit handling path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-emotion-qa-cn)
- [Xinjianxue API base](https://chinaapi.xinjianxue.com)
- [Xinjianxue API path prefix](https://chinaapi.xinjianxue.com/api/xinjianxue)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Configuration, Guidance]

**Output Format:** [Markdown or conversational text with HTTP API request and response handling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user consent, service credentials, and current report data; reports are treated as data and are not stored by design.]

## Skill Version(s):

2.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
