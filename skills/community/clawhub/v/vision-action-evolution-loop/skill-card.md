## Description: <br>
视觉-动作-进化闭环框架 —— 将感知、规划、执行、评估、进化五阶段融合为自迭代认知循环 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kingofzhao](https://clawhub.ai/user/kingofzhao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to structure an embodied AI workflow that connects visual perception, planning, execution, evaluation, and iterative learning. It is intended for agents exploring 2D detection, 3D spatial understanding, action planning, feedback, and self-updating knowledge loops. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes physical robot actions and automation loops without enough safety limits or user control. <br>
Mitigation: Use only in a scoped workspace and require explicit human confirmation before any real-world action or hardware control. <br>
Risk: The skill describes recurring heartbeat tasks and self-updating memory that could persist or change behavior over time. <br>
Mitigation: Disable or tightly control heartbeat tasks, and review memory or world-model updates before enabling persistent operation. <br>
Risk: Separate implementation code could add file, tool, robotics, or external-system behavior not visible in the documentation-only artifact. <br>
Mitigation: Inspect implementation code and run security review before connecting the skill to external tools, files, robotics, or automation systems. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kingofzhao/vision-action-evolution-loop) <br>
- [Project homepage](https://github.com/KingOfZhao/AGI_PROJECT) <br>
- [Vlaser: Synergistic Embodied Reasoning](https://arxiv.org/abs/2510.11027) <br>
- [Efficient VLA Models for Embodied Manipulation](https://arxiv.org/abs/2510.17111) <br>
- [From 2D CAD to 3D Parametric via VLM](https://arxiv.org/abs/2412.11892) <br>
- [SAGE: Multi-Agent Self-Evolution](https://arxiv.org/abs/2603.15255) <br>
- [Self-evolving Embodied AI](https://arxiv.org/abs/2602.04411) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline code and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe action plans, confidence values, feedback records, and knowledge updates for a closed-loop agent workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, README, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
