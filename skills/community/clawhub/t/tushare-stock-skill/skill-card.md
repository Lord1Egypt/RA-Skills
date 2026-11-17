## Description:

TuShare Stock Skill helps agents query Tushare data for China A-share equities and produce stock research, valuation, risk, and trading-observation analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[magica-chen](https://clawhub.ai/user/magica-chen)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to retrieve China A-share market data through Tushare and generate concise stock research, financial-quality analysis, risk notes, and technical trading observations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a user-provided Tushare token for market-data queries.

Mitigation: Provide the token through TUSHARE_TOKEN when possible and avoid broad env files; if TUSHARE_STOCK_ENV_FILE is used, point it to a minimal file containing only that token.

Risk: Live queries and catalog refreshes make network requests to Tushare services.

Mitigation: Run the skill in an environment where outbound access to api.waditu.com and tushare.pro is expected and review returned data before relying on analysis.

Risk: Cached stock metadata may be written to a shared temporary directory by default.

Mitigation: Set TUSHARE_STOCK_CACHE_DIR to a private per-user cache directory when cache contents or local multi-user isolation matter.

Risk: The dependency set is installed from Python packages and includes market-data and web-request libraries.

Mitigation: Install the skill in a virtual environment and manage dependency versions according to local security policy.

Risk: Some catalog entries can reach adjacent non-A-share or cross-market Tushare endpoints.

Mitigation: Keep prompts and explicit endpoint calls scoped to China A-share workflows and review the reported endpoint before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/magica-chen/skills/tushare-stock-skill)
- [Project homepage](https://github.com/Magica-Chen/tushare-stock-skill)
- [Tushare official stock-data index](https://tushare.pro/document/2?doc_id=14)
- [Stock endpoint catalog](references/stock_endpoints.md)
- [Machine-readable stock endpoint catalog](references/stock_endpoints.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Simplified Chinese text and structured JSON, with Markdown documentation and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided TUSHARE_TOKEN for live Tushare queries; query results may reflect Tushare point thresholds and endpoint permissions.]

## Skill Version(s):

1.0.3 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
