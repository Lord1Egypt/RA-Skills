## Description: <br>
Self-reflection + Self-criticism + learning from corrections. Agent evaluates its own work, catches mistakes, and improves permanently. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sieyer](https://clawhub.ai/user/Sieyer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agent users and developers use this skill to let an agent record explicit corrections, confirmed preferences, and self-reflection lessons in local memory so future work can reflect those learned patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Long-lived local memory can retain sensitive or unwanted personal information. <br>
Mitigation: Do not store secrets, credentials, customer data, medical details, or private third-party information; periodically review or delete entries in ~/self-improving/. <br>
Risk: Stored preferences or corrections can become stale, overbroad, or conflict across projects. <br>
Mitigation: Use the skill's confirmation, source-citation, conflict-resolution, and forget/export workflows before relying on retained patterns. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Sieyer/self-improving-1-1-3) <br>
- [Skill homepage](https://clawic.com/skills/self-improving) <br>
- [Setup guide](setup.md) <br>
- [Learning mechanics](learning.md) <br>
- [Security boundaries](boundaries.md) <br>
- [Memory operations](operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and local file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory files under ~/self-improving/ when the agent applies the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.1.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
