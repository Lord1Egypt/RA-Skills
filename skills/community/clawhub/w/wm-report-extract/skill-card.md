## Description:

Extracts auditable data and quoted evidence from A-share and Hong Kong IFRS financial-report PDFs, supporting full-report and need-specific extraction with page-level provenance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deadkingyy](https://clawhub.ai/user/deadkingyy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent workflows use this skill to convert financial-report PDFs into auditable extracted tables, field records, narratives, gaps, and review artifacts. It is suited for locating specific facts such as cash balances, shareholders, dividends, or page content, and for producing broader extraction packages for downstream financial analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary PDF URLs.

Mitigation: Use only trusted HTTPS PDF links and run the skill in a sandbox or disposable environment until URL controls are reviewed.

Risk: Cache-clean behavior may delete directories outside the intended cache when given unsafe input.

Mitigation: Avoid attacker-influenced cache IDs or output paths, do not run cache clean on untrusted input, and set the cache directory to a safe disposable location.

Risk: Unpinned dependencies and heavyweight PDF conversion components can change behavior across installs.

Mitigation: Pin dependencies before production use and review the installed environment before processing sensitive reports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/deadkingyy/skills/wm-report-extract)
- [README](README.md)
- [Workflow guide](references/workflow.md)
- [Provenance contract](references/provenance.md)
- [Coverage checklist](references/coverage-checklist.md)
- [Capabilities](references/capabilities.json)
- [WinMale Open Platform](https://open.winmale.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces page-linked extraction artifacts such as manifest.json, quality.json, review.json, tables/*.json, fields/*.json, narratives/*.json, and gaps.json; typed table outputs are intended to be consumed only after quality and review gates pass.]

## Skill Version(s):

0.6.1 (source: frontmatter, CHANGELOG, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
