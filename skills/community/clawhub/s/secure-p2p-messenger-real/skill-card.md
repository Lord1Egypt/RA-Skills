## Description: <br>
A local OpenClaw shell skill for initializing identities, managing public-key contacts, and encrypting or decrypting peer-to-peer message packages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[puppetcat-fire](https://clawhub.ai/user/puppetcat-fire) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and OpenClaw agents use this skill to set up local command-line encrypted messaging workflows, exchange public-key contact information, and produce encrypted JSON message packages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence classifies the release as suspicious because it appears to be a local encryption prototype that overstates secure-messenger capabilities. <br>
Mitigation: Treat it as a simple local encryption tool, not a reviewed secure messenger, and do not rely on it for sensitive communications or metadata protection. <br>
Risk: The skill persists sensitive private keys under ~/.openclaw/secure-p2p/keyring and relies on contact IDs and message packages supplied by users. <br>
Mitigation: Protect or passphrase-encrypt private keys, verify contacts through a trusted channel, and avoid untrusted contact IDs or message packages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/puppetcat-fire/secure-p2p-messenger-real) <br>
- [SKILL.md](SKILL.md) <br>
- [README.md](README.md) <br>
- [package.json](package.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON message packages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bash, openssl, jq, and base64; writes local configuration, logs, contacts, and key material under ~/.openclaw/secure-p2p.] <br>

## Skill Version(s): <br>
1.0.14 (source: server release metadata, SKILL.md frontmatter, and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
