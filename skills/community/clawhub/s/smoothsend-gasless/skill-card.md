## Description:

Guides developers through sponsoring gas fees for Aptos dApp users with SmoothSend, including wallet adapter integration and fee-in-token stablecoin transfers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iskysun96](https://clawhub.ai/user/iskysun96)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building Aptos dApps use this skill to integrate SmoothSend so end users can submit transactions without holding APT for gas. It covers wallet adapter setup, fee-in-token stablecoin transfers, billing-related error handling, and common integration mistakes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill advises frontend environment variables for a paid-service API key, which can expose credit-bearing credentials in public bundles.

Mitigation: Use a backend integration or vendor-supported restrictions, quotas, and transaction policy controls before exposing any key tied to mainnet credits.

Risk: The skill references unpinned npm and npx package usage.

Mitigation: Pin package versions, review package provenance, and avoid running unreviewed npx commands in environments with sensitive secrets.

Risk: Mainnet usage depends on SmoothSend credits and can fail when credits are exhausted.

Mitigation: Handle HTTP 402 or insufficient-credit errors with a clear user-facing fallback and monitor billing before enabling mainnet sponsorship.

## Reference(s):

- [SmoothSend Docs](https://docs.smoothsend.xyz)
- [SmoothSend Pricing](https://docs.smoothsend.xyz/pricing)
- [SmoothSend Dashboard](https://dashboard.smoothsend.xyz)
- [@smoothsend/sdk on npm](https://www.npmjs.com/package/@smoothsend/sdk)
- [ClawHub skill page](https://clawhub.ai/iskysun96/skills/smoothsend-gasless)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with TypeScript, TSX, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes environment variable names, package installation commands, service links, and integration caveats.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
