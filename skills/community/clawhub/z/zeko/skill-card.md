## Description:

Guides users and developers through Zeko bridging, testnet funding, network queries, and zkApp development with terminal-first workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hebilicious](https://clawhub.ai/user/hebilicious)

### License/Terms of Use:

MIT-0

## Use Case:

Users and developers use this skill to navigate Zeko bridge and faucet workflows, query live or historical network data, and build zkApps with o1js or OCaml. Legacy Mina-backed commands apply only to explicitly selected legacy networks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended transactions can sign and submit actions using a private key.

Mitigation: Use isolated test keys and require explicit confirmation before any signing or transaction submission.

Risk: Unpinned CLI downloads can introduce unreviewed code during execution.

Mitigation: Review the skill before installing and pin or preinstall the required CLI packages.

Risk: Credentials can leak through shared shells or logs.

Mitigation: Use least-privilege tokens and avoid pasting secrets into shared shells or logs.

## Reference(s):

- [Zeko skill release on ClawHub](https://clawhub.ai/hebilicious/skills/zeko)
- [Zeko agent skills documentation](https://docs.zeko.io/developers/tools/agent-skills)
- [Zeko bridge guide](https://docs.zeko.io/users/guides/zeko-bridge)
- [Zeko developer getting started](https://docs.zeko.io/developers/getting-started)
- [o1js documentation](https://docs.o1labs.org/o1js/)
- [Bridge and faucet workflows](references/30-bridge-and-faucet.md)
- [Endpoints and curl examples](references/40-endpoints-and-curl.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with code and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Transaction commands may sign and submit on-chain actions; confirm the target network and obtain explicit approval before execution.]

## Skill Version(s):

0.0.1-main.20.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
