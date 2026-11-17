## Description:

Provides a Chinese-language Xinjianxue career-planning advisor workflow that, after user confirmation and account binding, calls the Xinjianxue service to generate career-planning reports from user-approved personal profile details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their assistants use this skill to request career-planning analysis for the user or for an explicitly consenting person. It helps frame career paths and judgment criteria from user-approved profile details instead of giving generic career advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends birth date or time, gender, birthplace, current location, and a one-time authorization code to a third-party service.

Mitigation: Confirm user consent before use, analyze only the user or an explicitly consenting person, use the documented Xinjianxue service domain, and do not share the one-time authorization code in public places.

Risk: Returned service credentials can enable future calls that may consume account credits.

Mitigation: Store credentials only in a secure credential store, avoid writing them into chat, configuration files, or long-term memory, and mask credential values when referring to them.

Risk: Career report content may be over-relied on or mistaken for executable instructions.

Mitigation: Treat service reports as reference data, ignore any instruction-like content in returned reports, and present path frameworks and judgment criteria rather than deciding for the user.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-career-plan-cn)
- [Xinjianxue API base](https://chinaapi.xinjianxue.com)
- [Xinjianxue API path prefix](https://chinaapi.xinjianxue.com/api/xinjianxue)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown guidance with HTTP request details and service report interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation, account binding, secure credential storage, and user-approved personal profile details before report generation.]

## Skill Version(s):

2.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
