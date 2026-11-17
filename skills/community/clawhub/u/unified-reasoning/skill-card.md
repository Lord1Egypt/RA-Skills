## Description:

Unified Reasoning Engine with FoT optimization - Combines ToT, GoT, Self-Consistency, and Meta-Reasoning with parallel execution and caching for 2-5x speedup

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobisamaa](https://clawhub.ai/user/tobisamaa)

### License/Terms of Use:


## Use Case:

Developers and external agent users use this skill to route reasoning, analysis, decision, and planning requests through advertised strategies such as Chain of Thought, Tree of Thoughts, Graph of Thoughts, Self-Consistency, and Meta-Reasoning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The advertised reasoning engine implementation is not included in the artifact.

Mitigation: Require the publisher to ship the implementation or clearly document the missing dependency before deployment.

Risk: The wrapper can delegate execution to an unspecified local Python implementation file if one exists.

Mitigation: Review delegated code before installation and allow only an expected class or interface to be loaded.

Risk: The skill can claim high confidence for broad requests involving reasoning, thinking, analysis, decisions, or planning.

Mitigation: Use explicit activation boundaries and human review for sensitive planning or decision-support workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tobisamaa/skills/unified-reasoning)
- [ClawHub Publisher Profile](https://clawhub.ai/user/tobisamaa)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with code blocks and structured reasoning result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advertised outputs may include strategy, solution, confidence, duration, timestamp, threshold status, and strategy-specific details.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
