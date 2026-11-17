## Description:

Provides a defined Tushare Pro connector for 23 A-share stock data interfaces covering market data, stock reference data, adjustment factors, trading calendars, and related China equity datasets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaingush](https://clawhub.ai/user/gaingush)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative analysts use this skill to query supported Tushare Pro A-share stock datasets by API name, stock code, date range, fields, and interface-specific parameters. It is useful for market data retrieval, basic screening, backtesting inputs, and data exploration when the caller has valid Tushare credentials and data entitlements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Tushare API token and can expose credentials if users paste tokens into shared chat or invocation logs.

Mitigation: Configure TUSHARE_TOKEN through an environment variable or secret manager, and avoid sharing tokens in prompts or reusable invocation JSON.

Risk: The skill performs expected network calls to Tushare Pro and depends on account permissions, points, interface limits, and data freshness.

Mitigation: Install it only where Tushare Pro access is expected, verify account entitlements before relying on results, and handle delayed or empty data responses in downstream workflows.

Risk: The Python dependencies are specified with minimum versions rather than an exact lockfile.

Mitigation: Use a locked environment or pinned dependency set for reproducible deployments.

## Reference(s):

- [Tushare Pro official documentation](https://tushare.pro/document/2)
- [Tushare Pro token registration](https://tushare.pro)
- [ClawHub skill release page](https://clawhub.ai/gaingush/skills/tushare-stocks)

## Skill Output:

**Output Type(s):** [JSON, text, guidance]

**Output Format:** [JSON object containing success status, returned data or error text, count, columns when available, and request metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Calls require a supported api_name and either a Tushare token parameter or the TUSHARE_TOKEN environment variable.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
