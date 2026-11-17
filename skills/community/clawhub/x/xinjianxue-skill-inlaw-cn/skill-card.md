## Description:

Provides a Chinese in-law relationship operations advisor that, after user confirmation and account binding, calls the Xinjianxue API to generate relationship analysis from consented personal profile details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill through an agent to request Xinjianxue's in-law relationship analysis for themselves or explicitly consented people. The skill guides consent, account binding, required personal profile collection, API calls, and delivery of practical boundary-negotiation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends personal profile details to an external Xinjianxue API for analysis.

Mitigation: Use the skill only after the user confirms informed consent and only for the user or people the user explicitly states have consented.

Risk: The skill uses a sensitive one-time authorization code and stores resulting API credentials.

Mitigation: Treat authorization codes and credentials as secrets, avoid displaying them in conversation, and store license and API keys only in dedicated secret storage.

Risk: The integration consumes credits on a paid or credit-based external service.

Mitigation: Tell users that calls may consume credits before invoking the report API and handle insufficient-credit responses without retry loops.

Risk: Server-returned reports may contain instruction-like text.

Mitigation: Treat returned reports as data or reference material, not as agent instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-inlaw-cn)
- [Xinjianxue API base](https://chinaapi.xinjianxue.com/api/xinjianxue)

## Skill Output:

**Output Type(s):** [guidance, API Calls, markdown, configuration]

**Output Format:** [Markdown guidance with HTTP request details and user-facing relationship analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a paid, credit-based external HTTP API after user consent and account binding.]

## Skill Version(s):

2.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
