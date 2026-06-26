## Description: <br>
Consult and operate against the Hyperliquid Names API for .hl name resolution, reverse lookups, profile and record retrieval, owner or list queries, mint-pass preparation, API diagnostics, and HyperEVM dApp integration guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hlndev](https://clawhub.ai/user/hlndev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use this skill to query HL Names APIs, resolve .hl names and wallet addresses, interpret profile and record payloads, troubleshoot validation errors, and guide HyperEVM wallet, dApp, or mint-pass integration work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: HL Names API requests can expose queried wallet addresses, names, and request context to HLN. <br>
Mitigation: Avoid sensitive lookups unless that disclosure is acceptable, and prefer a user-controlled HLN API key for accountable use. <br>
Risk: The skill includes a public fallback API key for HL Names API access. <br>
Mitigation: Use a dedicated HLN API key when possible, especially for production or attributable usage. <br>
Risk: The bundled eval runner can send prompts, responses, or secrets to configured model providers. <br>
Mitigation: Do not run evaluations with proprietary prompts or secrets unless that provider disclosure is intended. <br>


## Reference(s): <br>
- [HLN API Endpoints](references/endpoints.md) <br>
- [HyperEVM dApp Integration](references/integration.md) <br>
- [Validation And Errors](references/validation-and-errors.md) <br>
- [Skill Homepage](https://github.com/HLnames/use_hln_api_skill) <br>
- [Production Swagger Docs](https://api.hlnames.xyz/api/docs/) <br>
- [HLN API Minting Examples](https://github.com/HLnames/hln_api_minting) <br>
- [Dynamic Integration Example](https://github.com/ori-wagmi/hlnames_dynamic) <br>
- [ClawHub Skill Page](https://clawhub.ai/hlndev/use-hln-api) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with endpoint selections, request examples, JSON interpretation notes, and occasional code or shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should identify the selected endpoint, expected identifier shape, relevant environment, and next useful follow-up call when helpful.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
