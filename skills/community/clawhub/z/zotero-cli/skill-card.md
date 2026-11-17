## Description:

Command-line interface for Zotero - search your Zotero library, add/edit notes, read attachments, and manage bibliographic references from the terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[killgfat](https://clawhub.ai/user/killgfat)

### License/Terms of Use:


## Use Case:

External users, researchers, and developers use this skill to work with Zotero from the terminal: searching libraries, reading attachments, adding or editing notes, exporting citations, and running batch research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install and update helpers can invoke package managers, change PATH-related shell startup files, and suggest unsafe installation modes.

Mitigation: Prefer pipx or an isolated virtual environment, avoid sudo pip, --break-system-packages, curl-piped shell execution, and git:// master installs, and review setup or update scripts before running them.

Risk: Backup helpers can copy Zotero configuration containing API credentials into local backup directories.

Mitigation: Keep the Zotero configuration and backup directory readable only by the user account, review backup contents before sharing or syncing them, and revoke or regenerate the Zotero API key if exposure is possible.

Risk: Helper scripts can write local output files such as query results, citation exports, restored query files, and backups.

Mitigation: Run helpers from a trusted working directory, inspect target paths before execution, and avoid feeding private library queries or exports into shared locations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/killgfat/skills/zotero-cli)
- [zotero-cli GitHub Repository](https://github.com/jbaiter/zotero-cli)
- [Zotero Documentation](https://www.zotero.org/support/)
- [Zotero API Key Settings](https://www.zotero.org/settings/keys)
- [PEP 668](https://peps.python.org/pep-0668/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration steps, Python and shell helper scripts, and optional JSON, Markdown, BibTeX, RIS, and plain-text command outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and either zotcli or zotero-cli; helper scripts can call local Zotero CLI commands and write local result, citation, backup, or configuration files.]

## Skill Version(s):

0.1.0 (source: server release evidence; artifact frontmatter and _meta.json report 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
