## Description: <br>
RedotPay Wallet helps an agent discover RedotPay services, inspect schemas and pricing, and make wallet-backed service requests only after explicit confirmation and spend-cap checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[turbo-wang](https://clawhub.ai/user/turbo-wang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search RedotPay service catalogs, inspect available endpoints and pricing, and request media, model API, data API, or commerce lookup results through the RedotPay CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet-backed requests can incur a charge if an agent proceeds without clear approval. <br>
Mitigation: Before any paid request, require the exact service, endpoint, amount, currency, purpose, expected return, explicit user confirmation, and a spend cap. <br>
Risk: OAuth tokens, wallet configuration, or payment metadata may be exposed in chat or verbose command output. <br>
Mitigation: Do not expose tokens, keys, or wallet config in chat, and use verbose CLI output sparingly because stderr may include payment metadata. <br>
Risk: The CLI installer is a separate supply-chain trust decision. <br>
Mitigation: Verify the RedotPay CLI installer from RedotPay's official source before running it. <br>


## Reference(s): <br>
- [ClawHub RedotPay Wallet release](https://clawhub.ai/turbo-wang/redotpay) <br>
- [RedotPay CLI installer](https://raw.githubusercontent.com/redotpay/redotpay-cli/v0.1.0/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the redotpay CLI; paid requests require explicit user confirmation and a spend cap.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
