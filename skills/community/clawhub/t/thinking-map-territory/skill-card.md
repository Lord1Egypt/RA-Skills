## Description:

When a claim, doc, test, metric, or assumption conflicts with observed behavior, stop theorizing from the map and verify the live code or data; let territory overrule.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tjboudreaux](https://clawhub.ai/user/tjboudreaux)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and reviewers use this skill when documentation, tests, metrics, or assumptions conflict with observed behavior so an agent checks current code or data, records the delta, and updates its working model before deciding on a fix.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Verification work may involve live systems or sensitive data even though the skill itself does not request hidden access or broad authority.

Mitigation: Apply normal access controls and data-handling care when choosing territory checks, especially for production systems or confidential datasets.

Risk: Over-applying the workflow can lead to unnecessary re-checking when the mismatch is irrelevant or has already been verified.

Mitigation: Stop once the contradiction is resolved or irrelevant, and reuse verified observations from the same session.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, text, markdown]

**Output Format:** [Structured Markdown-style text using the skill's Map, Territory check, Observation, Delta, Updated model, Action, and Uncovered fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill disables model invocation and produces a bounded reasoning workflow rather than executable code.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
