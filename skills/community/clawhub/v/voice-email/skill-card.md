## Description: <br>
Send emails via natural voice commands - designed for accessibility <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sundiver1](https://clawhub.ai/user/Sundiver1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Accessibility-focused users and operators use this skill to compose and send Gmail messages from voice commands. It transcribes Telegram voice messages with Deepgram, extracts the recipient, subject, and body, then sends the email through gogcli. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice recordings and email content are processed through Telegram, Deepgram, and Gmail. <br>
Mitigation: Install only in environments where those service flows are acceptable, and use dedicated test accounts before routine use. <br>
Risk: The skill depends on sensitive credentials and OAuth access for Deepgram, Telegram, optional ElevenLabs, and Gmail. <br>
Mitigation: Store API keys and OAuth tokens in a secure environment, scope accounts and quotas where possible, and remove credentials when uninstalling. <br>
Risk: Misheard or malformed voice commands could produce an unintended recipient or message body. <br>
Mitigation: Confirm the workflow gives the user a chance to review recipients and message content before any email is sent. <br>


## Reference(s): <br>
- [Voice Email ClawHub Page](https://clawhub.ai/Sundiver1/voice-email) <br>
- [gogcli](https://gogcli.ai) <br>
- [Deepgram Console](https://console.deepgram.com) <br>
- [Deepgram Listen API](https://api.deepgram.com/v1/listen) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured Telegram, Deepgram, Gmail/gogcli, and optional ElevenLabs access before use.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
