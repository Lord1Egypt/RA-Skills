## Description: <br>
Billions/Iden3 authentication and identity management tools for agents. Link, proof, sign, and verify. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Web3Dropper](https://clawhub.ai/user/Web3Dropper) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to create Billions/Iden3 decentralized identities, link an agent identity to a human owner, sign authentication challenges, and verify DID ownership. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent private keys are stored unencrypted under $HOME/.openclaw/billions. <br>
Mitigation: Use a dedicated low-value agent key, restrict filesystem access to that directory, and keep the directory out of logs and shared backups. <br>
Risk: Signed identity material can be sent to caller-supplied recipients. <br>
Mitigation: Confirm the recipient and challenge before signing or linking, and stop if the sender or challenge is not recognized. <br>
Risk: The release has no server-resolved import provenance. <br>
Mitigation: Treat provenance as unavailable and review the published artifact and publisher profile before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Web3Dropper/web3dropper-verified-agent) <br>
- [Billions Network](https://billions.network/) <br>
- [Billions Wallet](https://wallet.billions.network) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions, shell commands, JSON responses, DID strings, verification URLs, and signature-verification status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js and the openclaw CLI; stores identity data under $HOME/.openclaw/billions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
