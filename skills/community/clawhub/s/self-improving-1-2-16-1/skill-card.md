## Description: <br>
Self-improving agent memory skill that helps agents learn from explicit corrections, self-reflection, and repeated patterns while storing preferences and lessons in local files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaoyu-157](https://clawhub.ai/user/xiaoyu-157) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to retain explicit corrections, preferences, and reusable lessons across work sessions. It is intended for local, transparent memory management with confirmation-oriented promotion rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local memory files may retain corrections, preferences, or project context that the user did not intend to preserve long term. <br>
Mitigation: Review ~/self-improving/ periodically, avoid storing secrets or sensitive personal or project data, and use stricter confirmation settings when entries should require approval. <br>
Risk: Workspace steering changes can persistently affect future agent behavior. <br>
Mitigation: Review proposed changes to AGENTS.md, SOUL.md, and HEARTBEAT.md before accepting them, and keep memory actions transparent and reversible. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xiaoyu-157/skills/self-improving-1-2-16-1) <br>
- [Skill Homepage](https://clawic.com/skills/self-improving) <br>
- [Security Boundaries](artifact/boundaries.md) <br>
- [Setup Guide](artifact/setup.md) <br>
- [Learning Mechanics](artifact/learning.md) <br>
- [Memory Operations](artifact/operations.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, file templates, and local configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains local markdown memory under ~/self-improving/ and may propose workspace steering updates for AGENTS.md, SOUL.md, or HEARTBEAT.md.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release; skill frontmatter version 1.2.16) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
