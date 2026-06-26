## Description: <br>
Scans a Solana wallet for reclaimable SOL from dormant token accounts and program buffer accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nedim1511](https://clawhub.ai/user/nedim1511) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to check whether a Solana public wallet address has reclaimable SOL from dormant token accounts or program buffer accounts. The scan is read-only and returns totals that help the user decide whether to claim through Unclaimed SOL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A scan sends the user's public Solana wallet address to the Unclaimed SOL API. <br>
Mitigation: Disclose the API call and obtain user consent before running the scan. <br>
Risk: Users could confuse the scan with wallet recovery or transaction signing. <br>
Mitigation: Ask only for Solana public addresses and never request private keys, seed phrases, mnemonics, or signing approval. <br>
Risk: The external API may be unavailable or return unexpected data. <br>
Mitigation: Surface a concise failure message and direct users to Unclaimed SOL for a manual check. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/nedim1511/unclaimed-sol-scanner) <br>
- [Unclaimed SOL](https://unclaimedsol.com) <br>
- [Privacy Policy](https://blog.unclaimedsol.com/privacy-policy/) <br>
- [Fee Schedule](https://unclaimedsol.com/fees/) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, API Calls, Shell commands, Markdown, Guidance] <br>
**Output Format:** [Markdown summary with JSON-derived SOL totals and optional shell command execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user consent before sending a public Solana wallet address to the Unclaimed SOL API.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
