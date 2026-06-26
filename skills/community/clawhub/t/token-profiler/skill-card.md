## Description: <br>
One API call replaces CoinGecko + DexScreener + GoPlus + on-chain queries. Enriched token data from 5 sources, clean JSON, under 3 seconds. Free, no key needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vswarm-ai](https://clawhub.ai/user/vswarm-ai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and developers use this skill to look up public token price, market, holder, security, social, and DEX information from a single network endpoint. It is intended for token data retrieval, not as the sole basis for trading or investment decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Token names or contract addresses are sent to a declared third-party endpoint. <br>
Mitigation: Use the skill for public token lookups only, and do not send private wallet details, API keys, seed phrases, or confidential trading strategy. <br>
Risk: Token profile data and security fields can be incomplete, stale, or insufficient for financial decisions. <br>
Mitigation: Treat outputs as informational data, verify important results with authoritative sources, and do not use the skill as the sole basis for trading or investment decisions. <br>


## Reference(s): <br>
- [Token Profiler on ClawHub](https://clawhub.ai/vswarm-ai/token-profiler) <br>
- [Declared Token Profiler API endpoint](https://verdictswarm-production-7460.up.railway.app) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, text, guidance] <br>
**Output Format:** [Structured JSON token profile with concise text answers based on requested fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a network call to the declared third-party endpoint; no API key is required for the documented free tier.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
