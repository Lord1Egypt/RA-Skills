## Description:

Soulprint helps agents verify that a real human is behind a bot using local zero-knowledge identity proofs, on-chain registration, and reputation checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manuelfelipearias](https://clawhub.ai/user/manuelfelipearias)

### License/Terms of Use:


## Use Case:

External developers and agent operators use Soulprint to add identity verification, validator-node workflows, and reputation checks to AI bots, APIs, and MCP servers. Identity and face-match workflows should be run only in trusted environments because the release processes sensitive identity and biometric data.

### Deployment Geography for Use:

Global, with documented full identity-document support for Colombia.

## Known Risks and Mitigations:

Risk: Unpinned npm commands may install changing code while the skill processes sensitive identity and biometric data.

Mitigation: Review package provenance before installing, prefer exact pinned versions or a lockfile, and run identity verification only on a trusted machine.

Risk: Identity verification workflows may expose cedula or face-match data if storage, deletion, or network behavior is not understood.

Mitigation: Confirm what data is stored, deleted, or sent over the network before using the cedula or face-match workflow, and isolate wallets and API tokens from the process.

## Reference(s):

- [Soulprint documentation](https://soulprint.digital)
- [Soulprint ClawHub skill page](https://clawhub.ai/manuelfelipearias/skills/soulprint)
- [manuelfelipearias ClawHub publisher profile](https://clawhub.ai/user/manuelfelipearias)
- [soulprint npm package](https://www.npmjs.com/package/soulprint)
- [soulprint-network npm package](https://www.npmjs.com/package/soulprint-network)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with command, configuration, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes npm and npx commands plus TypeScript integration examples for MCP, Express, and Fastify.]

## Skill Version(s):

1.0.25 (source: server release metadata; artifact documentation describes Soulprint v0.6.4 behavior)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
