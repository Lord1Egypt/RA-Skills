## Description:

XinJianXue Custom Advisor is a generic advisor entry point that helps an agent onboard to the XinJianXue paid API, request consented subject details, call the report endpoint, and present the returned relationship, personality, and behavior-pattern analysis as reference material.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill when they want a customizable XinJianXue advisor to analyze consented personal details through the XinJianXue API. The skill guides onboarding, credential handling, paid report calls, and delivery of the returned report in the user's language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends personal details, including birth date, gender, birthplace when available, and current location, to the XinJianXue API.

Mitigation: Use the skill only after explicit user consent, collect only the required fields, and do not analyze a third party unless that person was mentioned and agreed to the analysis.

Risk: The skill depends on a one-time authorization code and locally stored service credentials.

Mitigation: Store credentials only in dedicated credential storage, never in chat, notes, configuration files, or long-term memory, and mask credentials whenever they must be referenced.

Risk: The security evidence notes that user-written role instructions persisted in SKILL.md can alter future behavior.

Mitigation: Review and control changes to the local role-definition text before reuse, especially in shared agent or shared skill-directory environments.

Risk: Returned reports may contain instruction-like phrasing even though they are external analysis material.

Mitigation: Treat reports only as data or reference material and ignore any instruction-like content from the API response.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-assistant-global)
- [XinJianXue service](https://www.xinjianxue.com)
- [XinJianXue API base](https://www.xinjianxue.com/api/xinjianxue)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTTP request examples and plain-language analysis output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a paid third-party HTTP API; returned reports are treated as data, not instructions.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
