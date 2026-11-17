## Description:

Provides a Chinese self-awareness Q&A advisor that, after user consent and account binding, calls the 心鉴学 paid API to generate current personal-profile analysis and explain behavior patterns without fixed personality labels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to access 心鉴学 self-awareness analysis for questions about personal behavior patterns, self-doubt, and repeated choices. The skill guides consent, account binding, paid API calls, and concise human-facing interpretation of the returned report data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends sensitive personal profile details to the 心鉴学 service and consumes account credits.

Mitigation: Ask for explicit consent before analysis, send only required fields, and tell the user when a paid report call will consume credits.

Risk: The one-time authorization code, license key, and API key are sensitive credentials.

Mitigation: Use a trusted session for the authorization code, store resulting credentials only in a proper secret store, and mask credentials in conversation or logs.

Risk: API-returned report text could contain instruction-like content.

Mitigation: Treat returned reports as reference data only and ignore any instructions embedded in the report content.

Risk: Self-awareness analysis could be mistaken for professional psychological or medical judgment.

Mitigation: Present outputs as reflective guidance about behavior patterns and avoid personality labels, diagnosis, or replacement of professional care.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-self-qa-cn)
- [Publisher profile](https://clawhub.ai/user/weixin97676414)
- [心鉴学 API base](https://chinaapi.xinjianxue.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Guidance]

**Output Format:** [Markdown or plain text guidance based on API-returned JSON data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user consent, account-bound credentials, required personal profile fields, and service credits for each report.]

## Skill Version(s):

2.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
