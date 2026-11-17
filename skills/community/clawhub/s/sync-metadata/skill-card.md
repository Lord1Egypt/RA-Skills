## Description:

Sync Metadata helps agents update README, SPEC, and similar Markdown documents from package.json metadata, including localized package.nls.json values and dry-run checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoqw7](https://clawhub.ai/user/guoqw7)

### License/Terms of Use:

GPL-3.0

## Use Case:

Developers and maintainers use this skill to keep repeated project metadata, such as name, version, description, license, repository URL, and author, synchronized across Markdown documentation after package.json changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may update marked README, SPEC, or other Markdown sections using package metadata, which could overwrite stale but intentional text inside sync markers.

Mitigation: Run the documented dry-run or check mode first and review the proposed synchronization report before confirming writes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guoqw7/skills/sync-metadata)
- [Project homepage](https://github.com/guoqw7/claude-skills)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown synchronization report with optional Markdown file updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports check-only dry-run behavior and user confirmation before writing changes.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
