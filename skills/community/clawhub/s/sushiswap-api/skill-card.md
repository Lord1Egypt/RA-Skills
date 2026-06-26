## Description: <br>
REST API for optimized token swapping, executable transaction generation, swap quoting, pricing, token metadata, and liquidity-source discovery using the SushiSwap Aggregator. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xMasayoshi](https://clawhub.ai/user/0xMasayoshi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to construct SushiSwap REST API requests for quotes, swaps, token prices, token metadata, and supported liquidity sources. It is intended for integrations that need schema-grounded HTTP access to SushiSwap Aggregator behavior rather than assumptions or a JavaScript SDK. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Swap endpoints can generate executable transaction data for financial actions. <br>
Mitigation: Before signing or submitting a transaction, verify the chain, token addresses, amount, recipient, slippage, fee and fee receiver, referrer, target contract, and transaction value. <br>
Risk: Using the SwaggerHub mock server instead of the production Sushi API server can produce non-production behavior. <br>
Mitigation: Pin integrations to https://api.sushi.com for production API calls. <br>
Risk: API changes can make hardcoded endpoints, parameters, or response shapes stale. <br>
Mitigation: Re-read references/openapi.yaml before constructing requests and update request construction to match the active schema. <br>


## Reference(s): <br>
- [OpenAPI usage guide](references/OPENAPI.md) <br>
- [Sushi API OpenAPI schema](references/openapi.yaml) <br>
- [Sushi API production server](https://api.sushi.com) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with HTTP parameters, JSON-oriented response guidance, and code or shell snippets when useful] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be grounded in references/openapi.yaml and should not fabricate transaction calldata.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
