## Description: <br>
Command-line interface for Zotero - search your Zotero library, add/edit notes, read attachments, and manage bibliographic references from the terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[killgfat](https://clawhub.ai/user/killgfat) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Researchers, students, writers, and developers use this skill to install and operate zotero-cli from an agent workflow for Zotero library search, note management, attachment reading, citation export, and bibliography automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional setup and update scripts can install packages, change shell PATH settings, or run package-manager commands. <br>
Mitigation: Prefer pipx installation and inspect helper scripts before running setup, update, restore, cleanup, or scheduled examples. <br>
Risk: Some installation examples show forced system-package installation or other commands that can affect the host Python environment. <br>
Mitigation: Use pipx or a virtual environment and avoid forced system-package examples unless they have been reviewed for the target system. <br>
Risk: Zotero configuration and backup folders can contain API credentials. <br>
Mitigation: Keep Zotero config and backup directories private and review backup or restore outputs before sharing files. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/killgfat/zotero-cli) <br>
- [zotero-cli project homepage](https://github.com/jbaiter/zotero-cli) <br>
- [Zotero](https://www.zotero.org) <br>
- [Zotero API key settings](https://www.zotero.org/settings/keys) <br>
- [PEP 668](https://peps.python.org/pep-0668/) <br>
- [Quick start guide](QUICKSTART.md) <br>
- [Installation guide](INSTALL.md) <br>
- [Usage examples](EXAMPLES.md) <br>
- [Helper scripts guide](scripts/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; helper scripts may produce console text, tables, JSON, Markdown, BibTeX, RIS, or plain text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and either zotcli or zotero-cli; uses Zotero API credentials configured by the user.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
