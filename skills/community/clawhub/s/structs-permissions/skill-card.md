## Description:

Permissions, address management, and delegation in Structs for granting or revoking object and address permissions, registering signing keys, managing multi-address accounts, and setting up minimum-permission delegate agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abstrct](https://clawhub.ai/user/abstrct)

### License/Terms of Use:

MIT-0

## Use Case:

External Structs players, developers, and agent operators use this skill to manage permission bitmasks, signing keys, address registration, and delegated worker access with minimum necessary authority.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Overbroad grants such as PermAll can give a delegate total control.

Mitigation: Review every generated transaction before signing and grant only the minimum permission bits required for the task.

Risk: Registering an address with unverified proof material can attach an attacker-controlled signing key.

Mitigation: Verify address-registration proofs and only register keys under the user's control.

Risk: Delegate keys can retain authority after their intended job ends.

Mitigation: Audit permissions after changes and revoke delegate permissions promptly when no longer needed.

## Reference(s):

- [Structs conventions](https://structs.ai/skills/conventions)
- [Structs permissions mechanics](https://structs.ai/knowledge/mechanics/permissions)
- [Structs agent security](https://structs.ai/awareness/agent-security)
- [Structs authentication protocol](https://structs.ai/protocols/authentication)
- [Structs async operations](https://structs.ai/awareness/async-operations)
- [structsd install skill](https://structs.ai/skills/structsd-install/SKILL)
- [Structs team operations](https://structs.ai/playbooks/meta/team-operations)
- [Structs guild skill](https://structs.ai/skills/structs-guild/SKILL)
- [Structs streaming skill](https://structs.ai/skills/structs-streaming/SKILL)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and reference tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides permission bit values, transaction command patterns, delegation recipes, verification queries, and operational cautions.]

## Skill Version(s):

1.25.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
