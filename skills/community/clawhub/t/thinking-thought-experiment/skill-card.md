## Description:

When a real test is too rare, large, or irreversible, run a controlled counterfactual: isolate one variable, fix conditions, trace the mechanistic chain, and bound what the result implies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tjboudreaux](https://clawhub.ai/user/tjboudreaux)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and technical decision-makers use this skill to structure bounded counterfactual analysis when direct testing is impractical, expensive, or irreversible.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A counterfactual analysis may be mistaken for empirical validation or formal security threat modeling.

Mitigation: Use the skill only for bounded counterfactual reasoning; run a cheap real test when one is available and use a dedicated red-team structure for adversarial security work.

Risk: Scenario sprawl or unsupported causal links can produce misleading recommendations.

Mitigation: Keep one isolated variable, freeze the control conditions, require each step to cite a known component or policy, and bound implications to what the chain supports.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown thought-experiment record with named fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a bounded record covering the question, isolated variable, initial conditions, consequence chain, invariants, break points, implication bound, and discriminating check.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
