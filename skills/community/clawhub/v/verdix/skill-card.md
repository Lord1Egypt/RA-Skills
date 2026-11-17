## Description:

Guides agents to screen Base recipient addresses with Verdix before sending funds and explain any risk signals found.

This skill is ready for commercial/non-commercial use.

## Publisher:

[verdixapi](https://clawhub.ai/user/verdixapi)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their users check unfamiliar Base recipient addresses before transfers or payments, then review the verdict and reasons before deciding whether to proceed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A real check shares the recipient address with a third-party service and may spend USDC.

Mitigation: Obtain user consent before a paid check and enforce the selected tier, price and wallet spending limits.

Risk: A clean verdict may miss new threats or checks that were not performed.

Mitigation: Explain the verdict's limits, show the checks performed and never present a lite no_known_risk result as a safety guarantee.

Risk: Address lookalikes can lead to an unintended transfer.

Mitigation: Confirm the full recipient address with the user before a large transfer.

## Reference(s):

- [Verdix skill on ClawHub](https://clawhub.ai/verdixapi/skills/verdix)
- [Verdix agent documentation](https://api.verdixapi.com/llms.txt)
- [Verdix API specification](https://api.verdixapi.com/openapi.json)
- [Verdix pricing](https://api.verdixapi.com/pricing)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports the address, selected tier, verdict, reasons and checks performed; advises whether to pause or proceed.]

## Skill Version(s):

1.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
