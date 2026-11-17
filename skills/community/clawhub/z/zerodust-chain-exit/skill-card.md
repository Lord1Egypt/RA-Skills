## Description:

Sweep 100% of native gas tokens from EIP-7702 compatible chains. Leaves exactly zero balance. Supports 25 mainnet chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zerodustxyz](https://clawhub.ai/user/zerodustxyz)

### License/Terms of Use:

MIT

## Use Case:

External wallet users and agents use this skill to sweep native gas-token balances, consolidate funds across supported EIP-7702 chains, and leave the source-chain balance at zero after user-approved signatures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended to empty the source-chain native-token balance, so incorrect chain, destination, amount, fee, expiry, or delegated-contract details could cause an unintended transfer.

Mitigation: Before signatures are requested, show the quote details and require explicit confirmation of the source chain, destination address, destination chain, amount, fees, expiry, and delegated contract.

Risk: The workflow relies on a third-party ZeroDust service and powerful wallet authorizations.

Mitigation: Use the skill only when the user trusts ZeroDust, reject blind signatures or broad delegations, and verify EIP-7702 and EIP-712 data in the wallet or with independent tooling.

Risk: Sweeps only work on EIP-7702 compatible chains.

Mitigation: Check the requested source chain against the supported-chain list before quoting or submitting a sweep.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zerodustxyz/skills/zerodust-chain-exit)
- [ZeroDust API Documentation](https://zerodust-backend-production.up.railway.app/docs)
- [ZeroDust API Base URL](https://zerodust-backend-production.up.railway.app)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ZERODUST_API_KEY for agent endpoints and user wallet signatures for sweeps.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
