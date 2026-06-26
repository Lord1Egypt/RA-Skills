## Description: <br>
Billions/Iden3 authentication and identity management tools for agents. Link, proof, sign, and verify. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ajitrisetiadi](https://clawhub.ai/user/ajitrisetiadi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create and manage Billions/Iden3 decentralized identities, link agent identities to human owners, sign challenges, and verify ownership proofs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles and transmits sensitive identity proofs, including DIDs, challenges, tokens, verification URLs, and wallet-related material. <br>
Mitigation: Review before installing, use a dedicated identity, and confirm exactly what will be sent and to whom before any signing or messaging action. <br>
Risk: Command-line examples may expose private keys or other sensitive credentials if real values are pasted directly. <br>
Mitigation: Do not paste real private keys into command-line examples; prefer a dedicated test identity and keep secrets out of shell history. <br>
Risk: The release evidence says required scripts and dependency files should be available for review before use. <br>
Mitigation: Require the missing scripts and dependency files to be reviewed before deployment or execution. <br>


## Reference(s): <br>
- [Billions Network](https://billions.network/) <br>
- [ClawHub skill page](https://clawhub.ai/ajitrisetiadi/verified-agent-identity-ajitrisetiadi) <br>
- [Publisher profile](https://clawhub.ai/user/ajitrisetiadi) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with bash commands and JSON or string command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node and openclaw; identity data is stored under $HOME/.openclaw/billions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
