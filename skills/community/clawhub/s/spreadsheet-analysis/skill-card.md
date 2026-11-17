## Description:

Analyzes, answers questions about, and compares XLSX and CSV spreadsheets through a hosted service, with verifiable worksheet-row evidence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[youteacher](https://clawhub.ai/user/youteacher)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to summarize spreadsheet data, ask questions, compare files, and trace findings back to worksheet rows. Parsed cell text is sent to the AI Skills platform for analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Extracted spreadsheet cell text, filenames, and row locations are sent to the hosted platform.

Mitigation: Use only on spreadsheets authorized for this disclosure; avoid confidential data without authorization.

Risk: A configured API key may also be used by related platform skills.

Mitigation: Protect the key and restrict access to its configuration.

Risk: Analysis may misstate spreadsheet findings or cite the wrong row.

Mitigation: Verify important findings and citations against the source worksheet rows.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/youteacher/skills/spreadsheet-analysis)
- [AI Skills platform](https://ai-skills.open-idea.net)
- [API key configuration](https://ai-skills.open-idea.net/skill-docs/spreadsheet-analysis/API-KEY.md)
- [Local spreadsheet extraction](https://ai-skills.open-idea.net/skill-docs/spreadsheet-analysis/LOCAL-EXTRACTION.md)
- [HTTP requests and task polling](https://ai-skills.open-idea.net/skill-docs/spreadsheet-analysis/HTTP-REQUESTS.md)
- [Spreadsheet operations](https://ai-skills.open-idea.net/skill-docs/spreadsheet-analysis/OPERATIONS.md)
- [Evidence and safety rules](https://ai-skills.open-idea.net/skill-docs/spreadsheet-analysis/BEHAVIOR-RULES.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Text or Markdown analysis; optional Markdown and JSON export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite verifiable worksheet rows; exports are available on request.]

## Skill Version(s):

1.2.0 (source: ClawHub release and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
