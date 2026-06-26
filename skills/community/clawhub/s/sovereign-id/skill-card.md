## Description: <br>
Enables agents to manage decentralized identities, create pairwise DIDs, sign B2B mandates, and generate selective disclosure proofs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TamTunnel](https://clawhub.ai/user/TamTunnel) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add local self-sovereign identity workflows for B2B mandate signing, B2C pairwise identifiers, and selective disclosure of claims. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent authority to maintain a persistent local signing identity and create signed business mandates. <br>
Mitigation: Require explicit user approval for each mandate, especially financial or legal actions, and inspect the mandate payload before signing. <br>
Risk: Signing credentials depend on CLAW_PASSWORD and the local .env.agent identity file. <br>
Mitigation: Treat CLAW_PASSWORD and .env.agent as signing credentials, keep them out of prompts and logs, and avoid sharing them with other agents or services. <br>
Risk: The security review warns that DID verification is not a complete trust-chain validation. <br>
Mitigation: Do not rely on verify_did.ts as full DID, credential, or counterparty trust validation; add independent policy checks before accepting proofs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TamTunnel/sovereign-id) <br>
- [Publisher profile](https://clawhub.ai/user/TamTunnel) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with TypeScript and shell command usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local identity files, signed mandate JSON, public JWK material, selective disclosure JWT examples, and verification status output when scripts are executed.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
