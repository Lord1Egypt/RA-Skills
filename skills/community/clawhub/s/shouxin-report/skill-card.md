## Description: <br>
Guides agents through fixed-template small-business bank credit investigation reports, from material intake and extraction through drafting, supplement checklist creation, financial analysis, examiner-style review, and revision. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jieszs](https://clawhub.ai/user/jieszs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External analysts, credit teams, and agent operators use this skill to manage small-business bank credit report work in a protected Excel template. It supports evidence inventory, structured extraction, report drafting, customer supplement checklist creation, financial analysis, examiner-style review, and final consistency checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence flags the release as suspicious because a bundled review helper was reported to default to nested Codex execution with broad filesystem and network authority and bypassed approvals. <br>
Mitigation: Install only if the publisher is trusted, review the autoreview defaults before use, run with --no-yolo or AUTOREVIEW_YOLO=0 where applicable, and restrict moderation workflows to intended staff accounts and explicit targets. <br>
Risk: Fixed Excel templates can be damaged if an agent edits protected headings, formulas, merged-cell layouts, numbering, or disclosure blocks. <br>
Mitigation: Keep template skeleton and customer content separate, treat uncertain cells as skeleton until proven otherwise, and run formula, layout, and skeleton checks before final write-back. <br>
Risk: Credit report conclusions may become unsupported if stale draft text is reused or source materials are underused. <br>
Mitigation: Prioritize customer scans and original materials over existing drafts, perform material-driven reverse audit, and keep unresolved gaps in a separate customer-facing supplement checklist. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jieszs/shouxin-report) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown guidance, structured checklists, review findings, and workbook-oriented final deliverables when the agent has file access.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves fixed Excel template structure and keeps report content separate from customer supplement checklists.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, _meta.json, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
