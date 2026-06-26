## Description: <br>
Memoria gives OpenClaw a durable external memory slot for storing, retrieving, correcting, forgetting, snapshotting, rolling back, branching, and merging cross-session memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[randomradio](https://clawhub.ai/user/randomradio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill when they want an agent to retain durable user or project memory across sessions, retrieve relevant prior context, and safely repair or remove stored memories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Long-term memory can retain sensitive, obsolete, or unwanted user and project information. <br>
Mitigation: Store only durable information, avoid secrets unless explicitly required, and periodically review, correct, forget, purge, or roll back saved memories. <br>
Risk: Setup can involve API keys and optional commands that fetch installer or source material. <br>
Mitigation: Keep API keys out of shared logs and screenshots, and inspect or trust the installer or source before running optional local setup commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/randomradio/thememoria) <br>
- [Memoria homepage](https://github.com/matrixorigin/Memoria) <br>
- [OpenClaw Setup](references/setup.md) <br>
- [Tool Surface](references/tool-surface.md) <br>
- [Memory Slot Operations](references/operations.md) <br>
- [Usage Patterns](references/patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are agent-facing operational guidance for choosing and using Memoria memory tools.] <br>

## Skill Version(s): <br>
0.2.0 (source: SKILL.md frontmatter and ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
