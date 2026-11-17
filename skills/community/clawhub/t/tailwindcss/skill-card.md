## Description:

Writes and debugs Tailwind CSS utility classes, theme configuration, dark mode, variants, plugins, framework setup, migration, and build issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure, migrate, and debug Tailwind CSS in web projects, including class generation, theming, accessibility, framework integration, and build performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package setup or migration snippets that use npm or npx can resolve changing dependencies.

Mitigation: Prefer exact package versions or locally installed lockfile-resolved tools before running setup or migration commands.

Risk: Tailwind migration commands can rewrite project files and produce visual changes that still compile successfully.

Mitigation: Run migration commands on a clean branch, review every diff, and compare rendered output before merging.

Risk: The skill can read and update disclosed Tailwind preference files when a user states preferences.

Mitigation: Review changes under ~/Clawic/data/tailwindcss/ and store only preferences the user actually declares.

## Reference(s):

- [Tailwind CSS skill page](https://clawhub.ai/ivangdavila/skills/tailwindcss)
- [Clawic Tailwind CSS homepage](https://clawic.com/skills/tailwindcss)
- [Installation guide](artifact/installation.md)
- [Tailwind v4 migration guide](artifact/v4-migration.md)
- [Debugging guide](artifact/debugging.md)
- [Accessibility guide](artifact/accessibility.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose project file edits and may update disclosed Tailwind preference files under ~/Clawic/data/tailwindcss/ when the user states preferences.]

## Skill Version(s):

1.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
