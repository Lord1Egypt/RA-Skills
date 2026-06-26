## Description: <br>
Provides a bounded Tushare Pro wrapper for querying 23 A-share stock data interfaces, including market data, stock metadata, fundamentals, adjustment factors, and trading calendars. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gaingush](https://clawhub.ai/user/gaingush) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, quantitative analysts, and agents use this skill to fetch structured A-share market data and reference data from Tushare Pro by selecting one of the supported API names and providing valid query parameters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tushare token exposure through request JSON, logs, or chat history. <br>
Mitigation: Prefer setting TUSHARE_TOKEN through a protected environment or secret store, and rotate the token if it is exposed. <br>
Risk: Returned market data may be unavailable, delayed, or limited by the caller's Tushare account permissions and points. <br>
Mitigation: Check Tushare account permissions, points, official documentation, and response errors before relying on the data for downstream analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gaingush/tushare-stocks) <br>
- [Tushare Pro official documentation](https://tushare.pro/document/2) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, text, guidance] <br>
**Output Format:** [Structured JSON responses with success flags, data arrays, counts, columns, request metadata, and error messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided Tushare token through request parameters or the TUSHARE_TOKEN environment variable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
