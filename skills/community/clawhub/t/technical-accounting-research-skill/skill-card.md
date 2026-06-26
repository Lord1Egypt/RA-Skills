## Description: <br>
Research technical accounting treatment and financial statement disclosure for specific transactions using U.S. GAAP and SEC-focused sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chipmunkrpa](https://clawhub.ai/user/chipmunkrpa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Accounting and finance professionals use this skill to research transaction-specific U.S. GAAP and SEC accounting questions, confirm relevant facts, and prepare memo, email, or Q-and-A documentation. It requires authoritative-source review and a local FinResearchClaw-backed drafting workflow before substantive conclusions are delivered. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an unpinned external FinResearchClaw workflow and dependencies. <br>
Mitigation: Review the FinResearchClaw repository and dependencies, pin a known commit, and run without elevated privileges in an isolated environment. <br>
Risk: Technical accounting work may involve confidential client, company, or transaction facts during web research and document generation. <br>
Mitigation: Redact sensitive facts before research and use a private output folder for sensitive memos instead of the default Downloads path. <br>
Risk: Generated accounting conclusions may be incomplete or misleading if not checked against authoritative sources. <br>
Mitigation: Verify final conclusions against ASC, SEC, AICPA, and clearly labeled interpretive guidance before relying on the deliverable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chipmunkrpa/technical-accounting-research-skill) <br>
- [Clarification Question Bank](references/clarification-question-bank.md) <br>
- [Source Priority and Citation Rules](references/source-priority.md) <br>
- [Report JSON Schema](references/report-json-schema.md) <br>
- [Example Report Payload](references/example_report_input.json) <br>
- [DOCX Report Generator](scripts/build_accounting_report_docx.py) <br>
- [FinResearchClaw Repository](https://github.com/ChipmunkRPA/FinResearchClaw) <br>
- [FASB Accounting Standards Updates](https://www.fasb.org/page/PageContent?pageId=/standards/accounting-standards-updates.html) <br>
- [SEC Financial Reporting Manual](https://www.sec.gov/divisions/corpfin/cffinancialreportingmanual.shtml) <br>
- [PwC Viewpoint](https://viewpoint.pwc.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Clarification questions, sourced accounting analysis, memo/email/Q-and-A prose, JSON payloads, and DOCX files for memo deliverables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Memo-mode output defaults to a DOCX file and requires cited authoritative and interpretive sources with assumptions and open items.] <br>

## Skill Version(s): <br>
0.0.0-auto (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
