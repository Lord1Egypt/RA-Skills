## Description:

Generates a Nano Banana style NFT and deploys it to the Zora Network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eshraqism](https://clawhub.ai/user/eshraqism)

### License/Terms of Use:


## Use Case:

Developers and creators can use this skill to generate character art and deploy it as an NFT collection on the Zora Network. It is intended for workflows that connect image generation, IPFS upload, and on-chain NFT contract deployment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests a raw wallet private key and can sign and broadcast blockchain transactions.

Mitigation: Use only a dedicated low-value deployment wallet, require manual transaction review before broadcast, and avoid primary or funded wallets.

Risk: On-chain deployment behavior may proceed without an explicit confirmation or transaction preview path.

Mitigation: Add transaction preview, chain validation, contract validation, and explicit user confirmation before routine use.

Risk: Unpinned dependencies can change behavior across installs.

Mitigation: Pin and review dependencies before production or routine deployment.

## Reference(s):

- [Zora RPC endpoint](https://rpc.zora.energy)
- [ClawHub skill page](https://clawhub.ai/eshraqism/skills/skill-zorapro)
- [Publisher profile](https://clawhub.ai/user/eshraqism)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with Python-oriented usage guidance and status strings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require GEMINI_API_KEY, PRIVATE_KEY, and ZORA_RPC_URL environment variables for full operation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
