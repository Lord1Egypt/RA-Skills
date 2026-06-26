## Description: <br>
Automates WEEX futures and spot trading workflows, including order placement, cancellation, order lookup, market data retrieval, and account data retrieval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iiiiicooper](https://clawhub.ai/user/iiiiicooper) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading operators use this skill in agent coding environments to query WEEX market and account data and to prepare or execute structured futures and spot order actions through the included REST helpers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send live authenticated WEEX trading requests, including mutating order actions. <br>
Mitigation: Use read-only or narrowly scoped API keys when possible, keep withdrawal permissions disabled, and require explicit human confirmation before using commands with --confirm-live. <br>
Risk: Generic endpoint calls and bundled endpoint definitions expose sensitive actions such as affiliate, rebate, internal withdrawal, cancel-all, close-all, leverage, and margin changes. <br>
Mitigation: Avoid the generic caller for those endpoint groups unless the user explicitly requests the exact action and the request parameters have been reviewed. <br>
Risk: Environment variables for WEEX credentials can grant account access if shared, committed, or stored too broadly. <br>
Mitigation: Store credentials only in the needed shell environment, never commit them, rotate exposed keys immediately, and prefer temporary or least-privilege keys. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iiiiicooper/weex) <br>
- [Auth and Signing](references/auth-and-signing.md) <br>
- [WEEX Spot Endpoint Summary](references/spot-endpoints.md) <br>
- [WEEX Contract Endpoint Summary](references/contract-endpoints.md) <br>
- [WEEX Spot API Definitions](references/spot-api-definitions.md) <br>
- [WEEX Contract API Definitions](references/contract-api-definitions.md) <br>
- [WEEX Signature Documentation](https://www.weex.com/api-doc/spot/QuickStart/Signature) <br>
- [WEEX Contract Place Order Documentation](https://www.weex.com/api-doc/contract/Transaction_API/PlaceOrder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, API calls, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Private endpoints require WEEX_API_KEY, WEEX_API_SECRET, and WEEX_API_PASSPHRASE environment variables.] <br>

## Skill Version(s): <br>
1.0.1 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
