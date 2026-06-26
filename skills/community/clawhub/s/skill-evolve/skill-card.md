## Description: <br>
Skill Evolve helps an agent turn lessons from non-trivial tasks into reusable SKILL.md files for future workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lorinwei](https://clawhub.ai/user/lorinwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to decide when useful workflow experience should become a persistent skill, and to create, update, inspect, or retire SKILL.md files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to create, edit, or delete persistent skills without enough user-control safeguards. <br>
Mitigation: Require explicit user approval before creating, editing, or deleting any skill, and keep backups of the skills directory. <br>
Risk: Generated SKILL.md files may contain incorrect assumptions, unsafe workflow guidance, or accidental secrets. <br>
Mitigation: Review generated SKILL.md files before use and scan them for secrets or unsafe instructions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lorinwei/skill-evolve) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces persistent skill-management guidance and SKILL.md content; generated skills should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
