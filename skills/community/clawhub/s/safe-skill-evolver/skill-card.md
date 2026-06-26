## Description: <br>
Safely create, improve, audit, and refactor OpenClaw skills by analyzing skill content and suggesting diff-based changes that require explicit user confirmation before application. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deathrowsushy](https://clawhub.ai/user/deathrowsushy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to create new OpenClaw skills, improve existing skills, and run read-only quality or safety audits. It is intended for workflows where proposed skill changes should be shown as diffs and applied only after explicit approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A user could approve proposed edits that weaken confirmation, safety, or audit rules in a skill. <br>
Mitigation: Review diffs carefully before approval and reject changes that reduce confirmation gates, safety boundaries, or audit visibility. <br>
Risk: Generated drafts or shell command guidance could be unsuitable for a specific workspace if requirements are ambiguous. <br>
Mitigation: Require clear user intent, inspect proposed drafts and command previews, and keep the workflow in read-only analysis mode when uncertainty remains. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/deathrowsushy/safe-skill-evolver) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with diff previews, audit reports, generated SKILL.md drafts, and optional shell command guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation before file writes or command execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
