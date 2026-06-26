## Description: <br>
门店Benchmark分析 compares a target retail store against group, region, province, or city peers to report store tier, ranking movement, and piece-price by attach-rate quadrant position. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gwyang7](https://clawhub.ai/user/gwyang7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Retail analysts, operators, and agents use this skill to benchmark a selected store against comparable stores and summarize relative sales performance, rank changes, tier, top peers, and matrix quadrant placement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill queries sensitive store-performance data through a local database helper. <br>
Mitigation: Review before installing and use only read-only, store-scoped database credentials. <br>
Risk: SQL is built from user-controlled store, scope, and date inputs. <br>
Mitigation: Require parameterized queries or strict validation for store IDs, scope codes, and dates before deployment. <br>
Risk: The code depends on a hardcoded local api_client path. <br>
Mitigation: Replace the local dependency with a packaged or declared dependency before operational use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/gwyang7/retail-store-benchmark-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Text, Markdown, Code] <br>
**Output Format:** [Python dictionary results and formatted text report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Queries store-performance data and returns rankings, tiers, quadrant distribution, and top-store summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact version note) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
