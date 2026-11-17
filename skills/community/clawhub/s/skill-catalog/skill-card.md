## Description:

Auto-scan all installed skills, generate a categorized INDEX.md, and keep it in sync via git hooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenwang-dev](https://clawhub.ai/user/kenwang-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace maintainers use this skill to inventory installed agent skills, generate a searchable skills/INDEX.md file, and optionally keep that index current through Git hooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional hook installer persistently replaces repository pre-commit and post-merge hooks, which can cause future repository scripts to run automatically.

Mitigation: Before running install-hooks.sh, inspect and back up existing hooks; use register.sh manually when automatic commit or pull updates are not needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kenwang-dev/skills/skill-catalog)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration]

**Output Format:** [Markdown file and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates skills/INDEX.md and can install repository Git hooks when the optional installer is run.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
