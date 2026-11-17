## Description:

How to create and use AccountAddress in @aptos-labs/ts-sdk, including AIP-40 address formats, relaxed and strict parsing, special addresses, string output forms, and derived address helpers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iskysun96](https://clawhub.ai/user/iskysun96)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill for concise guidance on creating, validating, comparing, formatting, and deriving Aptos account addresses with @aptos-labs/ts-sdk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Address strings may be compared or normalized incorrectly when used directly.

Mitigation: Use AccountAddress.from() for normalization and equals() for comparisons, as described by the skill.

Risk: Manually deriving object, resource, token, or user-derived addresses can produce incorrect Aptos addresses.

Mitigation: Use the SDK helper functions covered by the skill instead of hand-rolled hashing.

## Reference(s):

- [AIP-40 address format](https://github.com/aptos-foundation/AIPs/blob/main/aips/aip-40.md)

## Skill Output:

**Output Type(s):** [guidance, code]

**Output Format:** [Markdown with TypeScript code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only SDK usage guidance; no executable behavior is included in the artifact.]

## Skill Version(s):

1.0.0 (source: server release metadata; SKILL.md frontmatter version is 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
