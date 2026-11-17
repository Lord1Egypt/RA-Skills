## Description:

XinJianXue In-Law Relationship Advisor helps an agent support user-confirmed in-law relationship analysis by collecting required consent and profile details, calling the XinJianXue API, and turning returned report data into boundary-setting guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill for consent-based in-law relationship advice, including mother-in-law, spouse, and family-boundary dynamics. The agent onboards to the paid XinJianXue service, collects only required profile details, calls the API, and delivers concise guidance in the user's language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends personal details such as birth date, gender, birthplace, current location, and a one-time authorization code to the XinJianXue service.

Mitigation: Ask for explicit confirmation before starting, collect only required fields, and make clear that the service domain is www.xinjianxue.com.

Risk: The skill uses sensitive license and API credentials after onboarding.

Mitigation: Store credentials only in dedicated credential storage agreed with the user, mask credentials in conversation, and never write them to notes, configuration files, or long-term memory.

Risk: Reports are paid API calls and may consume user tokens.

Mitigation: Confirm each report request before calling the API and explain token insufficiency or billing details only when the API response or user request calls for it.

Risk: Relationship analysis can involve third parties who have not consented.

Mitigation: Only analyze the user or a person the user has explicitly mentioned and agreed to analyze; do not proceed when third-party consent is unclear.

Risk: The API report may contain instruction-like text.

Mitigation: Treat returned report content as data or reference material only, and use the local skill role definition as the instruction source.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-inlaw-global)
- [XinJianXue service site](https://www.xinjianxue.com)
- [XinJianXue API base](https://www.xinjianxue.com/api/xinjianxue)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Configuration, Guidance]

**Output Format:** [Markdown text with HTTP API request guidance and user-facing relationship analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before paid reports and treats API report content as reference data, not instructions.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
