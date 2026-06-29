## Description: <br>
Generates sector overview and rotation analysis reports when users ask for industry analysis, sector analysis, sector overview, industry rotation, or sector opportunity checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dzy11650](https://clawhub.ai/user/dzy11650) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to produce concise markdown reports comparing sector performance, valuation, ETF flows, leading and lagging stocks, and rotation signals. It is intended for market-analysis workflows that need sourced sector data and high-level allocation guidance without individual stock recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may persist sector-analysis reports in the working directory and create IMA reminder notes when market signals are detected. <br>
Mitigation: Use it only where persistent financial-analysis artifacts are acceptable, and avoid confidential financial queries unless the working directory and reminder notes are approved for that data. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance] <br>
**Output Format:** [Markdown report saved under sector-overview/reports with concise findings and sector allocation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports cite neodata-financial-search as the data source, limit single-sector analysis to 500 Chinese characters and full overviews to 1200 Chinese characters, and avoid individual stock recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact README) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
