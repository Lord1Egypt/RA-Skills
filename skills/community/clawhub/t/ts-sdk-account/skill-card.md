## Description: <br>
Guides TypeScript developers through creating, importing, serializing, signing with, and safely handling Aptos Account signers in @aptos-labs/ts-sdk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iskysun96](https://clawhub.ai/user/iskysun96) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when integrating Aptos account management in TypeScript server scripts or backend workflows. It helps them generate or import Account signers, select signing schemes, serialize accounts, sign and verify messages or transactions, and avoid exposing private keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private keys, mnemonics, or serialized accounts can expose funds if copied into chat, frontend code, logs, or source control. <br>
Mitigation: Keep secrets server-side in environment-managed storage, avoid sharing them with agents, and review examples against official Aptos SDK documentation before using real funds. <br>
Risk: Account guidance can be misapplied to the wrong network, sender, recipient, amount, payload, signing scheme, or derivation path. <br>
Mitigation: Review transaction details and account parameters before signing or submitting, and treat the skill as documentation rather than permission for automatic transactions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/iskysun96/ts-sdk-account) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code] <br>
**Output Format:** [Markdown guidance with TypeScript code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only; does not execute transactions, submit network requests, or manage keys.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact metadata version 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
