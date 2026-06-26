## Description: <br>
Handles permissions, address management, and inter-player coordination in Structs for granting or revoking permissions, registering addresses, managing multi-address accounts, delegating authority, and setting up address-level access control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abstrct](https://clawhub.ai/user/abstrct) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Structs users and agent operators use this skill to prepare and verify wallet-backed permission, delegation, address registration, address revocation, and primary-address update operations. It is intended for workflows where the user must review sensitive identifiers, proof material, permission bitmasks, and transaction approval before execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Permission grants, PermAll, address registration, address revocation, and primary-address changes can alter control of Structs assets or identity. <br>
Mitigation: Require explicit approval for sensitive operations and verify the wallet, object ID, player ID, address, proof material, and permission bitmask before any transaction. <br>
Risk: Suppressing CLI confirmation with approved transaction flags can execute sensitive wallet-backed operations without an interactive prompt. <br>
Mitigation: Use interactive transaction flags by default and allow prompt suppression only after the user has approved the exact operation and parameters. <br>
Risk: Invalid or attacker-supplied proof material during address registration can attach an unintended signing key. <br>
Mitigation: Verify proof provenance and signature material before address registration, then query the registered address and linked player after execution. <br>


## Reference(s): <br>
- [Structs Diplomacy on ClawHub](https://clawhub.ai/abstrct/structs-diplomacy) <br>
- [Structs Safety](https://structs.ai/SAFETY) <br>
- [Structs Agent Security](https://structs.ai/awareness/agent-security) <br>
- [Structs Permission Mechanics](https://structs.ai/knowledge/mechanics/permissions) <br>
- [Structs UGC Moderation Mechanics](https://structs.ai/knowledge/mechanics/ugc-moderation) <br>
- [Structs Transaction Mechanics](https://structs.ai/knowledge/mechanics/transactions) <br>
- [Structs Entity Relationships](https://structs.ai/knowledge/entities/entity-relationships) <br>
- [Structs Authentication Protocols](https://structs.ai/protocols/authentication) <br>
- [structsd Install Skill](https://structs.ai/skills/structsd-install/SKILL) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline structsd shell commands and verification steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires structsd on PATH, a configured signing key, explicit user approval for sensitive transactions, and verification of wallet, object ID, player ID, address, proof material, and permission bitmask before execution.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
