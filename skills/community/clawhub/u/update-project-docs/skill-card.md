## Description:

Guides an agent through auditing code changes, identifying affected documentation, updating or scaffolding docs, validating them, and recording a documentation sync point.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openghz](https://clawhub.ai/user/openghz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to keep project documentation aligned with code changes, including full first-run audits, incremental documentation updates, and documentation site scaffolding when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect repository contents and propose documentation edits, which may expose or propagate sensitive or inaccurate project information if used without review.

Mitigation: Run it only in repositories where documentation updates are intended, review proposed changes before applying or committing them, and validate generated docs against the project build or lint checks.

Risk: The scaffolded Docsify template may rely on externally hosted assets or scripts before publication.

Mitigation: Before publishing a scaffolded site, pin dependencies to exact HTTPS URLs, add integrity checks, or vendor reviewed assets as recommended by the security guidance.

## Reference(s):

- [DOC-CONVENTIONS.md](references/DOC-CONVENTIONS.md)
- [CODE-TO-DOCS-MAPPING.md](references/CODE-TO-DOCS-MAPPING.md)
- [ClawHub Skill Page](https://clawhub.ai/openghz/skills/update-project-docs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with proposed file edits, code blocks, shell commands, and documentation content.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update documentation files, documentation navigation, Docsify scaffold files, and a documentation sync record after user confirmation.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
