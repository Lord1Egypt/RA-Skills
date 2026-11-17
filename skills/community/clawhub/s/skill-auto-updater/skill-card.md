## Description:

Skill Updater helps update ClawHub-installed skills while preserving local modifications as patch files and reporting merge conflicts for manual review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tempest-01](https://clawhub.ai/user/tempest-01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to preview and apply updates to ClawHub-installed skills while attempting to preserve local edits. It is most useful when a locally modified skill has a newer upstream release and conflicts need to be surfaced before changes are accepted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The update script can rewrite installed skills under OPENCLAW_SKILLS_DIR.

Mitigation: Install only where that write access is acceptable, back up locally edited skills first, and prefer targeting one skill at a time with --skill.

Risk: Dry-run and conflict-recovery behavior may not guarantee local changes are preserved.

Mitigation: Review dry-run output, inspect generated patches or conflict reports, and avoid --discard unless accepting the upstream version is intentional.

Risk: Patch application can fail when local edits overlap with a newer release.

Mitigation: Treat conflict reports as a manual review step and verify the updated skill before relying on it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tempest-01/skills/skill-auto-updater)
- [Publisher Profile](https://clawhub.ai/user/tempest-01)
- [README](artifact/README.md)
- [SKILL](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create patch, backup, and conflict-report files under target skill directories when its update script is executed.]

## Skill Version(s):

1.1.1 (source: evidence.release.version and artifact/_meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
