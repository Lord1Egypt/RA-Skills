## Description: <br>
Analyzes tender and bid documents to extract key terms, identify risks, estimate win probability, and produce structured bidding recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ylbwjf](https://clawhub.ai/user/ylbwjf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Procurement, sales, legal, and bid teams use this skill to review tender materials, compare requirements, surface contractual and commercial risks, and draft bid-analysis reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tender and bid materials may contain confidential commercial or procurement information. <br>
Mitigation: Use redacted excerpts or approved non-confidential materials, and provide private document URLs only when authorized. <br>
Risk: Bidding strategy guidance can create procurement compliance concerns, especially when based on relationships or preferential treatment. <br>
Mitigation: Treat relationship-based advice as a compliance red flag and route sensitive recommendations through legal, procurement, or compliance review. <br>
Risk: Generated risk ratings, estimates, and win-probability assessments may be incomplete or inaccurate. <br>
Mitigation: Verify outputs against the original tender documents, current rules, and qualified domain review before making bid decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ylbwjf/tender-analyzer-agent) <br>
- [README](README.md) <br>
- [Analyzer prompt template](analyzer-prompt.md) <br>
- [Tender analysis checklist](checklist.md) <br>
- [Sample report](examples/sample-report.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown reports with tables, checklists, risk ratings, and numbered recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include tender risk ratings, cost estimates, win-probability assessment, and bid/no-bid recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
