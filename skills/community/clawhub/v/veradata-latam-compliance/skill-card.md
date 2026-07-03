## Description: <br>
VeraData provides hosted LATAM compliance data through API calls for sanctions screening, KYB checks, registry lookup, central bank rates, and market intelligence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teodorofodocrispin-cmyk](https://clawhub.ai/user/teodorofodocrispin-cmyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to query VeraData's hosted service for LATAM sanctions, KYB, registry, rates, and market context when compliance screening or regional financial data is needed. <br>

### Deployment Geography for Use: <br>
Global, with LATAM-focused coverage <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends sanctions, KYB, registry, rates, or market-intelligence queries to VeraData's hosted service, which may involve regulated personal or business data. <br>
Mitigation: Use the service only when the organization approves the provider's retention and audit model; minimize submitted data and avoid unnecessary regulated identifiers. <br>
Risk: Paid calls use x402 USDC micropayments and can spend funds when payment signing is enabled. <br>
Mitigation: Start with trial mode where possible and require explicit operator approval, wallet controls, and budget limits before enabling paid calls or the remote MCP server. <br>
Risk: Compliance and registry decisions can depend on hosted API availability, source registry availability, and sanctions-list update timing. <br>
Mitigation: Handle API errors and trial limits explicitly, monitor the published health or OpenAPI endpoints, and verify high-impact decisions against authoritative sources. <br>


## Reference(s): <br>
- [VeraData OpenAPI specification](https://api.veradata.dev/openapi.json) <br>
- [VeraData x402 discovery](https://api.veradata.dev/.well-known/x402) <br>
- [VeraData MCP endpoint](https://api.veradata.dev/mcp) <br>
- [VeraData llms.txt](https://api.veradata.dev/llms.txt) <br>
- [VeraData public repository](https://github.com/teodorofodocrispin-cmyk/veradata-public) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with JSON response examples, curl commands, Python snippets, and MCP configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on VeraData hosted API availability, trial limits, and approved x402 payment controls.] <br>

## Skill Version(s): <br>
2.3.2 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
