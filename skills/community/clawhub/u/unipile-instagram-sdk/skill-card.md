## Description: <br>
Access Instagram messaging, profiles, posts, and interactions via Unipile's official Node.js SDK for automation and content management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mohit21gojs](https://clawhub.ai/user/mohit21gojs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect Instagram account data, read or send DMs, fetch profiles and posts, and manage content through a Unipile-connected Instagram account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read Instagram account data and, when write permission is enabled, send DMs, create posts, comment, and react through a connected Unipile account. <br>
Mitigation: Install only for accounts where Unipile is trusted, prefer a dedicated Instagram account, rotate access tokens, and monitor Unipile dashboard activity. <br>
Risk: The security evidence notes a mismatch between read-only safety claims and default write-capable behavior. <br>
Mitigation: Set UNIPILE_PERMISSIONS=read unless messaging, posting, comments, or reactions are intentionally required. <br>
Risk: UNIPILE_ACCESS_TOKEN grants API-level access to connected social accounts. <br>
Mitigation: Store the token in an environment-secret manager, avoid sharing shell history or logs that include it, and regenerate the token if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mohit21gojs/unipile-instagram-sdk) <br>
- [Unipile Node SDK](https://github.com/unipile/unipile-node-sdk) <br>
- [Unipile Provider Features Documentation](https://developer.unipile.com/docs/list-provider-features) <br>
- [Unipile Dashboard](https://dashboard.unipile.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output from the included CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires UNIPILE_DSN and UNIPILE_ACCESS_TOKEN; UNIPILE_PERMISSIONS controls read and write command access.] <br>

## Skill Version(s): <br>
1.0.6 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
