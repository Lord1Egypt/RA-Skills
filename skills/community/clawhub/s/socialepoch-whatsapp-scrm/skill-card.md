## Description: <br>
SocialEpoch WhatsApp SCRM API helps agents configure SocialEpoch credentials, send and manage WhatsApp messages across multiple media types, query task and agent status, set callbacks, and operate message receiving for customer service and marketing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[socialepoch](https://clawhub.ai/user/socialepoch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External teams and developers use this skill to connect an agent to SocialEpoch WhatsApp SCRM for account queries, one-to-one and bulk messaging, callback setup, task tracking, and local message receiving. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads and runs a native receiver client locally. <br>
Mitigation: Install only if the SocialEpoch publisher and download path are trusted, and review the local client before enabling receiver commands. <br>
Risk: The skill stores SocialEpoch tenant credentials and the security evidence notes insufficient disclosure. <br>
Mitigation: Use limited-scope test credentials first, rotate or revoke credentials as needed, and avoid sharing local configuration files. <br>
Risk: The skill changes local OpenClaw settings and writes local files. <br>
Mitigation: Review expected local configuration changes before running receiver or reset commands, and restore settings if they do not match the intended deployment. <br>
Risk: Callback configuration and WhatsApp automation can route messages or status updates to unintended destinations. <br>
Mitigation: Review callback URLs carefully and require explicit user authorization before sending messages or enabling automated receiving workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/socialepoch/socialepoch-whatsapp-scrm) <br>
- [SocialEpoch API endpoint](https://api.socialepoch.com) <br>
- [SocialEpoch receiver client download for Windows](https://download.anascrm.com/installer/social/social_claw.exe) <br>
- [SocialEpoch receiver client download for macOS Intel](https://download.anascrm.com/installer/social/social_claw) <br>
- [SocialEpoch receiver client download for macOS Apple silicon](https://download.anascrm.com/installer/social/social_claw_arm) <br>
- [SocialEpoch receiver client download for Linux](https://download.anascrm.com/installer/social/social_claw_linux) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [JSON command responses with concise setup and error text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SocialEpoch tenant credentials and network access; some commands modify local OpenClaw settings or run a local receiver client.] <br>

## Skill Version(s): <br>
2.3.3 (source: evidence release, SKILL.md frontmatter, and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
