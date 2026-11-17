## Description:

Consult and operate against the Hyperliquid Names API for .hl resolution, reverse lookups, profiles, records, owner and list queries, mint-pass preparation, and HyperEVM integration guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hlndev](https://clawhub.ai/user/hlndev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to query and interpret Hyperliquid Names API data, choose the right endpoint, validate identifiers, troubleshoot API failures, and prepare HyperEVM integration or mint-pass workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The packaged evaluation runner may handle API keys and live mint-pass authorization data.

Mitigation: Use only the canonical skill directory for normal API guidance, and run eval tooling only after reviewing the environment, model provider configuration, base URL, and local result retention.

Risk: Live mint-pass responses are short-lived authorization data for downstream minting workflows.

Mitigation: Request mint-pass data only when ready to continue promptly, avoid echoing signatures unnecessarily, and keep generated result artifacts out of shared locations.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hlndev/skills/use-hln-api)
- [HLN API Endpoints](references/endpoints.md)
- [HyperEVM dApp Integration](references/integration.md)
- [Validation And Errors](references/validation-and-errors.md)
- [Production Swagger Docs](https://api.hlnames.xyz/api/docs/)
- [Production API](https://api.hlnames.xyz/)
- [Testnet API](https://api.testnet.hlnames.xyz/)
- [Dynamic Integration Reference](https://github.com/ori-wagmi/hlnames_dynamic)
- [HLN API Minting Reference](https://github.com/HLnames/hln_api_minting)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with endpoint references, JSON examples, code snippets, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API endpoints, request headers, identifier validation notes, and concise follow-up recommendations.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
