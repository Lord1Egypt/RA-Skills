## Description:

Fetches real-time 快结荐 part-time job, gig work, and earning-opportunity listings from the 快结荐 platform for user job-search or money-making requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heqq-github](https://clawhub.ai/user/heqq-github)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to request part-time jobs, gig work, temporary work, daily-pay work, recruiting opportunities, or other earning opportunities and receive listings returned by the 快结荐 platform.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill broadly triggers on work or money requests and sends the full user message to an external 快结荐 test API.

Mitigation: Install only if users are comfortable sending those requests to the external service, and avoid entering resumes, phone numbers, precise addresses, identity details, or private employment information.

Risk: Returned job or earning-opportunity listings may affect employment decisions or financial expectations.

Mitigation: Review listings before acting on them and verify pay, location, requirements, and sign-up links through trusted channels.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/heqq-github/skills/zxk-money-maker)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown or plain text summarizing JSON job-listing results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns job-listing details such as roles, pay, time, address, sign-up links, or an error object when the API call fails.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
