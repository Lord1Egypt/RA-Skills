## Description:

xzk-money-maker helps users find part-time or gig-work opportunities by sending job-search requests to the 快结荐 platform and returning matched listings with pay, time, location, and signup links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heqq-github](https://clawhub.ai/user/heqq-github)

### License/Terms of Use:

MIT-0

## Use Case:

External users seeking flexible part-time, gig, or temporary work use this skill to request real-time opportunities and receive matched listings from the 快结荐 platform. Agents use it to route eligible earning or job-search prompts into a structured listing response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Job-search or money-making prompts may include personal data and are sent in full to an external test backend.

Mitigation: Ask for user consent before invocation and avoid sending phone numbers, addresses, identity documents, credentials, or detailed resume information unless privacy and redaction controls are documented.

Risk: Broad auto-routing for employment-related phrases can invoke the skill when a user did not expect data to leave the agent environment.

Mitigation: Use explicit confirmation before sending sensitive employment, income, or personal-data requests to the external service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/heqq-github/skills/xzk-money-maker)
- [快结荐 skill API endpoint](https://test-gig-c-api.1haozc.com/api/wx/kjj/v1/customer/skill/call)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text job-listing summaries with pay, time, address, and signup links; API errors are returned as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Signup and mini-program links should be preserved on standalone lines; the API call script uses a 30-second timeout.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
