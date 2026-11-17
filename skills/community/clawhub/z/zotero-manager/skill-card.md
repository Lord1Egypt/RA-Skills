## Description:

Zotero Manager is a compatibility skill for Zotero literature management that routes users toward the unified knowledge entry point while preserving legacy Zotero workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jirboy](https://clawhub.ai/user/jirboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and Zotero users use this skill to search literature, import DOI records, manage categories, and export references through the recommended knowledge zotero command path or compatible legacy Zotero commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles reusable Zotero API credentials that could leak through unsafe storage, shell history, or overly broad permissions.

Mitigation: Use a dedicated least-privilege Zotero key, prefer read-only permissions, restrict saved key files to the current user, and avoid pasting tokens directly into shell history.

Risk: The local API URL can be overridden, which could send credentials or library data to an untrusted endpoint if misdirected.

Mitigation: Use --api-url only with trusted Zotero loopback addresses such as localhost or 127.0.0.1, and review commands before execution.

## Reference(s):

- [ClawHub Zotero Manager release](https://clawhub.ai/jirboy/skills/zotero-manager)
- [Zotero API key settings](https://www.zotero.org/settings/keys)
- [Zotero Web API v3 documentation](https://www.zotero.org/support/dev/web_api/v3/start)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance, shell commands, Python command output, and optional JSON search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call Zotero local or remote APIs and may read Zotero API keys from user configuration files or ZOTERO_API_KEY.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
