## Description: <br>
Manage Sun-Panel navigation by adding websites, creating and editing shortcut groups, and recommending icons for bookmarks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meichuanyi](https://clawhub.ai/user/meichuanyi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, NAS administrators, and homelab users use this skill to configure Sun-Panel shortcuts, groups, favicons, and Iconify icons through the Sun-Panel API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores the Sun-Panel URL, username, and password in a local plaintext config file. <br>
Mitigation: Use a limited-permission Sun-Panel account where possible, restrict permissions on ~/.openclaw/skills/sun-panel/config.json, and rotate or delete the password when no longer needed. <br>
Risk: Generated commands send credentials and tokens to the configured Sun-Panel host. <br>
Mitigation: Configure only trusted Sun-Panel hosts and use HTTPS when available before running generated API commands. <br>


## Reference(s): <br>
- [Iconify icon sets](https://icon-sets.iconify.design/) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include curl commands and JSON payloads that target a user-configured Sun-Panel instance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
