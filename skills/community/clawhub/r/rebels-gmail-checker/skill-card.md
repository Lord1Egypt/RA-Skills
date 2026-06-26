## Description: <br>
Check Gmail for unread inbox emails, filtered by priority, and output a brief digest sorted by HIGH, MEDIUM, and LOW priority while skipping marketing, promotions, social, and update categories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[99rebels](https://clawhub.ai/user/99rebels) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to check unread Gmail messages, filter out noisy categories, and receive a prioritized inbox digest. It can also guide first-time setup for Google OAuth credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires read-only Gmail OAuth access and stores OAuth credentials locally. <br>
Mitigation: Grant access only when email checking is intended, run setup on a trusted machine, and keep <DATA_DIR>/gmail.json private. <br>
Risk: OAuth client secrets and refresh tokens could be exposed if pasted into chat, logs, or shared files. <br>
Mitigation: Avoid pasting OAuth secrets into chat or logs and store credential files in the configured private data directory. <br>


## Reference(s): <br>
- [Gmail Setup Guide](references/setup.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/99rebels/rebels-gmail-checker) <br>
- [Google Cloud Console](https://console.cloud.google.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text digest or structured JSON, with setup guidance and shell commands when credentials are missing.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Unread messages are filtered by configurable labels and sorted by HIGH, MEDIUM, and LOW priority.] <br>

## Skill Version(s): <br>
1.3.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
