## Description: <br>
Secure computer-to-computer networking for AI agents, including gossip broadcast, direct messaging, CRDTs, group encryption, post-quantum encryption, and NAT traversal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimcollinson](https://clawhub.ai/user/jimcollinson) <br>

### License/Terms of Use: <br>
MIT OR Apache-2.0 <br>


## Use Case: <br>
Developers and agent builders use this skill to install, configure, and operate x0x as a local daemon and CLI for secure peer-to-peer agent communication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and runs a local x0x daemon that creates persistent agent identity keys and communicates with other agents over the network. <br>
Mitigation: Install only when that daemon behavior is desired, and use the documented explicit controls for starting, stopping, or enabling autostart. <br>
Risk: WebSocket examples can expose the local api-token if token-bearing URLs are pasted into shared terminals, logs, or transcripts. <br>
Mitigation: Treat the api-token as a credential and avoid sharing WebSocket URLs or command output that contains it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jimcollinson/skills/x0x) <br>
- [Publisher profile](https://clawhub.ai/user/jimcollinson) <br>
- [x0x release downloads](https://github.com/saorsa-labs/x0x/releases/latest) <br>
- [Full API Reference](https://github.com/saorsa-labs/x0x/blob/main/docs/api-reference.md) <br>
- [Security & Cryptography](https://github.com/saorsa-labs/x0x/blob/main/docs/security.md) <br>
- [SDK Quickstart](https://github.com/saorsa-labs/x0x/blob/main/docs/sdk-quickstart.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON API examples, and TOML configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces installation, daemon operation, API usage, trust management, and configuration guidance for x0x.] <br>

## Skill Version(s): <br>
0.27.0 (source: evidence release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
