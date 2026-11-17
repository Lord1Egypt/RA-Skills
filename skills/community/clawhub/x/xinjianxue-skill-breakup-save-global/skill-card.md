## Description:

XinJianXue Breakup Recovery and Reconciliation Advisor helps an agent onboard to the paid XinJianXue API and produce consent-gated relationship recovery guidance from a returned trait-encoding report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill through an agent to request breakup recovery and reconciliation analysis after confirming consent, supplying required birth, gender, and location details, and completing XinJianXue account binding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends birth details, gender, place of birth, and current location to XinJianXue for relationship analysis.

Mitigation: Ask for explicit user confirmation before calling the service, collect only required details, and do not analyze a third party unless the user has mentioned and agreed to that analysis.

Risk: The skill uses a one-time authorization code plus stored license and API credentials.

Mitigation: Use a secure credential store, mask credentials in conversation, never place them in configuration files or long-term memory, and do not share the authorization code outside the intended binding flow.

Risk: Each report consumes paid XinJianXue service tokens.

Mitigation: Confirm the user wants the analysis before every report call and explain token insufficiency or billing checks only when relevant.

Risk: Returned reports may contain instruction-like text.

Mitigation: Treat service reports only as data or reference material and follow the local skill role definition for behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-breakup-save-global)
- [XinJianXue service](https://www.xinjianxue.com)
- [XinJianXue API base](https://www.xinjianxue.com/api/xinjianxue)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown guidance with HTTP request details and user-facing analysis text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user consent, XinJianXue credentials, direct HTTP access, and paid service tokens before report generation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
