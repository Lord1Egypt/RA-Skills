## Description:

README Craft helps agents create, audit, and rewrite project README files using documented README quality patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lanyasheng](https://clawhub.ai/user/lanyasheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to create README.md files for new projects, audit existing README quality with a 22-item score, or rewrite README content while preserving useful project facts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated or rewritten README content may be inaccurate, stale, or inconsistent with the project if accepted without review.

Mitigation: Run audit mode first when possible, review proposed diffs before writes, and keep version control active around README changes.

Risk: The skill has broad shell, network, delegation, and file-editing authority relative to a README-writing task.

Mitigation: Use it on trusted workspaces, or narrow execution to README-scoped file access and avoid unrestricted Bash, WebFetch, or Agent access when reviewing untrusted repositories.

## Reference(s):

- [Quality Checklist](references/quality-checklist.md)
- [README Anti-Patterns](references/anti-patterns.md)
- [Badge and Visuals Guide](references/badge-and-visuals.md)
- [Community Standards](references/community-standards.md)
- [Real-World README Patterns](references/real-world-patterns.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Code, Shell commands, Guidance]

**Output Format:** [Markdown reports and README.md file updates; may include code blocks, score tables, and diff-oriented rewrite guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Create and rewrite modes can write README.md and optional bilingual README files; audit mode returns a report without file changes.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
