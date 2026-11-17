## Description:

ClawTrace observes, reconstructs, records, and explains AI workflow runtime behavior from trace logs without modifying workflow state, context, prior outputs, or skill outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallkeyboy](https://clawhub.ai/user/smallkeyboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect AI workflow execution, reconstruct skill call chains, and understand retry, fallback, critic, arbitration, recovery, and context-integrity behavior from available runtime traces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runtime traces can expose complete prompts, outputs, workflow context, secrets, or private data.

Mitigation: Use explicit operator authorization, scoped diagnostic sessions, trace redaction, and tenant or workflow isolation.

Risk: Weak activation controls can make diagnostic inspection available in contexts where users should not see full workflow logs.

Mitigation: Restrict debug triggers to authorized operators and avoid enabling the skill for general users or sensitive production contexts.

## Reference(s):


## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance]

**Output Format:** [JSON diagnostic trace report with concise explanatory text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a need_retry trace response when required trace logs are missing or incomplete.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
