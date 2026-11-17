## Description:

Searches and calls monetized AI skills from Skillz Market with automatic USDC payments on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hiich](https://clawhub.ai/user/hiich)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to search Skillz Market, inspect paid AI services, and call x402-enabled endpoints from an OpenClaw agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a wallet private key to make automatic paid requests, including requests to arbitrary direct endpoints.

Mitigation: Use a dedicated low-balance wallet, avoid direct endpoint calls unless the endpoint is trusted, and review the service and price before calling.

Risk: Skill calls and direct calls may send user payloads to external endpoints.

Mitigation: Avoid sensitive payloads and prefer verified marketplace skills or trusted endpoints.

Risk: Dependencies are version-ranged and no lockfile evidence was provided.

Mitigation: Review installed dependency versions before deployment and prefer a release with pinned dependencies and a lockfile.

## Reference(s):

- [Skillz Market](https://skillz.market)
- [x402 Protocol](https://x402.org)
- [ClawHub SkillzMarket release page](https://clawhub.ai/hiich/skills/skillzmarket)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Terminal output and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires npx for CLI execution and SKILLZ_PRIVATE_KEY for paid calls.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata; package.json reports 0.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
