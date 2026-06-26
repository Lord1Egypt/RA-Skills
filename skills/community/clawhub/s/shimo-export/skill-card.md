## Description: <br>
Shimo Document Export AI Skill enables agents to authenticate with shimo.im, browse files and team spaces, and export Shimo documents in formats such as Markdown, PDF, Word, Excel, PowerPoint, XMind, and images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[navyum](https://clawhub.ai/user/navyum) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent find, list, and export Shimo documents that are accessible to the authenticated account. It is intended for document backup, conversion, and batch download workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles a full live Shimo session cookie, which can grant broad access to personal and team documents. <br>
Mitigation: Use the skill only on a trusted machine, never paste cookie values into chat, keep config/env.json protected with 0600 permissions, and rotate or revoke the Shimo session when finished. <br>
Risk: The skill can scan and export broad sets of files, including all-space or team-space documents available to the account. <br>
Mitigation: Confirm the intended scope and destination before large exports, avoid all-space exports unless necessary, and review exported content storage locations. <br>
Risk: Credential expiry or failed authentication can interrupt export workflows. <br>
Mitigation: Run the provided preflight check before operations and reauthenticate through the local browser login flow when the Shimo API returns an authorization error. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/navyum/shimo-export) <br>
- [Publisher profile](https://clawhub.ai/user/navyum) <br>
- [Export API reference](artifact/export/references/api.md) <br>
- [File management API reference](artifact/file-management/references/api.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Natural-language summaries with JSON parsed from Node.js scripts and exported document files written to disk] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a valid SHIMO_COOKIE session credential; exported file formats depend on the Shimo document type.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
