## Description: <br>
Self-reflection, self-criticism, self-learning, and self-organizing memory for agents to evaluate their own work, catch mistakes, and improve permanently. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[taron-ai](https://clawhub.ai/user/taron-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add local self-reflection, correction logging, and preference memory workflows to an agent. It is intended for situations where an agent should learn from explicit corrections, repeated patterns, failed operations, or post-task reflection while keeping the memory files visible to the user. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create persistent local memory of user corrections, preferences, and work patterns. <br>
Mitigation: Install it only when persistent local memory is desired, inspect ~/self-improving/ periodically, and avoid storing sensitive information there. <br>
Risk: Workspace steering files such as AGENTS.md, SOUL.md, and HEARTBEAT.md may be edited during setup. <br>
Mitigation: Review proposed edits to workspace steering files before accepting them. <br>
Risk: The documented forget-everything flow may export memory before wiping it. <br>
Mitigation: Treat full-memory deletion carefully and confirm whether an export should be created before removing stored data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/taron-ai/self-improving-1-2-16) <br>
- [Skill homepage](https://clawic.com/skills/self-improving) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Setup guide](artifact/setup.md) <br>
- [Security boundaries](artifact/boundaries.md) <br>
- [Learning mechanics](artifact/learning.md) <br>
- [Memory operations](artifact/operations.md) <br>
- [Heartbeat rules](artifact/heartbeat-rules.md) <br>
- [Scaling patterns](artifact/scaling.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory file structures, workspace steering snippets, maintenance guidance, and user-facing memory summaries.] <br>

## Skill Version(s): <br>
1.2.16 (source: artifact/SKILL.md frontmatter); release package 1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
