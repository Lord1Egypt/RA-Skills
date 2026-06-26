## Description: <br>
Enables agents to create and manage Billions decentralized identities, link them to human owners, and verify authentication proofs using Billions ERC-8004, Attestation Registries, and iden3. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adamlucker21](https://clawhub.ai/user/adamlucker21) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to manage a Billions Network agent DID, link it to a human owner, sign identity challenges, and verify DID ownership. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles long-lived private keys and local identity files. <br>
Mitigation: Do not import valuable private keys, restrict access to $HOME/.openclaw/billions, and review storage settings before use. <br>
Risk: Identity creation, owner linking, challenge signing, and verification messages can affect agent identity trust. <br>
Mitigation: Require explicit human approval before creating identities, linking an owner, signing challenges, or sending verification messages. <br>
Risk: The security evidence flags insufficient consent and scoping around identity linking. <br>
Mitigation: Install only when this identity-management behavior is intended, and review scripts before running npm install or node commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/adamlucker21/verified-agent-identity-6) <br>
- [Publisher Profile](https://clawhub.ai/user/adamlucker21) <br>
- [Billions Network](https://billions.network/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration guidance, Text, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and text or JSON command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and may create or read identity data under $HOME/.openclaw/billions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
