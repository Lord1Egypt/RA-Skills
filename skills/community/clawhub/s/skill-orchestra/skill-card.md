## Description:

Skill-aware agent routing with explicit competence/cost modeling. +22.5% accuracy, 700x cheaper than RL routers. Based on arXiv:2602.19672.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobisamaa](https://clawhub.ai/user/tobisamaa)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to route tasks to suitable skills or agents by comparing task demands, competence, cost, and recent performance signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Future pattern-learning examples may keep or learn from routing decisions.

Mitigation: Review any enabled history or pattern-learning storage before deployment and avoid storing sensitive task context unless retention is intended.

Risk: The bundled wrapper and documentation are incomplete, which may cause functional failures in an agent runtime.

Mitigation: Test routing, wrapper loading, and model-router integration in a staging runtime before relying on the skill for production routing.

## Reference(s):

- [ClawHub Skill Orchestra release page](https://clawhub.ai/tobisamaa/skills/skill-orchestra)
- [SkillOrchestra paper](https://arxiv.org/abs/2602.19672)
- [Research code referenced by artifact](https://github.com/jiayuww/SkillOrchestra)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code examples; runtime routing APIs return strings or dictionaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on model-router integration and local skill catalog state when used in an agent runtime.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
