## Description: <br>
Enables agents to create, manage, link, prove, and verify Billions Network decentralized identities using iden3 signatures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[masudijkp003-star](https://clawhub.ai/user/masudijkp003-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to create local DID identities, sign or verify ownership challenges, and link an agent identity to a human owner through the Billions Network. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles durable private keys and can store them with unsafe defaults. <br>
Mitigation: Set BILLIONS_NETWORK_MASTER_KMS_KEY before creating or importing identities, keep the master key outside chat and logs, and run the skill only on a trusted machine. <br>
Risk: Passing private keys on the command line can expose credentials through shell history or process inspection. <br>
Mitigation: Avoid command-line private key arguments unless there is an explicit, reviewed operational need; prefer generating new identities in a trusted environment. <br>
Risk: Signing a challenge or creating a human-agent linking URL can bind an agent identity to a user workflow. <br>
Mitigation: Require explicit user confirmation before signing challenges or creating linking URLs, and stop if identity checks or script execution fail. <br>
Risk: Server evidence marks the security verdict as suspicious. <br>
Mitigation: Review the publisher, Billions/iden3 workflow, and local key-storage behavior before installation or deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/masudijkp003-star/verified-agent-identity-masud) <br>
- [Publisher profile](https://clawhub.ai/user/masudijkp003-star) <br>
- [Billions Network](https://billions.network/) <br>
- [OpenClaw environment documentation](https://docs.openclaw.ai/help/environment) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON or text script outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local identity records, DID strings, verification URLs, challenge strings, and signature verification results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
