## Description:

Publishes completed agent skills to GitHub, ClawHub, and SkillHub with pre-publish safety checks, version checks, repository packaging, and user confirmation before visible external publishing or local synchronization actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[edwardwason](https://clawhub.ai/user/edwardwason)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to prepare and publish completed agent skills across GitHub, ClawHub, and SkillHub while checking version conflicts, packaging rules, and pre-publish security requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing tokens and platform write access can mutate repositories and marketplace releases.

Mitigation: Install only when comfortable granting those credentials, and run authentication on a trusted single-user machine.

Risk: Local synchronization can overwrite installed skill files.

Mitigation: Disable or tightly review the local sync step, and use dry-run review before allowing synchronization.

Risk: All-skills synchronization and installer or authentication steps increase operational impact.

Mitigation: Avoid all-skills sync mode and install required CLIs through verified manual paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/edwardwason/skills/skill-publisher-ai)
- [Project homepage](https://github.com/EdwardWason/skill-publisher)
- [Publishing Guide](references/publishing-guide.md)
- [Publish Procedures](references/publish-procedures.md)
- [Security Audit Reference](references/security-audit.md)
- [SkillHub Publishing](references/skillhub-publishing.md)
- [Change Detection and Version Bump](references/change-detection.md)
- [Changelog Generation](references/changelog-generation.md)
- [Repo Structure](references/repo-structure.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown reports with tables, command snippets, and generated repository files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation before publishing or local synchronization; uses publishing credentials from declared environment variables.]

## Skill Version(s):

5.22.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
