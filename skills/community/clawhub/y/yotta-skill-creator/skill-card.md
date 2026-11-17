## Description:

Creates yotta-prefixed skill scaffolds from embedded templates, validates naming and directory structure, and supports a self-use mode without release files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yottameta](https://clawhub.ai/user/yottameta)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to create a new yotta-prefixed agent skill from a release-ready scaffold and check its naming and structure. The self-use option creates only the skill body and references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private-mode scaffolds can include a package-publishing workflow despite the promise to omit publishing files.

Mitigation: Before committing a private scaffold, remove the generated .github/workflows/publish.yml or correct it.

Risk: Reinstalling can affect an existing skill installation.

Mitigation: Choose --agent or --dir, preview with --dry-run, and back up an existing installation before reinstalling.

## Reference(s):

- [CLI reference](artifact/references/cli-reference.md)
- [Scaffold structure](artifact/references/scaffold-structure.md)
- [Tutorial](artifact/references/tutorial.md)
- [Project homepage](https://github.com/YottaMeta/yotta-skill-creator)
- [ClawHub skill page](https://clawhub.ai/yottameta/skills/yotta-skill-creator)
- [npm package](https://www.npmjs.com/package/@yottameta/yotta-skill-creator)

## Skill Output:

**Output Type(s):** [Files, Code, Markdown, Configuration instructions, Shell commands]

**Output Format:** [Generated skill directory with Markdown documentation, configuration files, and optional CLI code and tests.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Full release scaffold or self-use scaffold; target directory is selected by the user and existing targets are not overwritten.]

## Skill Version(s):

0.1.7 (source: SKILL.md frontmatter, CHANGELOG.md, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
