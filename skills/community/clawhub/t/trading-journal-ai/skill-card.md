## Description: <br>
Log every trade with full context (thesis, entry, exit, PnL, emotion, lesson), generate weekly and monthly performance reports, and identify patterns in wins and losses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mars82311111](https://clawhub.ai/user/mars82311111) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading-focused agents use this skill to record trade thesis, entry and exit details, PnL, emotion, and lessons. They can use the journal to produce weekly or monthly reviews that summarize performance patterns and strategy adjustments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading journal entries can contain sensitive trading history, PnL, strategy rationale, signal sources, and emotion labels. <br>
Mitigation: Store the local journal file with appropriate file permissions or encryption, and avoid syncing it to untrusted backups. <br>
Risk: Generated reports or pipeline handoffs could be mistaken for execution-ready trading guidance. <br>
Mitigation: Manually review outputs before using them with trading, backtesting, or exchange-related tools. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown instructions and reports with JSON trade records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores journal data in a local JSON file and summarizes weekly or monthly trading performance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
