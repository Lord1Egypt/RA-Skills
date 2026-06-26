## Description: <br>
Push X/Twitter bookmarks into Google NotebookLM notebooks, auto-routed by bookmark folder. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spideystreet](https://clawhub.ai/user/spideystreet) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to fetch X/Twitter bookmark folders, match them to NotebookLM notebooks, and add each bookmark as a text source while tracking which bookmark IDs were pushed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reusable X session cookies are stored locally and can expose account access if leaked. <br>
Mitigation: Protect the cookie file like a password, restrict local file access, and re-export cookies only when needed. <br>
Risk: Private bookmark text and URLs may be copied into Google NotebookLM notebooks. <br>
Mitigation: Review folder routing and notebook destinations before syncing sensitive material. <br>
Risk: Unattended auto-sync can route bookmarks to matching notebooks without per-folder confirmation. <br>
Mitigation: Avoid cron or unattended sync until the folder-to-notebook matching behavior has been reviewed. <br>


## Reference(s): <br>
- [X To Notebook on ClawHub](https://clawhub.ai/spideystreet/x-to-notebook) <br>
- [spideystreet ClawHub Profile](https://clawhub.ai/user/spideystreet) <br>
- [twikit](https://github.com/d60/twikit) <br>
- [notebooklm-mcp-cli](https://github.com/jacob-bd/notebooklm-mcp-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, API calls, Guidance] <br>
**Output Format:** [Markdown/text guidance with shell command and JSON command snippets; helper scripts return JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv, mcporter, twikit, notebooklm-mcp-cli, X session cookies, Chrome, and authenticated NotebookLM access.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
