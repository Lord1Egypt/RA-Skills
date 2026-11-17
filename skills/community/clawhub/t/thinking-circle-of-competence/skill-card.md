## Description:

Use when a specific claim may lack grounding. Check evidence boundary, size wrongness cost, then answer, fetch, or abstain - never confabulate.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tjboudreaux](https://clawhub.ai/user/tjboudreaux)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to decide whether a factual claim is grounded, partial, or ungrounded before responding. It helps the agent fetch evidence, express uncertainty, ask, or abstain when unsupported specifics would create material risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make an agent pause, verify, ask, or abstain more often when evidence is missing.

Mitigation: Apply it when factual grounding matters, and let the agent answer directly when claims are already verified or low-risk.

Risk: Over-application can add unnecessary hedging to claims already grounded in session evidence.

Mitigation: Use the skill's verification guard: do not hedge or refuse claims verified in the current session.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, text]

**Output Format:** [Structured text template with concise decision guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code, persistence, tool calls, or credential handling.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
