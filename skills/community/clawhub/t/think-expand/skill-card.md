## Description:

Think Expand is an OpenCode-oriented decision core that coordinates listening, viewing, speaking, doing, and learning modules with memory retrieval, event-driven planning, self-healing behavior, and continuous learning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and internal OpenCode users use this skill to route agent inputs through a central planning layer that can retrieve memory, select related modules, suggest next actions, and coordinate local automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Always-on activation, automatic self-healing, and persistent self-evolution can create behavior that continues without clear user control.

Mitigation: Require explicit user approval for activation, recovery, and self-evolution steps, and provide clear disable and deletion controls before deployment.

Risk: Clipboard monitoring and user-pattern profiling can expose sensitive user data.

Mitigation: Disable these behaviors by default, scope collection narrowly, and require informed opt-in before any monitoring or profiling occurs.

Risk: Autonomous importing of remote skills can introduce unreviewed third-party behavior.

Mitigation: Gate all skill imports behind provenance checks, human review, and security scanning before integration.

## Reference(s):

- [Think Expand skill page](https://clawhub.ai/534422530/skills/think-expand)
- [Publisher profile](https://clawhub.ai/user/534422530)
- [RimTalk Expand Memory video](https://www.bilibili.com/video/BV1uLUYBwErw)
- [MC Expand video](https://www.bilibili.com/video/BV1Gw4m1k7FN)
- [Expand and expend vocabulary video](https://www.bilibili.com/video/BV1cX4y1h7mW)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown guidance with inline shell commands and configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task-routing recommendations, memory search commands, status-monitoring commands, and suggested next actions.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
