## Description:

Yuhang helps agents turn GitHub repositories into standardized Trae skill folders by scanning or cloning repositories, generating context bundles, and drafting skill files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guangliang2233](https://clawhub.ai/user/guangliang2233)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to evaluate GitHub repositories and scaffold them into Trae-compatible skills with context bundles, generated SKILL.md files, and optional wrapper scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repository cloning and generated scripts may introduce unreviewed third-party code into an agent skill workspace.

Mitigation: Install only in an isolated workspace, prefer official GitHub sources, and manually review generated context and SKILL.md before installing dependencies or running cloned code.

Risk: The force mode can overwrite an existing skill directory.

Mitigation: Avoid force mode unless the target directory is disposable; use unique skill names or backups before overwriting.

Risk: Local .env loading and mirrored network endpoints can expose local configuration or shift trust to mirror services.

Mitigation: Run from a directory without secrets in .env, constrain network access, and avoid proxy or mirror settings unless they are explicitly trusted.

## Reference(s):

- [ClawHub yuhang skill page](https://clawhub.ai/guangliang2233/skills/yuhang)
- [GitHub CLI official documentation](https://cli.github.com/)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files, generated code templates, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates skill directory structures and context_bundle.md; may run Git and write files in the selected output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
