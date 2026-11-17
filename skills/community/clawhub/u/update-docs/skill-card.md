## Description:

Guides agents through identifying documentation impact from code changes, updating or scaffolding OpenClaw docs, and validating formatting, links, and frontmatter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frisky1985](https://clawhub.ai/user/frisky1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to inspect changed source files, find affected OpenClaw documentation, update existing docs or scaffold new pages, and run basic documentation validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documentation edits can introduce incorrect or misleading guidance if proposed changes are applied without review.

Mitigation: Review planned edits before approving them and validate frontmatter, formatting, links, spelling, and examples before release.

Risk: Optional bundled utilities can inspect git changes or create/package files when run.

Mitigation: Use the normal guided documentation workflow unless those utilities are needed, and review command effects before execution.

## Reference(s):

- [Code to Documentation Mapping](references/CODE-TO-DOCS-MAPPING.md)
- [Documentation Conventions](references/DOC-CONVENTIONS.md)
- [API Reference Template](assets/api-reference-template.md)
- [Guide Template](assets/guide-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, file paths, checklists, and optional generated Markdown or code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May inspect local git diffs and propose documentation edits; bundled utilities can list changed files, map affected docs, validate docs, initialize skill files, or package the skill.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
