## Description: <br>
Self-reflection + Self-criticism + Self-learning + Self-organizing memory. Agent evaluates its own work, catches mistakes, and improves permanently. Use before starting work and after responding to the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanghan0501](https://clawhub.ai/user/wanghan0501) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to maintain local execution-improvement memory, learn from explicit corrections, reflect after significant work, and retrieve relevant project or domain patterns before future tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local memory can persist corrections, preferences, and work patterns longer than intended. <br>
Mitigation: Use Passive or Strict mode, review ./self-improving/ periodically, and use the documented forget or forget everything commands when memory should be removed. <br>
Risk: Sensitive information could be written into local memory if the agent records inappropriate categories. <br>
Mitigation: Follow the documented security boundaries: do not store credentials, financial data, medical information, third-party personal information, location patterns, or access patterns. <br>
Risk: Setup guidance may propose changes to AGENTS.md, SOUL.md, or HEARTBEAT.md that alter future agent behavior. <br>
Mitigation: Inspect proposed steering-file changes before applying them and keep additions non-destructive. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wanghan0501/self-improving-with-reflection) <br>
- [Skill homepage](https://clawic.com/skills/self-improving-with-reflection) <br>
- [Security boundaries](artifact/boundaries.md) <br>
- [Setup guide](artifact/setup.md) <br>
- [Memory operations](artifact/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with file templates and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and maintains local markdown memory files under ./self-improving/.] <br>

## Skill Version(s): <br>
1.2.11 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
