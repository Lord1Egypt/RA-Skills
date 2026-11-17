## Description:

How to read on-chain data in @aptos-labs/ts-sdk with view(), getBalance(), getAccountInfo(), getAccountResources(), getAccountModules(), and getResource().

This skill is ready for commercial/non-commercial use.

## Publisher:

[iskysun96](https://clawhub.ai/user/iskysun96)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to generate guidance and TypeScript examples for read-only Aptos on-chain data queries, including balances, account metadata, resources, modules, and Move view function calls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Aptos SDK method names or return shapes may differ from the installed @aptos-labs/ts-sdk version.

Mitigation: Check the installed SDK version and confirm exact method names and return types before using the examples in production code.

Risk: Move u128 and u256 values can lose precision if handled as JavaScript numbers.

Mitigation: Use bigint conversion for large Move integer return values, as shown in the skill guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iskysun96/skills/ts-sdk-view-and-query)

## Skill Output:

**Output Type(s):** [guidance, markdown, code]

**Output Format:** [Markdown with TypeScript code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only SDK guidance; no executable code is installed by the skill.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
