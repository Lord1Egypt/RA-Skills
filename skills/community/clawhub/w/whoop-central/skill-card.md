## Description: <br>
WHOOP Central provides OAuth setup and scripts for fetching WHOOP sleep, recovery, strain, and workout data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[4xiomdev](https://clawhub.ai/user/4xiomdev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Individuals and agents use this skill to authenticate with a user-controlled WHOOP developer app and retrieve sleep, recovery, strain, and workout metrics for personal health and fitness workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill accesses sensitive WHOOP health data and stores OAuth tokens locally. <br>
Mitigation: Use a WHOOP developer app you control, request only needed scopes, keep local token files private, and revoke or delete tokens when finished. <br>
Risk: Bulk import can create a local archive of historical health data. <br>
Mitigation: Run historical import only when a local archive is intended, and protect or delete generated health logs according to your data-retention needs. <br>


## Reference(s): <br>
- [WHOOP Developer Portal](https://developer.whoop.com/) <br>
- [WHOOP Developer API v2](https://api.prod.whoop.com/developer/v2) <br>
- [WHOOP Central on ClawHub](https://clawhub.ai/4xiomdev/whoop-central) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [Console text, JSON, JSONL, and local JSONL log files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and WHOOP OAuth credentials; optional OpenSSL is used for the local HTTPS OAuth flow.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter, package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
