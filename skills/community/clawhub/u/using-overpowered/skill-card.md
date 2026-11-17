## Description:

Part of the Overpowered skill suite, this skill routes knowledge-work and enterprise-automation tasks through the smallest relevant combination of Overpowered skills and invokes gear-up only when a material execution capability is genuinely missing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raguets](https://clawhub.ai/user/raguets)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, developers, and agents use this skill to choose a minimal set of Overpowered workflow skills for non-trivial organizational knowledge, automation, evidence, decision, and completion tasks. It helps avoid over-composition while preserving controls for risky side effects, unresolved authority, and genuine capability gaps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can route an agent toward companion skills that perform automation or capability generation when justified.

Mitigation: Review the selected companion skills separately before use, especially when the resulting work may have side effects.

Risk: Over-composition can add unnecessary process steps or route work through unrelated skills.

Mitigation: Apply the skill's smallest-relevant-combination rule and stop routing once active skills and runtime capabilities cover the material failure modes.

Risk: Side-effecting automation can be broad, costly, irreversible, or hard to audit.

Mitigation: Use dry-run and human-gates where the skill's routing conditions identify risky side effects or approval boundaries.

## Reference(s):

- [Overpowered suite](https://github.com/raguets/overpowered)
- [ClawHub skill page](https://clawhub.ai/raguets/skills/using-overpowered)

## Skill Output:

**Output Type(s):** [guidance, markdown]

**Output Format:** [Markdown guidance for skill routing and composition]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routing-only skill; produces no executable code or hidden persistence.]

## Skill Version(s):

1.0.2 (source: release metadata; artifact metadata version 0.4.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
