## Description:

Wdh helps agents call paid-per-call WDH.sh CLI utilities for file transfer, URL shortening, Chart.js image rendering, hosted markdown pages, QR codes, feature requests, and support tickets, with payment settled in USDC on Base mainnet via x402.

This skill is ready for commercial/non-commercial use.

## Publisher:

[workingdevshero](https://clawhub.ai/user/workingdevshero)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and agents use this skill to run WDH.sh utilities when they need public file links, short URLs, rendered charts, hosted markdown, QR codes, or paid communication with the WDH team. It is intended for users who can provide a funded Base wallet and accept per-command USDC charges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commands require a wallet private key that can authorize paid x402 requests.

Mitigation: Use a dedicated low-balance Base wallet, never use a primary wallet key, and avoid logging or committing the private key.

Risk: Using bunx or npx without pinning can execute a newer CLI version than the one reviewed.

Mitigation: Pin @wdhsh/cli to a reviewed version before use.

Risk: Uploads and publishing commands can expose private documents, secrets, or long-lived public links.

Mitigation: Confirm each upload or paid command before running it and do not upload private documents or secrets.

Risk: Re-running feedback or support commands may create duplicate paid issues.

Mitigation: Confirm whether a request has already been submitted before repeating a paid feedback or support command.

## Reference(s):

- [WDH.sh homepage](https://wdh.sh)
- [WDH.sh docs](https://wdh.sh/docs)
- [@wdhsh/cli on npm](https://www.npmjs.com/package/@wdhsh/cli)
- [x402 protocol](https://x402.org)
- [Chart.js](https://www.chartjs.org/)
- [chartsplat docs](https://chartsplat.com/docs)
- [ClawHub skill page](https://clawhub.ai/workingdevshero/skills/wdh)
- [Publisher profile](https://clawhub.ai/user/workingdevshero)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and command-output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some invoked commands may produce URLs, PNG or SVG image files, hosted markdown pages, public file links, or issue links.]

## Skill Version(s):

0.3.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
