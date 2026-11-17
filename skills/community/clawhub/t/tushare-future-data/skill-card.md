## Description:

Tushare 期货数据 helps agents query supported Tushare Pro futures-market data, including contract metadata, trading calendars, market bars, warehouse receipts, settlement data, holding rankings, indexes, and limit data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaingush](https://clawhub.ai/user/gaingush)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative research users can use this skill to have an agent retrieve Tushare Pro futures data through a bounded set of documented interfaces. It is suited for workflows that need contract lookup, historical or real-time futures bars, warehouse receipt data, settlement data, position rankings, index data, and related futures-market reference data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill needs a Tushare API token to send queries to Tushare.

Mitigation: Set TUSHARE_TOKEN through an environment variable or secret manager instead of pasting the token into chat-visible JSON.

Risk: Python dependencies are specified with minimum versions rather than pinned lockfile versions.

Mitigation: Pin or lock dependency versions before installation when stronger supply-chain assurance is required.

## Reference(s):

- [Tushare Pro official documentation](https://tushare.pro/document/2)
- [ClawHub skill page](https://clawhub.ai/gaingush/skills/tushare-future-data)

## Skill Output:

**Output Type(s):** [API Calls, JSON data, Guidance]

**Output Format:** [JSON responses with success, data, count, and error fields, plus concise setup and parameter guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided Tushare token through TUSHARE_TOKEN or a call parameter.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
