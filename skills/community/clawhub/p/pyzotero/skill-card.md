## Description:

Python scripts for Zotero that support search, browsing, item creation, and collection management through local Zotero API or Zotero Web API modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[killgfat](https://clawhub.ai/user/killgfat)

### License/Terms of Use:


## Use Case:

Developers and Zotero users use this skill to search, export, add, and organize Zotero library records from an agent workflow. It is useful for literature review, bibliography management, and automated Zotero collection maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Online Zotero mode uses ZOTERO_API_KEY and documentation includes shell environment setup that can expose credentials.

Mitigation: Prefer local Zotero mode when possible; for online mode, create a least-privilege Zotero key and keep it out of shell startup files, logs, and screenshots.

Risk: Installation guidance includes unpinned package installation and a sudo pip option.

Mitigation: Use pipx or a virtual environment with a pinned pyzotero version, and avoid sudo pip for normal installs.

Risk: Collection and item commands can modify or delete Zotero library data, including a delete command with a skip-confirmation flag.

Mitigation: Review collection and item keys before write operations, keep interactive confirmation enabled for deletes, and test on noncritical data before using automation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/killgfat/skills/pyzotero)
- [Publisher Profile](https://clawhub.ai/user/killgfat)
- [Pyzotero Homepage](https://github.com/urschrei/pyzotero)
- [Zotero API Key Settings](https://www.zotero.org/settings/keys)
- [Quickstart](artifact/QUICKSTART.md)
- [Installation Guide](artifact/INSTALL.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Human-readable terminal text or JSON, with Markdown documentation and shell command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can use local Zotero access or Zotero Web API access; write commands can create, rename, delete, or reorganize Zotero library records and collections.]

## Skill Version(s):

2.2.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
