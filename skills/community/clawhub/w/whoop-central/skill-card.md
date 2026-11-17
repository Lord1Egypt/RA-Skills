## Description:

WHOOP Central provides OAuth setup and Node.js scripts for fetching WHOOP sleep, recovery, strain, workout, and profile data from the WHOOP Developer API v2.

This skill is ready for commercial/non-commercial use.

## Publisher:

[4xiomdev](https://clawhub.ai/user/4xiomdev)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to connect an agent to their WHOOP account, verify OAuth access, and retrieve recent or historical sleep, recovery, strain, and workout metrics for personal health analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WHOOP OAuth tokens and client credentials are stored in local JSON files.

Mitigation: Use the skill only on a trusted single-user machine, restrict permissions on ~/.clawdbot/whoop, and avoid entering or displaying tokens in recorded or shared terminals.

Risk: Fetched health history can be written to local WHOOP log files.

Mitigation: Protect ~/clawd/health/logs/whoop with local file permissions and delete retained logs when they are no longer needed.

Risk: Granted WHOOP read scopes provide access to sensitive fitness and health metrics.

Mitigation: Authorize only the scopes needed for the workflow and revoke WHOOP tokens if the skill is no longer in use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/4xiomdev/skills/whoop-central)
- [WHOOP Developer Portal](https://developer.whoop.com/)
- [WHOOP Developer API v2](https://api.prod.whoop.com/developer/v2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, JSON, JSONL]

**Output Format:** [Markdown guidance with inline shell commands plus optional JSON or JSONL command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+; openssl is needed only for the optional localhost HTTPS OAuth flow.]

## Skill Version(s):

1.0.2 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
