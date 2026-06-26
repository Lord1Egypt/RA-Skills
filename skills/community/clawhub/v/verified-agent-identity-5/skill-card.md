## Description: <br>
Billions/Iden3 authentication and identity management tools for agents. Link, proof, sign, and verify. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AgungPrabowo123](https://clawhub.ai/user/AgungPrabowo123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to create and manage Billions/Iden3 decentralized identities, link an agent identity to a human owner, and sign or verify identity challenges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Signing keys are stored in plaintext under $HOME/.openclaw/billions. <br>
Mitigation: Use a fresh low-value identity key, avoid passing real private keys on the command line, and restrict filesystem access to $HOME/.openclaw/billions. <br>
Risk: The skill can sign and send identity proofs with weak confirmation boundaries. <br>
Mitigation: Require explicit human confirmation of the recipient, challenge, and DID before running signing or linking scripts. <br>


## Reference(s): <br>
- [Billions Network](https://billions.network/) <br>
- [ClawHub skill page](https://clawhub.ai/AgungPrabowo123/verified-agent-identity-5) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text and JSON responses from Node.js command-line scripts, with Markdown guidance for agent workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update identity data under $HOME/.openclaw/billions and send direct messages through openclaw when linking or signing.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
