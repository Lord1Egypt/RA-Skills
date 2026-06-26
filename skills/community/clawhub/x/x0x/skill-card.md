## Description: <br>
x0x helps agents use secure peer-to-peer networking for gossip broadcast, direct messaging, CRDT synchronization, group encryption, and NAT traversal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimcollinson](https://clawhub.ai/user/jimcollinson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to install and operate x0x networking tools, start the local daemon, manage identities and trust, and exchange peer-to-peer messages or encrypted group data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs networking binaries and can run a peer-to-peer daemon that creates persistent identity keys and an API token on the user's machine. <br>
Mitigation: Review and pin the downloaded release or installer when supply-chain controls are required, protect generated keys and bearer tokens, and enable autostart only when persistent daemon operation is intended. <br>


## Reference(s): <br>
- [ClawHub x0x skill page](https://clawhub.ai/jimcollinson/x0x) <br>
- [Publisher profile](https://clawhub.ai/user/jimcollinson) <br>
- [macOS arm64 release download](https://github.com/saorsa-labs/x0x/releases/latest/download/x0x-macos-arm64.tar.gz) <br>
- [macOS x64 release download](https://github.com/saorsa-labs/x0x/releases/latest/download/x0x-macos-x64.tar.gz) <br>
- [Linux x64 GNU release download](https://github.com/saorsa-labs/x0x/releases/latest/download/x0x-linux-x64-gnu.tar.gz) <br>
- [Linux arm64 GNU release download](https://github.com/saorsa-labs/x0x/releases/latest/download/x0x-linux-arm64-gnu.tar.gz) <br>
- [Windows x64 release download](https://github.com/saorsa-labs/x0x/releases/latest/download/x0x-windows-x64.zip) <br>
- [x0x API reference](https://github.com/saorsa-labs/x0x/blob/main/docs/api-reference.md) <br>
- [x0x security and cryptography documentation](https://github.com/saorsa-labs/x0x/blob/main/docs/security.md) <br>
- [x0x diagnostics documentation](https://github.com/saorsa-labs/x0x/blob/main/docs/diagnostics.md) <br>
- [x0x SDK quickstart](https://github.com/saorsa-labs/x0x/blob/main/docs/sdk-quickstart.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell, JSON, TOML, and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance covers installation, daemon startup, identity and token locations, REST and WebSocket usage, trust management, and configuration.] <br>

## Skill Version(s): <br>
0.26.0 (source: server-resolved release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
