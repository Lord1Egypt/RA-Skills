## Description:

Encrypt, decrypt, and manage keys with the SAFE CLI - a modern GPG alternative with post-quantum support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[grittygrease](https://clawhub.ai/user/grittygrease)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to encrypt, decrypt, inspect, and manage encrypted files and key material with the SAFE CLI or the SAFE browser interface when the CLI is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may attempt automatic installation of a remote SAFE binary with elevated permissions.

Mitigation: Use a user-controlled install path, verify the downloaded binary and checksum before use, and do not permit automatic sudo installation.

Risk: The skill handles private keys and may reuse existing SSH keys for decryption workflows.

Mitigation: Prefer dedicated SAFE keys, keep private keys out of browser forms unless explicitly required, and review any workflow that accesses existing SSH keys.

Risk: Passwords entered directly in command lines or automation traces can be exposed.

Mitigation: Use interactive prompts or environment-variable based password references instead of literal command-line passwords.

## Reference(s):

- [SAFE web interface](https://thesafe.dev)
- [SAFE downloads](https://thesafe.dev/download/)
- [SAFE download checksums](https://thesafe.dev/downloads/checksums.txt)
- [SAFE GitHub repository](https://github.com/grittygrease/safe)
- [ClawHub skill release](https://clawhub.ai/grittygrease/skills/safe-encryption-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands and workflow guidance for SAFE CLI operations, browser-based encryption workflows, key management, and encrypted file handling.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
