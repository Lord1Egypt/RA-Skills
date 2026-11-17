## Description:

Teach agents how to design, implement, explain, and debug gameplay randomness with the RNGNeeds Unity plugin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[starphaselab](https://clawhub.ai/user/starphaselab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical agents use this skill to choose RNGNeeds Unity patterns, generate focused C# examples, explain probability behavior, and debug gameplay randomness setups such as loot tables, gacha, repeat prevention, influence providers, depletable lists, and ordered card decks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Unity/C# examples may not match the installed RNGNeeds package version or a project's gameplay architecture.

Mitigation: Review generated gameplay code before use and check local RNGNeeds package documentation or source when API details are uncertain.

Risk: Incorrectly choosing between weighted picks, depletable lists, repeat prevention, and deck-order operations can produce misleading probability or card-flow behavior.

Mitigation: Use the skill's decision guidance to select the RNGNeeds mechanic that matches the gameplay requirement, then test probability and deck behavior in the Unity project.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/starphaselab/skills/rngneeds-unity)
- [API Surface](references/api-surface.md)
- [Common Patterns](references/common-patterns.md)
- [Core Concepts](references/core-concepts.md)
- [Decision Guide](references/decision-guide.md)
- [Examples](references/examples.md)
- [Guide Workflows](references/guide-workflows.md)
- [Pitfalls](references/pitfalls.md)
- [Test Prompts](references/test-prompts.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Configuration instructions]

**Output Format:** [Markdown with concise Unity/C# code blocks when code is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Grounded in RNGNeeds terminology and API names; generated gameplay code should be reviewed for project fit.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
