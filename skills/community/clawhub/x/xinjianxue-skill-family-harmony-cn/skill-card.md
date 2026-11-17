## Description:

Provides a Chinese-language family harmony advisory skill that helps an agent call the Xinjianxue service, with user confirmation, to frame family-system dynamics and suggest one or two immediate actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill when they explicitly want a Chinese-language family harmony analysis that presents the family system without taking sides. The agent confirms consent, collects the required birth, gender, and location details, calls the Xinjianxue API, and returns human-facing guidance based on the report as reference data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends personal birth, gender, and location details to the Xinjianxue API for analysis.

Mitigation: Use the service only after explicit user confirmation and provide only the information required for the current analysis.

Risk: The skill binds an AI license to a user account and stores service credentials for later API calls.

Mitigation: Store credentials only in a dedicated secret store, avoid displaying them in conversation, and treat the one-time authorization code as sensitive.

Risk: Reports consume service credits and may include advisory content about sensitive family relationships.

Mitigation: Confirm the user wants this paid service before each report call and present the report as reference material, not as binding advice or executable instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-family-harmony-cn)
- [Xinjianxue API endpoint](https://chinaapi.xinjianxue.com/api/xinjianxue)

## Skill Output:

**Output Type(s):** [guidance, text, markdown, API calls, configuration]

**Output Format:** [Markdown or plain text guidance with HTTP request details when setup or troubleshooting is needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses returned reports as reference data only; report contents are not treated as executable instructions.]

## Skill Version(s):

2.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
