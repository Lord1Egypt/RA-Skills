## Description:

Provides an agent with onboarding, consent, authentication, API-call, and response-handling guidance for XinJianXue coworker relationship analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill through an agent to request coworker relationship analysis after explicit consent, account binding, and required personal context collection. The agent uses it to call the XinJianXue service, treat returned reports as reference data, and produce workplace-boundary guidance in the user's language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can share sensitive personal birth, gender, and location details with the XinJianXue service and may consume paid service tokens.

Mitigation: Obtain explicit user confirmation before each analysis, collect only required inputs, disclose token use, and send requests only to the documented XinJianXue service domain.

Risk: The onboarding flow handles sensitive one-time authorization codes and persistent license/API credentials.

Mitigation: Request the authorization code only for account binding, mask credentials in conversation, and store license/API credentials only in dedicated credential storage.

Risk: Returned reports could contain instruction-like phrasing even though they are analysis material.

Mitigation: Treat returned reports only as reference data and follow only the local skill role definition and the user's current request as instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-colleague-qa-global)
- [Publisher profile](https://clawhub.ai/user/weixin97676414)
- [XinJianXue service](https://www.xinjianxue.com)
- [XinJianXue API base](https://www.xinjianxue.com/api/xinjianxue)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline HTTP request details and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include translated user-facing analysis; credentials must be masked and stored only in dedicated credential storage.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
