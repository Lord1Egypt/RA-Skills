## Description:

Safely update skills with preview, migration support, and user validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[litiao1224](https://clawhub.ai/user/litiao1224)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to preview, explain, back up, apply, verify, and roll back skill updates while preserving user control over migrations and changed files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill proposes unpinned npx ClawHub commands while helping update installed skills.

Mitigation: Use a pinned or trusted preinstalled ClawHub CLI, review preview diffs, confirm backups, and approve updates or migrations only after understanding changed files and impact.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/litiao1224/skills/skill-update-litiao)
- [Publisher profile](https://clawhub.ai/user/litiao1224)
- [Preview Changes](preview.md)
- [Migration Strategies](migrate.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks and step-by-step update guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include update previews, migration plans, backup locations, rollback instructions, and confirmation prompts.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
