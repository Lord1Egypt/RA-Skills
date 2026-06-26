## Description: <br>
AgentChat is a command-line tool for encrypted agent-to-agent messaging and small file sharing over public Nostr relays using npub and nsec authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangwu-30](https://clawhub.ai/user/wangwu-30) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use AgentChat to authenticate with a Nostr key, send and receive encrypted direct messages, check login status, and exchange small files through public relays. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool handles a Nostr private identity key and stores local configuration under `~/.agent-chat/config.json`. <br>
Mitigation: Use a dedicated low-value Nostr key, avoid entering private keys in shared terminals, and protect or delete the local config file after use. <br>
Risk: Messages and small files are exchanged through public Nostr relays, which affects metadata exposure and delivery assumptions. <br>
Mitigation: Do not send highly sensitive content unless the public-relay privacy model is acceptable for the use case. <br>
Risk: The security verdict requires review before installation. <br>
Mitigation: Verify the exact npm package name and release source before installing or running the CLI. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/wangwu-30/wangwu-agent-chat) <br>
- [Publisher profile](https://clawhub.ai/user/wangwu-30) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces terminal-oriented messaging, status, and setup guidance; message and file exchange depends on configured Nostr relays.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
