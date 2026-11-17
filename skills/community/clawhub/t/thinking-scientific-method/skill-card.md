## Description:

When a symptom has several plausible causes, rank falsifiable hypotheses and run the cheapest discriminating observation first; prefer least-assumptive survivors only after evidence fit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tjboudreaux](https://clawhub.ai/user/tjboudreaux)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to troubleshoot bugs, incidents, and anomalies by comparing falsifiable hypotheses and running the cheapest observation that distinguishes among them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents using the skill may inspect task-relevant files, logs, tests, configurations, or data during troubleshooting.

Mitigation: Use the skill only in workspaces where that diagnostic access is appropriate and keep observations scoped to the reported symptom.

Risk: The method can produce misleading guidance if applied after a single obvious cause is already evidenced or if hypotheses lack falsifiers.

Mitigation: Follow the skill's verification guards: use at least two serious hypotheses, name falsifiers before checking, and stop once the fault is directly localized.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Markdown or plain text diagnostic record with symptom, hypotheses, test order, results, survivors, localized fault, and ruled-out causes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No hidden execution, persistence, or data-sharing behavior; may lead the agent to inspect task-relevant files, logs, tests, configurations, or data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
