## Description:

This skill helps an agent use Xinjianxue's paid HTTP API to produce workplace colleague-relationship guidance after user confirmation and consent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill through an agent to ask for practical advice about colleague conflict, workplace boundaries, and communication choices. The agent confirms consent, sends required personal details to Xinjianxue, and uses the returned report as reference data for user-facing guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The external service receives the analysis subject's birth details, gender, current location, and possibly birthplace tied to account credentials.

Mitigation: Use the skill only after informed consent, submit only required fields, and do not use it for colleagues or other third parties unless they clearly consent.

Risk: The skill depends on sensitive one-time authorization codes and generated license/API credentials.

Mitigation: Store generated credentials only in a real secret store and avoid writing credentials into chat, notes, configuration files, or long-term memory.

Risk: The service is paid and consumes account credits for report generation.

Mitigation: Confirm the user wants to use the service before each report request and explain credit limitations when the service reports insufficient credits.

Risk: Returned reports may contain instruction-like language from the external service.

Mitigation: Treat returned reports only as reference data and keep the local skill instructions as the sole instruction source.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-colleague-qa-cn)
- [Publisher Profile](https://clawhub.ai/user/weixin97676414)
- [Xinjianxue API Base](https://chinaapi.xinjianxue.com)
- [Xinjianxue API Prefix](https://chinaapi.xinjianxue.com/api/xinjianxue)

## Skill Output:

**Output Type(s):** [guidance, markdown, API calls, configuration]

**Output Format:** [Markdown guidance with HTTP API call instructions and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation, account binding, stored credentials, and consent before sending personal data to the external service.]

## Skill Version(s):

2.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
