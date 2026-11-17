## Description:

Refactors existing SKILL.md files for clearer triggers, durable constraints, progressive disclosure, and concise execution flows; it can also audit a skill without editing it or polish its companion README.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elisabeth15501](https://clawhub.ai/user/elisabeth15501)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to improve an existing SKILL.md, obtain a read-only structure and trigger audit, or polish its companion README. A local linter checks mechanical formatting and budget rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Refactoring or README polishing may change intended instructions or overwrite a file.

Mitigation: Specify the target and mode, retain a backup, and review the revised file and changelog before accepting edits.

Risk: A missing PyYAML dependency may prompt package installation.

Mitigation: Confirm whether package installs are permitted before running the linter in a restricted environment.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/elisabeth15501/skills/skill-refactor-clawhub-pub)
- [Platform frontmatter reference](artifact/references/platform-frontmatter.md)
- [Audit report example](artifact/references/skillmd_audit_sample.md)
- [README quality guide](artifact/references/readme_quality.md)

## Skill Output:

**Output Type(s):** [Markdown, Configuration guidance, JSON]

**Output Format:** [Optimized SKILL.md or README.md with a changelog, a read-only Markdown audit, or optional linter JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Three modes: refactor, audit, and readme; local, offline linting.]

## Skill Version(s):

1.0.0 (source: skill frontmatter, changelog, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
