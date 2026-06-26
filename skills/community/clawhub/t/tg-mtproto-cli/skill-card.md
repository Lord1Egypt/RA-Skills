## Description: <br>
Provides read-only Telegram access through the tg MTProto CLI to list chats, fetch messages, download media, and manage local accounts or sessions without modifying Telegram data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyberash-dev](https://clawhub.ai/user/cyberash-dev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, operators, and agents use this skill when they need read-only access to Telegram chats for message retrieval, media download, account listing, or data extraction workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram API credentials and local session databases can grant access to account data if exposed. <br>
Mitigation: Keep the session directory private, do not share session files, and do not log or display api_id or api_hash values. <br>
Risk: Using the CLI gives the local agent or runtime access to Telegram messages and media available to the authenticated account. <br>
Mitigation: Use the skill only on machines where the user trusts the local runtime with Telegram message access. <br>
Risk: Media downloads write files to the selected output directory or current working directory. <br>
Mitigation: Direct downloads to an explicit output directory and review downloaded files before sharing or processing them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cyberash-dev/tg-mtproto-cli) <br>
- [tg-mtproto-cli npm package](https://www.npmjs.com/package/tg-mtproto-cli) <br>
- [Telegram API app registration](https://my.telegram.org/apps) <br>
- [tg-mtproto-cli source repository listed in artifact](https://github.com/cyberash-dev/tg-mtproto-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Telegram operations; may produce local media downloads when the user invokes tg download.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
