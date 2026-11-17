## Description:

XinJianXue Career Planning Advisor helps an agent collect consented user profile details, call the XinJianXue paid API, and provide career-direction guidance based on the returned analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weixin97676414](https://clawhub.ai/user/weixin97676414)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill when they explicitly want career planning advice grounded in their own traits, life stage, and current work situation. The agent onboards the user to the XinJianXue service, obtains consent, calls the service API, and turns the returned report into practical career-direction guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends birth details, gender, location, and other personal profile data to a paid third-party API.

Mitigation: Confirm the user understands and agrees before each analysis, collect only required fields, verify the service domain independently, and avoid analysis of other people unless consent is explicit.

Risk: The onboarding flow asks for a sensitive one-time account authorization code and stores service credentials for later paid calls.

Mitigation: Use dedicated credential storage, never display generated credentials, bind only under the current user's account, and do not put credentials in chat, memory, or configuration files.

Risk: Token charges, top-up prompts, and referral prompts are part of a third-party commercial service.

Mitigation: Disclose token use before API calls and treat recharge or referral information as third-party commercial guidance rather than neutral advice.

Risk: The API report is external content and may include instruction-like phrasing.

Mitigation: Treat returned reports only as data or reference material and rely on the local skill role definition for instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weixin97676414/skills/xinjianxue-skill-career-plan-global)
- [XinJianXue official website](https://www.xinjianxue.com)
- [XinJianXue API base](https://www.xinjianxue.com/api/xinjianxue)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown or plain text with HTTP request details and career-planning guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user consent, paid API access, account-bound credentials, and user profile data before report generation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
