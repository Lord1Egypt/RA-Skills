## Description:

Conducts autonomous, iterative research by defining goals, generating hypotheses, verifying results, modifying approaches, and repeating until criteria are met.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amdf01-debug](https://clawhub.ai/user/amdf01-debug)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and research-oriented agent users use this skill to run scoped research loops with explicit goals, success criteria, iteration logs, source verification, and confidence labels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases such as "deep dive" may start a more structured iterative research workflow than the user intended.

Mitigation: Use explicit scope, success criteria, and stopping criteria before beginning the research loop.

Risk: Iterative research can consume unnecessary time or paid tool calls if the stopping point is unclear.

Mitigation: Keep the artifact's 10-iteration maximum and stop when the defined success criteria are met.

Risk: Research findings can be incorrect or overconfident if accepted without verification.

Mitigation: Verify findings from multiple sources and label each finding with high, medium, or low confidence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/amdf01-debug/skills/sw-autoresearch)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown research plan, iteration log, and synthesized final output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes success criteria, up to 10 logged iterations per research question, source verification, and confidence levels for findings.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
