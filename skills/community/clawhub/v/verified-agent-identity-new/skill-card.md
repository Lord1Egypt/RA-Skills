## Description: <br>
Billions decentralized identity for agents. Link agents to human identities using Billions ERC-8004 and Attestation Registries. Verify and generate authentication proofs. Based on iden3 self-sovereign identity protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ch4812](https://clawhub.ai/user/ch4812) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to create and manage decentralized agent identities, link an agent DID to a human owner, and sign or verify identity challenges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill manages reusable identity private keys and identity proofs, and the security review notes weak defaults and incomplete consent or disclosure boundaries. <br>
Mitigation: Set a strong BILLIONS_NETWORK_MASTER_KMS_KEY before creating or importing identities, restrict access to $HOME/.openclaw/billions, and run linking or signing commands only when intentionally sending a proof. <br>
Risk: Using the --key option with valuable wallet keys can expose high-value credentials to local storage and agent workflows. <br>
Mitigation: Use dedicated identity keys for this skill and avoid importing wallet keys that protect funds or other high-value assets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ch4812/verified-agent-identity-new) <br>
- [Billions Network](https://billions.network/) <br>
- [OpenClaw environment documentation](https://docs.openclaw.ai/help/environment) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local identity files under $HOME/.openclaw/billions when the user runs the provided scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
