## Description: <br>
Scans public news, announcements, regulatory information, and financial signals for named companies, then produces structured credit-risk sentiment reports with risk levels, factors, alerts, and recommended actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yukirang](https://clawhub.ai/user/yukirang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and business teams use this skill to batch-review company watchlists for public sentiment and credit risk, especially when they need structured JSON reports, high-risk alerts, and follow-up review cadence suggestions. Outputs should be treated as draft research and verified against source material before business, credit, compliance, or investment decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The executable helper can produce low-risk reports without fetched news evidence. <br>
Mitigation: Treat generated reports as draft research, require fetched source evidence for real assessments, and verify source URLs before using the output. <br>
Risk: Outputs may be used for credit, compliance, investment, or other high-impact business decisions. <br>
Mitigation: Do not rely on the skill as a formal credit rating; route material decisions through qualified financial, legal, or compliance review. <br>
Risk: Scheduled scans and report sharing can include outdated watchlists or unintended Feishu destinations. <br>
Mitigation: Review watchlists before scheduled scans and confirm sharing destinations before publishing reports. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yukirang/risk-sentiment-scanner) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, markdown, files, guidance] <br>
**Output Format:** [Structured JSON reports, markdown summaries, and chat guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save dated risk reports and produce high-risk alert summaries; reports should retain source URLs when fetched evidence is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
