## Description:

Generates, audits, and packages agent skills for local use and distribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyuming0823](https://clawhub.ai/user/liuyuming0823)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to create agent skill skeletons, check existing skills, and package them for local installation or publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit suppression can bypass a critical finding before a skill is packaged and installed.

Mitigation: Do not treat the P0 audit as a hard security gate; inspect .skillignore and inline ignore markers, then review packages manually before use or publication.

Risk: Packaging can install a skill locally by default.

Mitigation: Use --no-install for trial runs and review the package before installing it.

## Reference(s):

- [Skill Generator on ClawHub](https://clawhub.ai/liuyuming0823/skills/ym-skill-generator-ch)
- [Generation guide](artifact/references/generation-guide.md)
- [Sanitization rules](artifact/references/sanitize-rules.md)

## Skill Output:

**Output Type(s):** [Code, Files, Markdown, Shell commands, Guidance]

**Output Format:** [Skill directory or ZIP package with Markdown and scripts; text audit reports and commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can install generated or packaged skills locally by default.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
