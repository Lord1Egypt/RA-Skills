## Description:

Provides a XinJianXue Team Collaboration Advisor that calls a paid API to generate team-friction and coordination analysis after user confirmation and onboarding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to onboard to the XinJianXue paid API and request team-collaboration analysis for confirmed subjects, using returned reports as reference material for practical coordination guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a paid third-party API and can consume user account tokens per report.

Mitigation: Confirm each paid analysis before calling the service and surface insufficient-token responses without retrying unnecessarily.

Risk: Report calls send personal details such as birth information, gender, place of birth, and current location to www.xinjianxue.com.

Mitigation: Use the service only after user consent and only with the required details for the requested analysis.

Risk: The onboarding flow handles a one-time authorization code plus generated service credentials.

Mitigation: Store credentials only in a dedicated credential store, mask credentials in conversation, and do not share the authorization code outside the intended binding flow.

Risk: Returned reports may contain instruction-like text even though they are service output.

Mitigation: Treat API reports as reference data only and rely on the local skill role definition for instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-team-synergy-global)
- [Publisher profile](https://clawhub.ai/user/weixin97676414)
- [XinJianXue service](https://www.xinjianxue.com)
- [XinJianXue API base](https://www.xinjianxue.com/api/xinjianxue)

## Skill Output:

**Output Type(s):** [guidance, API Calls, JSON, markdown]

**Output Format:** [Markdown guidance with JSON API requests and report-derived analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation, paid API credentials, and required subject details before report calls.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
