## Description:

Updates SenseNova Skills (the sn-* bundle) inside an OpenClaw or hermes-agent install, either for all sn-* skills or only specifically named skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sensenova-skills](https://clawhub.ai/user/sensenova-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to refresh installed SenseNova sn-* skills in OpenClaw or hermes-agent environments while preserving scoped updates, version comparison, backups, and concise update reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can replace installed sn-* skills with content from upstream or a user-supplied fork.

Mitigation: Review the source repository or fork URL before allowing updates, and use only trusted repositories.

Risk: Updating installed skills changes active agent behavior.

Mitigation: Review and scan updated skills before deployment, and check the update summary for errors.

Risk: Backup retention keeps only the newest three backup buckets.

Mitigation: Keep separate backups when longer rollback history is required.

## Reference(s):

- [sn-update on ClawHub](https://clawhub.ai/sensenova-skills/skills/sn-update)
- [SenseNova-Skills repository](https://github.com/OpenSenseNova/SenseNova-Skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown status summaries with shell command and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide an agent to replace installed sn-* skill files and maintain backup and version marker files.]

## Skill Version(s):

2026.8.19 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
