## Description:

Sync code snippets and notes between machines via file sync. Organized by language, rendered in any Markdown viewer (Obsidian, VS Code, etc.).

This skill is ready for commercial/non-commercial use.

## Publisher:

[cdmichaelb](https://clawhub.ai/user/cdmichaelb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other technical users use this skill to store reusable code snippets and Markdown notes in a dedicated synced vault for later search and reuse across machines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Synced notes or snippets may unintentionally include secrets or sensitive content and propagate to other machines.

Mitigation: Use a dedicated vault that contains no secrets, avoid credential-containing repositories or password stores, and keep backups or versioning for synced notes.

Risk: A mutable `npx clawhub@latest install snippets-sync` command can change behavior over time.

Mitigation: Prefer a pinned or verified installer command when installing the skill in controlled environments.

Risk: Writing outside the intended vault could affect local application configuration or unrelated files.

Mitigation: Restrict reads and writes to `.md` files in the dedicated vault and avoid `.obsidian/` or other application configuration directories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cdmichaelb/skills/snippets-sync)
- [Publisher profile](https://clawhub.ai/user/cdmichaelb)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown notes and code snippets with optional YAML frontmatter and fenced code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended for .md files in a dedicated snippets vault; optional obsidian-cli commands may be suggested when available.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
