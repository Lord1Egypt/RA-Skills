## Description:

Discovers, inspects, and requests RedotPay services and data through the RedotPay CLI across media generation, model APIs, data APIs, and commerce lookups while excluding purchase flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[turbo-wang](https://clawhub.ai/user/turbo-wang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to search RedotPay service catalogs, inspect endpoint schemas and pricing, and make confirmed data requests through the RedotPay CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow references a remote installer for a payment-capable CLI.

Mitigation: Install only from a trusted RedotPay CLI source, prefer a signed or package-manager installation, and verify installer integrity before use.

Risk: Paid RedotPay requests can incur charges.

Mitigation: Inspect service pricing, quote the exact amount and currency, set --max-spend or REDOTPAY_CLI_MAX_SPEND, and wait for explicit user confirmation before each paid request.

Risk: Login tokens, wallet configuration, or payment metadata could be exposed in chat or verbose output.

Mitigation: Do not expose OAuth tokens, keys, wallet config, or verbose payment metadata; display only the QR login artifact needed for authorization.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/turbo-wang/skills/redotpay-wallet)
- [RedotPay CLI installer reference](https://raw.githubusercontent.com/redotpay/redotpay-cli/v0.1.0/install.sh)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON CLI output references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the redotpay CLI; paid requests require explicit user confirmation and a spend cap.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
