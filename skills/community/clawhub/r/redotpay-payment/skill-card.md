## Description:

Guides agents through RedotPay service discovery, endpoint inspection, pricing review, and user-confirmed CLI requests for data, media, model API, and MPP-style lookups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[turbo-wang](https://clawhub.ai/user/turbo-wang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find RedotPay-compatible services, inspect schemas and pricing, and make explicit user-approved requests through the RedotPay CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to install or expose the RedotPay payment CLI and create a persistent ~/.local/bin symlink.

Mitigation: Install the CLI through a trusted, verified process outside the skill and review persistent PATH changes before enabling the workflow.

Risk: Chargeable RedotPay requests can incur payment costs or expose sensitive wallet and payment metadata if handled carelessly.

Mitigation: Require explicit confirmation of amount, currency, and purpose; use a max spend cap; run wallet preflight before requests; and avoid printing tokens, wallet config, or verbose payment logs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/turbo-wang/skills/redotpay-payment)
- [RedotPay CLI Installation Reference](https://raw.githubusercontent.com/redotpay/redotpay-cli/v0.1.1/install.sh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command blocks and JSON-oriented CLI outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation, wallet login preflight, and a spend cap before chargeable RedotPay requests.]

## Skill Version(s):

0.1.7 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
