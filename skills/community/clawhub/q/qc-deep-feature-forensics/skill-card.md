## Description: <br>
Qc Deep Feature Forensics analyzes closed trade orders by reconstructing trades, downloading market history, extracting 12 technical entry features, and comparing winning entries against losing entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tltby12341](https://clawhub.ai/user/tltby12341) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Trading analysts, developers, and quantitative strategy reviewers use this skill to compare the market conditions around winning and losing trade entries, test what-if filters, and produce a feature attribution report from an orders CSV. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading exports and generated analysis files can reveal trading history, P&L patterns, and strategy signals. <br>
Mitigation: Run the skill only on trusted exports in a dedicated working folder, and restrict access to feature_diagnosis.md, generated CSV files, and yfinance_cache contents. <br>
Risk: The first run downloads market data for each ticker, which may expose ticker activity to the data provider and can fail or produce incomplete analysis if network access is unavailable. <br>
Mitigation: Use a controlled network environment for first-time runs, pre-populate the cache for offline use, and review generated diagnostics before relying on conclusions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tltby12341/qc-deep-feature-forensics) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown report, CSV feature matrix, and terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes feature_diagnosis.md, an orders-derived _features.csv file, and a yfinance_cache directory next to the input CSV.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
