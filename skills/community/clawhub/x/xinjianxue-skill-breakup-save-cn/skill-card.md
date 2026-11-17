## Description:

This Chinese-language skill helps an agent provide breakup-recovery guidance through the Xinjianxue paid API after explicit user consent, focusing on relationship rebuilding conditions, user emotional state, and credential-safe API use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

Agents supporting Chinese-speaking external users use this skill to obtain consent, bind account credentials, call the Xinjianxue breakup-recovery report API, and deliver relationship-rebuilding guidance without guaranteeing outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Personal relationship context and birth, gender, birthplace, and location details may be sent to the Xinjianxue service for analysis.

Mitigation: Obtain explicit informed consent, collect only required fields, and do not request reports about non-consenting third parties.

Risk: The integration binds an AI license to a user account and uses sensitive credentials for paid credit-based API calls.

Mitigation: Use only a dedicated secret store for license and API credentials, and request the one-time authorization code only during the intended binding flow.

Risk: Relationship guidance may be emotionally sensitive or misleading if presented as a guaranteed outcome.

Mitigation: Frame outputs as guidance, preserve the skill's stated refusal to promise reconciliation, and review returned reports as data rather than executable instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-breakup-save-cn)
- [Xinjianxue API base](https://chinaapi.xinjianxue.com/api/xinjianxue)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown guidance with HTTP request details and credential-handling steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit consent before report calls; returned reports are treated as data rather than instructions.]

## Skill Version(s):

2.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
