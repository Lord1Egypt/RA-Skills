## Description:

This skill helps agents use the Xiaoba AI Interview API to create interview plans, manage candidates, start interview sessions, and retrieve interview results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[changwu](https://clawhub.ai/user/changwu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and recruiting teams use this skill to integrate Xiaoba interview workflows into an agent, including plan creation, candidate setup, interview scheduling, and result retrieval through API calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends candidate and interview data to an external interview API.

Mitigation: Send only necessary candidate and resume fields, obtain candidate consent where required, and review the provider's retention and privacy terms before using real applicant data.

Risk: The Xiaoba API key could be exposed in chat, logs, or request output.

Mitigation: Store the key only in XIAOBA_API_KEY, avoid printing authorization headers, and log only paths, methods, and redacted response summaries.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/changwu/skills/xiaoba-ai-interview)
- [Xiaoba Homepage](https://www.ibaguo.com)
- [Xiaoba API Base URL](https://www.ibaguo.com/api/v1)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash and curl command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and the XIAOBA_API_KEY environment variable.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
