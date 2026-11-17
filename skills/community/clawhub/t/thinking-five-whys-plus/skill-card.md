## Description:

When a fault is localized and the proximate cause is known but the systemic root is not, chain evidence-linked whys with a counterfactual stop and a countermeasure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tjboudreaux](https://clawhub.ai/user/tjboudreaux)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, support responders, and incident reviewers use this skill after a fault has been localized to build an evidence-linked causal chain, retain independent causal branches, and define recurrence-preventing countermeasures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Applying the skill before a fault is localized can produce premature or misleading root-cause conclusions.

Mitigation: Use the skill only after the component, path, or subsystem and proximate cause are known; stop and gather localization evidence when they are not.

Risk: Speculative or blame-oriented why-chains can lead to weak countermeasures.

Mitigation: Require evidence for each causal step, rule out alternatives, test each retained pathway counterfactually, and continue past human error to the enabling condition.

Risk: Troubleshooting evidence may include data outside the intended investigation scope.

Mitigation: Limit reviewed logs, code, configuration, metrics, and witness input to evidence appropriate for the localized troubleshooting task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tjboudreaux/skills/thinking-five-whys-plus)
- [Publisher profile](https://clawhub.ai/user/tjboudreaux)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown or structured text root-cause analysis with causal chains, evidence, counterfactual checks, countermeasures, and verification steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a localized fault and known proximate cause; directs the agent to stop when evidence is missing or the problem is still pre-localization.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
