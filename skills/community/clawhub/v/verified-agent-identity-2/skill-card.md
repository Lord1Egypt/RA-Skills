## Description: <br>
Billions/Iden3 authentication and identity management tools for agents. Link, proof, sign, and verify. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ferdiannsy33-pixel](https://clawhub.ai/user/ferdiannsy33-pixel) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to create and manage Billions/Iden3 decentralized identities, link an agent identity to a human owner, sign challenges, and verify identity ownership. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence says the skill asks users to run missing or unreviewed Node scripts that handle persistent private keys and signed identity proofs. <br>
Mitigation: Install only after inspecting the referenced scripts and dependencies from a trusted source. <br>
Risk: Identity data, including private keys, is stored under $HOME/.openclaw/billions. <br>
Mitigation: Use a dedicated low-value identity key and protect access to $HOME/.openclaw/billions. <br>
Risk: Existing private keys can be passed on the command line and signing or linking operations can bind identity claims to a recipient or challenge. <br>
Mitigation: Avoid passing existing private keys on the command line, and confirm the recipient and challenge before any signing or linking operation. <br>


## Reference(s): <br>
- [Billions Network](https://billions.network/) <br>
- [ClawHub skill page](https://clawhub.ai/ferdiannsy33-pixel/verified-agent-identity-2) <br>
- [Publisher profile](https://clawhub.ai/user/ferdiannsy33-pixel) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce DID strings, identity lists, challenge strings, signed-token verification results, and success or error messages from the referenced Node scripts.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
