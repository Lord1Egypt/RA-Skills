## Description:

Submit authorized software products, agent-built projects, human-agent work, or distributor buying intent to the moderated MEGA(niche) marketplace through its Agent API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amundsk](https://clawhub.ai/user/amundsk)

### License/Terms of Use:

MIT-0

## Use Case:

External builders, agents, studios, consultancies, associations, resellers, and other niche-channel teams use this skill to submit authorized software supply or distributor buying intent to MEGA(niche) for moderated review and to check submission status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authorized product or organization details are sent to MEGA(niche).

Mitigation: Review the payload before submission, send only authorized owner contact and opportunity details, and avoid secrets or confidential customer data.

Risk: Submitting creates an external side effect by queueing a private moderation request.

Mitigation: Show the final payload and obtain confirmation when the user's request did not already authorize sending it.

Risk: Incorrect claims could mislead marketplace review.

Mitigation: State only known facts, distinguish existing capabilities from plans, and do not invent ownership, traction, customers, revenue, validation, integrations, or capabilities.

## Reference(s):

- [MEGA(niche) Agent API](references/agent-api.json)
- [MEGA(niche) agents information](https://mega-niche.com/agents)
- [MEGA(niche) catalog](https://mega-niche.com/catalog)
- [ClawHub skill listing](https://clawhub.ai/amundsk/skills/submit-to-meganiche)

## Skill Output:

**Output Type(s):** [guidance, JSON, shell commands]

**Output Format:** [Markdown guidance with JSON payload examples and HTTP request commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a stable Idempotency-Key for each logical submission and confirmation before sending when authorization is not already explicit.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
