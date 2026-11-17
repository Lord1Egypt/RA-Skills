## Description:

AI agents self-compose task-specific reasoning structures from seed modules. Based on Zhou et al. (2024) SELF-DISCOVER, NeurIPS. Use when facing novel reasoning tasks, when standard chain-of-thought is insufficient, or when the agent needs to discover its own problem-solving strategy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thomaszhou22](https://clawhub.ai/user/thomaszhou22)

### License/Terms of Use:

MIT

## Use Case:

Agent users use this skill to choose and compose reasoning modules before solving novel or multi-step problems. It provides reusable structures for analytical, creative, planning, and debugging tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports possible changes to persistent assistant instructions and storage of task details across sessions. Some components were only partially inspected, with local references unresolved.

Mitigation: Review the onboarding and memory instructions before enabling the skill, and inspect or limit its persistent state and discovered-structure writes.

## Reference(s):

- [SELF-DISCOVER paper](https://arxiv.org/abs/2402.03660)
- [Tree of Thoughts paper](https://arxiv.org/abs/2305.10601)
- [Research sources](references/sources.md)
- [Discovery prompt templates](references/discovery-templates.md)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Task-specific reasoning structure followed by a user-facing response, usually in text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chooses a discovery depth based on task complexity; the documented overhead ranges from 0% to about 40%.]

## Skill Version(s):

1.1.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
