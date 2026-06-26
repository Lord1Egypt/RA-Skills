## Description: <br>
Report Generator helps users turn natural-language weekly work updates into structured, professional weekly reports with role-specific sections, issue analysis, and next-week plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wscats](https://clawhub.ai/user/wscats) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, team leads, and business operators use this skill to draft concise weekly reports from their role, completed work, blockers, metrics, and next-week priorities. It is especially useful for engineering, sales, marketing, HR, operations, finance, project status, and management reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may paste confidential company information, personal data, customer identifiers, financial details, source code, credentials, or unreleased business plans into an AI service while preparing a report. <br>
Mitigation: Use only AI services approved by the user's organization and remove or anonymize sensitive details before sharing work updates with the model. <br>
Risk: Generated reports may omit context, overstate progress, or frame issues incorrectly when the user's input is incomplete. <br>
Mitigation: Review and edit the generated report before sending it, and add missing metrics, owners, dates, and business context where needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wscats/smart-weekly-report) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact Skill Definition](artifact/SKILL.md) <br>
- [Artifact Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown reports and follow-up editing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompt-only skill that produces role-specific weekly report drafts and can revise tone, detail, or structure based on user feedback.] <br>

## Skill Version(s): <br>
1.1.3 (source: server release evidence and CHANGELOG, released 2026-05-02) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
