## Description: <br>
Build a self-evolving memory and learning system for an AI assistant on OpenClaw using a three-layer memory architecture, self-improvement workflow, and reusable templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shu0yu](https://clawhub.ai/user/shu0yu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users and developers use this skill to set up local memory files, work logs, and self-improvement records that help an AI assistant preserve user preferences and learn from corrections over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect persistent local memory files that shape future agent behavior. <br>
Mitigation: Back up the workspace before use, review templates before copying them over existing files, and keep memory updates under explicit user control. <br>
Risk: The "整理一下" workflow may read and organize memory files that contain personal or project context. <br>
Mitigation: Treat that phrase as an explicit command, review what will be read or written, and pause or skip memory loading when sensitive context should not be used. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/shu0yu/self-evolving-blueprint) <br>
- [Three-layer memory architecture](references/architecture.md) <br>
- [Self-evolution workflow](references/self-evolution.md) <br>
- [Workflows and rules](references/workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and template files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local workspace templates and operating guidance; users review, copy, and adapt the files before use.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
