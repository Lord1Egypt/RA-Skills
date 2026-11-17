## Description:

Handles permissions, address management, and inter-player coordination in Structs. Use when granting or revoking permissions on objects, registering new addresses, managing multi-address accounts, delegating authority to other players, or setting up address-level access control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abstrct](https://clawhub.ai/user/abstrct)

### License/Terms of Use:

MIT-0

## Use Case:

External Structs players and operators use this skill to inspect and change permissions, register or revoke addresses, and coordinate delegated access for players, objects, and guild ranks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact permission or identity changes could grant unintended control, revoke needed access, or orphan the operator's own signing access.

Mitigation: Confirm the target object, player, address, and permission bits before execution; prefer minimum necessary permissions and keep interactive confirmation enabled unless the exact transaction has already been deliberately approved.

Risk: Address registration or primary-address changes can attach an unintended signing key when proof material or the new address is untrusted.

Mitigation: Verify proof provenance and confirm the new address is controlled by the intended operator before registering it or making it primary.

## Reference(s):

- [Structs Safety](https://structs.ai/SAFETY)
- [Agent Security](https://structs.ai/awareness/agent-security)
- [Permission System Reference](https://structs.ai/knowledge/mechanics/permissions)
- [structsd Install Skill](https://structs.ai/skills/structsd-install/SKILL)
- [UGC Moderation Mechanics](https://structs.ai/knowledge/mechanics/ugc-moderation)
- [Transactions Mechanics](https://structs.ai/knowledge/mechanics/transactions)
- [Entity Relationships](https://structs.ai/knowledge/entities/entity-relationships)
- [Authentication Protocols](https://structs.ai/protocols/authentication)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline structsd commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires structsd on PATH and a configured signing key.]

## Skill Version(s):

1.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
