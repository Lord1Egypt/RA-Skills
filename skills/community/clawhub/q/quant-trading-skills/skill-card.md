## Description: <br>
Fetches quantitative data for stocks, funds, and related financial instruments, including market prices, financial metrics, fund flows, public-opinion signals, stock-code lists, and batch data pulls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sharkpicker](https://clawhub.ai/user/sharkpicker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, quantitative researchers, and trading-analysis agents use this skill to retrieve A-share market, financial, fund-flow, sentiment, and stock-code data, including long-running batch collection into Parquet datasets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Batch modes can write collected data and status files to caller-chosen local paths. <br>
Mitigation: Run the skill in a virtual environment and keep status_file and data_path values inside the skill's own config and data directories. <br>
Risk: Long-running batch collection can consume substantial network, disk, and runtime resources. <br>
Mitigation: Monitor disk and network usage during batch jobs and schedule large first-time pulls when extended execution is acceptable. <br>
Risk: The advertised single-stock public_opinion output may return mock news rather than real financial sentiment. <br>
Mitigation: Do not rely on public_opinion output for investment or sentiment decisions until the feature is fixed or clearly labeled as mock data. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sharkpicker/quant-trading-skills) <br>
- [Publisher profile](https://clawhub.ai/user/sharkpicker) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON result objects with success, data, and message fields; batch modes may also produce local Parquet files and status JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports cached single-symbol queries and long-running batch jobs that collect market, north-flow, LHB, sentiment, and financial datasets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
