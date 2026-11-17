## Description:

A workflow skill for planning and debugging AI image generation or editing work by turning a visual goal into prompt packs, reference-image instructions, retry budgets, and visual QA checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, skill authors, and teams use this skill to turn AI image generation or editing goals into prompt packs, reference-image plans, QA checks, and bounded retry plans. It also helps diagnose failed outputs caused by prompt ambiguity, reference mismatch, model limits, queue or cost issues, and setup problems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate more often than intended in environments that honor broad Chinese trigger metadata or implicit invocation.

Mitigation: Review trigger metadata before deployment and prefer explicit invocation in environments where broad activation would be disruptive.

Risk: Image-workflow guidance, prompts, QA checks, or retry plans may still be incomplete for a user's specific model, tool, brand, licensing, or safety constraints.

Mitigation: Have users review generated workflows against their model limits, brand rules, safety requirements, and export criteria before production use.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-nano-banana-workflow-helper-130446)
- [Nano Banana Pro Demand Signal](https://clawhub.ai/skills/nano-banana-pro)
- [Nano PDF Demand Signal](https://clawhub.ai/skills/nano-pdf)
- [AI Image and Video Generation Experience Discussion](https://www.v2ex.com/t/1222073)
- [Guided First Deployment Feature Request](https://github.com/Makerspace-Ashoka/smart-db/issues/25)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration instructions]

**Output Format:** [Markdown with prompt packs, QA checklists, retry plans, and optional configuration checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should name unresolved model or tool limits and keep retry decisions bounded by an explicit budget.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
