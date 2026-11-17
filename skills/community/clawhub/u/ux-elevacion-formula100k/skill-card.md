## Description:

Spanish-language UI/UX elevation skill for Next.js 16, Tailwind CSS, and shadcn/ui projects that helps agents audit, polish, animate, typeset, and build higher-quality interfaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product builders use this skill to improve application and landing-page UI quality, especially for Spanish-language workflows using Next.js, Tailwind CSS, and shadcn/ui. It produces actionable UX audits, design guidance, code diffs, and implementation patterns for spacing, typography, motion, interaction states, and landing-page craft.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may propose or edit UI files, and design edits can introduce incorrect behavior, regressions, or unsuitable visual choices.

Mitigation: Review proposed edits before applying them and keep broad PR-review requests scoped to UI and design work.

Risk: The skill references the f100k-puente bridge skill for environment translation.

Mitigation: Verify the referenced f100k-puente skill before an agent loads or relies on it.

## Reference(s):

- [Anti-Slop Patterns reference](references/anti-slop-patterns.md)
- [ClawHub skill page](https://clawhub.ai/formula100k/skills/ux-elevacion-formula100k)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code diffs and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Spanish-language UX/design output; edits should be reviewed before applying.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
