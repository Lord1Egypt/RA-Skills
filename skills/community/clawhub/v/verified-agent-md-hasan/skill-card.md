## Description: <br>
A decentralized identity management toolkit for AI agents using the iden3 protocol on Billions Network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mdh531916-collab](https://clawhub.ai/user/mdh531916-collab) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to create and manage Billions Network DIDs, sign or verify identity challenges, and link an agent DID to a human owner. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private identity keys can be stored in plaintext when BILLIONS_NETWORK_MASTER_KMS_KEY is not set. <br>
Mitigation: Set BILLIONS_NETWORK_MASTER_KMS_KEY before generating or importing keys, store the master key securely, and restrict access to $HOME/.openclaw/billions. <br>
Risk: Providing an existing private key on the command line can expose sensitive credentials through shell history or process inspection. <br>
Mitigation: Avoid command-line secrets, prefer generating a dedicated agent identity, and do not reuse high-value wallet keys. <br>
Risk: DID resolution, verification, or attestation requests may contact Billions or Privado services. <br>
Mitigation: Use the skill only when external identity verification is intended and obtain consent before sending verification or DID-resolution requests. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mdh531916-collab/verified-agent-md-hasan) <br>
- [Billions Network](https://billions.network/) <br>
- [OpenClaw Environment Documentation](https://docs.openclaw.ai/help/environment) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; scripts return plain text, JSON, verification URLs, or success/error status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js. Identity data and key material are persisted under $HOME/.openclaw/billions; BILLIONS_NETWORK_MASTER_KMS_KEY enables encrypted key storage.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
