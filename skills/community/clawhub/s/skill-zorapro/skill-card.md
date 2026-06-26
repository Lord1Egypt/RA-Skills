## Description: <br>
Generates a Nano Banana style NFT and deploys it to the Zora Network. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eshraqism](https://clawhub.ai/user/eshraqism) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and creators use this skill to generate Nano Banana style character artwork, upload it to IPFS, and deploy a Zora NFT collection from a prompt. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use a raw wallet private key to submit live Zora blockchain transactions without an explicit review or confirmation step. <br>
Mitigation: Use a dedicated low-value deployment wallet, avoid primary wallet keys, and review transaction details with an external signer or wallet flow before broadcast. <br>
Risk: The skill depends on live external services and unpinned Python packages for image generation, Web3 access, and HTTP requests. <br>
Mitigation: Pin dependencies, review package versions before installation, and run the skill in an isolated environment with only the required credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eshraqism/skill-zorapro) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, configuration] <br>
**Output Format:** [Plain text status with a transaction hash and generated image file path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GEMINI_API_KEY, PRIVATE_KEY, and ZORA_RPC_URL environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
