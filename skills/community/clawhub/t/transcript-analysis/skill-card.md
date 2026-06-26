## Description: <br>
Fetches earnings call transcripts from Stock Analysis or the QVeris API, mines theme signals, and produces evidence, time-series, and summary outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cgxxxxxxxxxxxx](https://clawhub.ai/user/cgxxxxxxxxxxxx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and research teams use this skill to analyze earnings call transcripts across one or more quarters, compare topic signals, and review source-backed excerpts in generated reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled script contains and uses a plaintext QVeris bearer token. <br>
Mitigation: Remove and rotate the embedded token before release; require users to provide their own credential through environment configuration for API mode. <br>
Risk: Transcript requests may send ticker, quarter, and retrieval details to external services. <br>
Mitigation: Document the Stock Analysis and QVeris data flows clearly, and let users choose web mode or API mode before execution. <br>
Risk: Generated transcript analysis can miss context or overstate theme importance when source pages change or transcripts are incomplete. <br>
Mitigation: Review the generated evidence ledger and quoted excerpts before using the summary report for decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cgxxxxxxxxxxxx/transcript-analysis) <br>
- [Stock Analysis](https://stockanalysis.com) <br>
- [QVeris API](https://qveris.ai/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples plus generated CSV and Markdown report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces an evidence ledger CSV, theme time-series CSV, and summary report Markdown for the requested ticker and quarters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
