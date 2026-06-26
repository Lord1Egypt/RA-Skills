## Description: <br>
Spraay Batch Payments helps agents send batch crypto payments and payroll through the Spraay x402 gateway across supported EVM chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[plagtech](https://clawhub.ai/user/plagtech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and finance operators use this skill to have an agent check balances, resolve ENS or Basename addresses, create invoices, and submit confirmed batch crypto payments or payroll through Spraay. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Blockchain payments can move real funds and may be irreversible. <br>
Mitigation: Require explicit user confirmation of the gateway URL, recipients, chain, token, amounts, and x402 fee before any paid endpoint or transfer. <br>
Risk: Paid endpoints may charge x402 micropayment fees. <br>
Mitigation: Show payment instructions or fee context to the user and obtain confirmation before retrying a request with payment proof. <br>
Risk: An incorrect gateway configuration could send requests to an unintended endpoint. <br>
Mitigation: Verify SPRAAY_GATEWAY_URL is the intended Spraay gateway before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/plagtech/spraay-payments) <br>
- [Server-resolved GitHub provenance](https://github.com/plagtech/spraay-payments) <br>
- [Spraay app](https://spraay.app) <br>
- [Spraay documentation](https://docs.spraay.app) <br>
- [Configured Spraay gateway endpoint](https://gateway.spraay.app) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with curl command examples and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SPRAAY_GATEWAY_URL, curl, jq, an x402-compatible wallet, and explicit user confirmation before payment execution.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
