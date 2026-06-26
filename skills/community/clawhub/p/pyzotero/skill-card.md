## Description: <br>
Python scripts for Zotero - supports search, browse, add items, and full collection management. Both local API and online Web API modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[killgfat](https://clawhub.ai/user/killgfat) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, researchers, and Zotero users use this skill to search, inspect, add, and organize Zotero library items from an agent session using local Zotero or the Zotero Web API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access a user's Zotero library through local Zotero or the Zotero Web API. <br>
Mitigation: Install only when this library access is acceptable, and prefer local mode when it meets the workflow need. <br>
Risk: Online mode uses a Zotero API key that could grant library access if stored or exposed insecurely. <br>
Mitigation: Use a least-privilege Zotero API key, avoid shared dotfiles, and do not echo the key in terminals or logs. <br>
Risk: Collection delete, rename, bulk add, and item move commands can modify the Zotero library. <br>
Mitigation: Review write and delete commands, collection keys, item keys, and bulk input files before execution. <br>


## Reference(s): <br>
- [Pyzotero ClawHub release](https://clawhub.ai/killgfat/pyzotero) <br>
- [Pyzotero upstream project](https://github.com/urschrei/pyzotero) <br>
- [Zotero API key settings](https://www.zotero.org/settings/keys) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands; Zotero commands can return human-readable text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and pyzotero; online mode uses ZOTERO_USER_ID and ZOTERO_API_KEY.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
