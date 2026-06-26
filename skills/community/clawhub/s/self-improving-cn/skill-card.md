## Description: <br>
Self-reflection + Self-criticism + Self-learning + Self-organizing memory. Agent evaluates its own work, catches mistakes, and improves permanently. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sharemen](https://clawhub.ai/user/sharemen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users install this skill when they want an agent to keep local, cross-session memory about corrections, preferences, work patterns, and reusable self-reflection lessons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores local cross-session memory about corrections, preferences, and work patterns, which can create privacy and persistence tradeoffs. <br>
Mitigation: Install only when this persistence is desired, inspect ~/self-improving periodically, and avoid storing secrets or sensitive personal data. <br>
Risk: Setup and maintenance can create or modify local memory and workspace steering files. <br>
Mitigation: Review the exact files before setup and require confirmation before memory exports, wipes, or heartbeat maintenance changes. <br>
Risk: Learning from weak signals could encode incorrect or overbroad preferences. <br>
Mitigation: Use the documented confirmation flow, avoid inferring from silence, and keep tentative lessons revisable until the user confirms them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sharemen/self-improving-cn) <br>
- [Skill homepage](https://clawic.com/skills/self-improving) <br>
- [Security boundaries](artifact/boundaries.md) <br>
- [Setup guide](artifact/setup.md) <br>
- [Memory operations](artifact/operations.md) <br>
- [Learning mechanics](artifact/learning.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and local file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and maintains local memory files under ~/self-improving/ and may update workspace steering files when the user chooses setup.] <br>

## Skill Version(s): <br>
1.2.16 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
