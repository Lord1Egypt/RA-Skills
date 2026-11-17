## Description:

Guides agents and developers through token launch planning, fee management, claiming, recipient updates, and secure transaction preparation across Tator, Clanker, Flaunch, and Pump.fun workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[azep-ninja](https://clawhub.ai/user/azep-ninja)

### License/Terms of Use:


## Use Case:

External agent builders and developers use this skill to evaluate token launch ideas, prepare launch or fee-management actions, and choose between an API-mediated Tator workflow and direct platform integration. It is intended for users who can review blockchain transactions and manage wallet signing safely.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides users through irreversible token deployments, fee-recipient changes, claims, and other externally prepared blockchain transaction payloads.

Mitigation: Decode and simulate every transaction, verify contract addresses and endpoints independently, and require human approval before signing or broadcasting.

Risk: Direct Mode can require private signing keys, RPC endpoints, and IPFS credentials in the user's own infrastructure.

Mitigation: Use a dedicated minimally funded launch wallet, store secrets in a secrets manager, pin dependencies, and avoid autonomous unsupervised signing.

Risk: The authoritative security verdict is suspicious because validation controls for externally constructed transaction payloads are incomplete.

Mitigation: Install only after reviewing the third-party service or SDK path, then apply the security guidance from evidence before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/azep-ninja/skills/tator-launch-pad)
- [Tator Documentation](https://docs.tator.bot)
- [Token Launcher Direct Mode Reference](REFERENCE.md)
- [Clanker v4 Direct Mode Reference](references/clanker.md)
- [Clanker SDK Documentation](https://clanker.gitbook.io/clanker-documentation/sdk/v4.0.0)
- [Flaunch Direct Mode Reference](references/flaunch.md)
- [Flaunch Builder Documentation](https://docs.flaunch.gg/for-builders)
- [Pump.fun Direct Mode Reference](references/pumpfun.md)
- [Pump.fun Public Documentation](https://github.com/pump-fun/pump-public-docs)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline JSON, TypeScript, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only; users must review, sign, and broadcast any blockchain transactions outside the skill.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
