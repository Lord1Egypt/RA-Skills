## Description:

This skill helps an agent provide mentor-relationship guidance by calling the 心鉴学 service for a consented report and using it as reference material for advice about being recognized by mentors without manipulative tactics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this agent skill to request guidance about mentor, advisor, or senior-peer relationships after confirming they want the 心鉴学 mentor guidance service. The skill gathers required personal profile details with consent, calls a paid HTTP API, and turns the returned Chinese report data into user-facing guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends personal profile details such as birth date, gender, birthplace, and current location to the 心鉴学 service.

Mitigation: Confirm user consent before collecting or sending the details, and only analyze the user or another person who has been explicitly identified and consented.

Risk: Setup requires a sensitive one-time authorization code and produces long-lived service credentials.

Mitigation: Use the authorization code only for intentional account binding, do not share it broadly, and store the resulting credentials in a dedicated secret store rather than conversation history or configuration files.

Risk: Using the paid API consumes account credits.

Mitigation: Tell users when a report call will use credits and check billing details only when the user asks about credit consumption.

Risk: The returned report could contain text that looks like instructions.

Mitigation: Treat service reports only as data or reference material and follow the local skill role and safety constraints for final guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-mentor-cn)
- [Publisher profile](https://clawhub.ai/user/weixin97676414)
- [心鉴学 API service endpoint](https://chinaapi.xinjianxue.com)

## Skill Output:

**Output Type(s):** [guidance, text, markdown, API calls, configuration]

**Output Format:** [Markdown or plain text guidance, with HTTP request details when setup or diagnostics are needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the user's preferred language for final guidance; returned reports are treated as reference data rather than instructions.]

## Skill Version(s):

2.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
