## Description:

Guides AI agents through using x0x for peer-to-peer messaging, gossip, shared data, and encrypted groups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimcollinson](https://clawhub.ai/user/jimcollinson)

### License/Terms of Use:

MIT OR Apache-2.0

## Use Case:

Developers use this skill to install and operate x0x agents, connect peers, and follow documented messaging and collaboration workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marked this release suspicious with medium confidence, citing a mutable unsigned shell installer that starts the daemon automatically and reported capabilities beyond the stated networking purpose. Its coverage was incomplete because referenced local paths were missing; the scanners did not establish malicious intent or data exfiltration.

Mitigation: Review the installation options and relevant source before installing. Avoid the shell installer unless its behavior is understood and daemon startup is authorized; the documented install.py checks pinned GPG signatures, and verification failures should not be bypassed.

## Reference(s):

- [x0x on ClawHub](https://clawhub.ai/jimcollinson/skills/x0x)
- [x0x project repository](https://github.com/saorsa-labs/x0x)
- [Security and cryptography](https://github.com/saorsa-labs/x0x/blob/main/docs/security.md)
- [Operations guide](https://github.com/saorsa-labs/x0x/blob/main/docs/skill/operations.md)
- [Owner and agent guide](https://github.com/saorsa-labs/x0x/blob/main/docs/skill/owner.md)
- [Messaging guide](https://github.com/saorsa-labs/x0x/blob/main/docs/skill/messaging.md)
- [Stores, files, and history guide](https://github.com/saorsa-labs/x0x/blob/main/docs/skill/stores.md)
- [x0x website](https://saorsalabs.com)
- [Install for macOS ARM64](https://github.com/saorsa-labs/x0x/releases/latest/download/x0x-macos-arm64.tar.gz)
- [Install for macOS x64](https://github.com/saorsa-labs/x0x/releases/latest/download/x0x-macos-x64.tar.gz)
- [Install for Linux x64](https://github.com/saorsa-labs/x0x/releases/latest/download/x0x-linux-x64-gnu.tar.gz)
- [Install for Linux ARM64](https://github.com/saorsa-labs/x0x/releases/latest/download/x0x-linux-arm64-gnu.tar.gz)
- [Install for Windows x64](https://github.com/saorsa-labs/x0x/releases/latest/download/x0x-windows-x64.zip)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Code]

**Output Format:** [Markdown with shell commands, REST examples, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Step-by-step instructions for installing and operating x0x, with links to topic-specific documentation.]

## Skill Version(s):

0.49.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
