## Description:

Research technical accounting treatment and financial statement disclosure for specific transactions using U.S. GAAP and SEC-focused sources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chipmunkrpa](https://clawhub.ai/user/chipmunkrpa)

### License/Terms of Use:

MIT-0

## Use Case:

Accounting and finance teams use this skill to research transaction-specific U.S. GAAP and SEC reporting questions, document assumptions, cite authoritative and interpretive sources, and prepare memo, email, or Q-and-A deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Normal use may clone and run an unpinned external GitHub repository and install local Python dependencies.

Mitigation: Use a pinned, reviewed commit or signed release, install dependencies in a restricted environment, and review the external repository before substantive use.

Risk: The workflow may process confidential accounting or client information while using web research and writing local DOCX files.

Mitigation: Confirm output paths, avoid unnecessary sensitive data in prompts, and run the skill only in an environment approved for the data being analyzed.

Risk: Generated accounting conclusions can be incomplete or misleading if not checked against authoritative standards.

Mitigation: Verify final conclusions against ASC, SEC, AICPA, and clearly labeled interpretive sources before relying on the deliverable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chipmunkrpa/skills/technical-accounting-research-skill)
- [Clarification Question Bank](references/clarification-question-bank.md)
- [Source Priority and Citation Rules](references/source-priority.md)
- [Report JSON Schema](references/report-json-schema.md)
- [Example Report Input](references/example_report_input.json)
- [FinResearchClaw Repository](https://github.com/ChipmunkRPA/FinResearchClaw)
- [FASB Accounting Standards Updates](https://www.fasb.org/page/PageContent?pageId=/standards/accounting-standards-updates.html)
- [SEC Financial Reporting Manual](https://www.sec.gov/divisions/corpfin/cffinancialreportingmanual.shtml)
- [PwC Viewpoint](https://viewpoint.pwc.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance, structured JSON report payloads, shell commands, and generated DOCX report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Memo outputs default to local DOCX files; email and Q-and-A outputs may be returned as concise text.]

## Skill Version(s):

0.0.0-auto (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
