## Description: <br>
Encrypt, decrypt, and manage keys with the SAFE CLI, a modern GPG alternative with post-quantum support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[grittygrease](https://clawhub.ai/user/grittygrease) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to encrypt, decrypt, generate keys, and exchange SAFE messages through the SAFE CLI or browser fallback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install a downloaded SAFE binary with elevated privileges. <br>
Mitigation: Require user approval before installation, verify the binary checksum, and prefer a user-local install path. <br>
Risk: The skill handles sensitive plaintext, private keys, and passphrases. <br>
Mitigation: Confirm the exact files, keys, recipients, and operations before encryption or decryption, and avoid browser fallback for highly sensitive material. <br>
Risk: Browser and network sharing workflows may expose sensitive material or route it to unintended destinations. <br>
Mitigation: Use the CLI for sensitive workflows where possible and confirm each network destination before sharing encrypted messages or keys. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/grittygrease/safe-encryption-skill) <br>
- [SAFE Web Interface](https://thesafe.dev) <br>
- [SAFE Downloads](https://thesafe.dev/download/) <br>
- [SAFE Download Checksums](https://thesafe.dev/downloads/checksums.txt) <br>
- [SAFE GitHub Repository](https://github.com/grittygrease/safe) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and automation examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include CLI commands, browser automation steps, encryption recipient guidance, and key-management guidance.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
