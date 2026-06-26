## Description: <br>
Wdh helps an agent call seven paid-per-call WDH.sh CLI utilities for file transfer, URL shortening, Chart.js rendering, hosted markdown pages, QR codes, paid feature requests, and paid support tickets using USDC on Base mainnet via x402. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[workingdevshero](https://clawhub.ai/user/workingdevshero) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill when they need paid WDH.sh utility calls for publishing or sharing files and markdown, generating QR codes or charts, shortening URLs, or filing paid feedback and support requests. The user or agent must have a funded EVM wallet and understand that calls may spend USDC. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: WDH.sh commands can publish files, markdown, shortened links, tickets, or generated assets to external hosted URLs. <br>
Mitigation: Review and redact content before running commands, especially credentials, private notes, customer data, internal documents, and business-sensitive files. <br>
Risk: The skill requires WDH_WALLET_PRIVATE_KEY and signs paid x402 transactions using a USDC-funded wallet. <br>
Mitigation: Use a dedicated low-balance wallet for agent activity, store the private key only in the intended environment variable, and remove or rotate it when no longer needed. <br>
Risk: Some commands spend USDC and repeated feedback or support submissions can create duplicate charges. <br>
Mitigation: Confirm command cost and intent before execution, and avoid retrying paid feedback or support commands unless a duplicate charge is acceptable. <br>
Risk: Short links persist indefinitely by default and uploaded files or markdown pages remain public until their configured expiration. <br>
Mitigation: Set explicit expiration values for temporary content and avoid using permanent links for sensitive or revocable material. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/workingdevshero/wdh) <br>
- [WDH.sh homepage](https://wdh.sh) <br>
- [WDH.sh docs](https://wdh.sh/docs) <br>
- [@wdhsh/cli on npm](https://www.npmjs.com/package/@wdhsh/cli) <br>
- [x402 protocol](https://x402.org) <br>
- [Chart.js](https://www.chartjs.org/) <br>
- [chartsplat docs](https://chartsplat.com/docs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may lead to CLI calls that return public URLs, issue URLs, file paths, or raw PNG/SVG image bytes depending on the WDH.sh utility used.] <br>

## Skill Version(s): <br>
0.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
