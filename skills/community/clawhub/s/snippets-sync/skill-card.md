## Description: <br>
Sync code snippets and notes between machines via file sync, organized by language and rendered in Markdown viewers such as Obsidian or VS Code. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cdmichaelb](https://clawhub.ai/user/cdmichaelb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create, organize, read, and update reusable code snippets and notes as Markdown files in a dedicated synced vault. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pointing the vault path at a home directory, password store, SSH directory, or repository containing secrets could expose or modify sensitive files. <br>
Mitigation: Use a dedicated snippets or notes folder for SNIPPETS_VAULT_PATH and restrict reads and writes to .md files inside that vault. <br>
Risk: Markdown written to the vault can propagate to other machines through file sync, including unwanted overwrites or conflicts. <br>
Mitigation: Use backups or versioning for the vault and review sync behavior before relying on changes across devices. <br>
Risk: Editing Obsidian application configuration could disrupt the user's local vault setup. <br>
Mitigation: Do not touch .obsidian or other application configuration directories; operate only on note and snippet Markdown files. <br>


## Reference(s): <br>
- [Snippets Sync ClawHub page](https://clawhub.ai/cdmichaelb/snippets-sync) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown files with YAML frontmatter, fenced code blocks, and concise chat notifications] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes only .md files inside the configured snippets vault; optional obsidian-cli commands may be used for search and listing when installed.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
