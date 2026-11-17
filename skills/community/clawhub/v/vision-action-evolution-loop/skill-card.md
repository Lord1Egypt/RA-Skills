## Description:

A vision-action-evolution loop framework that combines perception, planning, execution, evaluation, and evolution into a self-iterating embodied cognition cycle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kingofzhao](https://clawhub.ai/user/kingofzhao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to structure an agent workflow that turns visual inputs into staged 2D detection, 3D spatial reasoning, action planning, execution review, and iterative model updates for embodied AI tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow describes robot-arm execution without clear user-controlled safety limits.

Mitigation: Use the skill only in simulation or a supervised, physically safe workcell until human approval, collision checks, force and speed limits, and emergency-stop controls are defined.

Risk: The workflow describes self-updating behavior that can change the internal world model over repeated cycles.

Mitigation: Require update logging, confidence thresholds, review gates, and rollback controls before allowing any persisted evolution step.

Risk: The skill depends on related skills for visual detection, self-evolution, human review, and paper discovery.

Mitigation: Pin and review related skills before installation and re-scan the assembled workflow before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kingofzhao/skills/vision-action-evolution-loop)
- [Publisher profile](https://clawhub.ai/user/kingofzhao)
- [Project homepage](https://github.com/KingOfZhao/AGI_PROJECT)
- [Vlaser: Synergistic Embodied Reasoning](https://arxiv.org/abs/2510.11027)
- [Efficient VLA Models for Embodied Manipulation](https://arxiv.org/abs/2510.17111)
- [From 2D CAD to 3D Parametric via VLM](https://arxiv.org/abs/2412.11892)
- [SAGE: Multi-Agent Self-Evolution](https://arxiv.org/abs/2603.15255)
- [Self-evolving Embodied AI](https://arxiv.org/abs/2602.04411)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe staged visual perception, action planning, robot-arm execution review, feedback injection, and self-update workflows.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
