## Description:

Automates TRON energy rental through TRXDO to help reduce smart contract and USDT transaction fees.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itfers](https://clawhub.ai/user/itfers)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to let an agent query TRXDO account information and submit TRON energy rental orders from chat commands for fee optimization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid TRON energy rental orders can be triggered from chat commands without built-in confirmation, authorization, or spending limits.

Mitigation: Before connecting funded TRXDO credentials, add confirmation, admin allowlisting, strict quantity limits, TRON address validation, rate limits, and safer secret storage.

Risk: Configured TRXDO user ID and secret key are used to sign API requests.

Mitigation: Store credentials outside shared skill files, restrict file access, rotate exposed keys, and avoid committing populated config.json.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/itfers/skills/tron-energy-rental)
- [TRXDO energy rental platform](https://www.trxdo.com)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, code, API calls, configuration]

**Output Format:** [Plain text command responses with Python, C#, and JSON configuration artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configured TRXDO credentials to sign account, order submission, and order query API requests.]

## Skill Version(s):

1.0.1 (source: server release metadata, created 2026-05-25)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
