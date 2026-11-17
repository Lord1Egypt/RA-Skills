## Description:

Enrich spreadsheet rows by fetching linked sources or APIs to fill missing fields, then aggregate the enriched data into summary sheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kylinr](https://clawhub.ai/user/kylinr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and spreadsheet operators use this skill to fill missing spreadsheet columns from URLs or APIs and produce grouped summary sheets after enrichment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read spreadsheet contents, visit URLs from the sheet, use browser automation, and write results back.

Mitigation: Use it only for intended enrichment workflows and review the source columns, target columns, and proposed batch updates before approving writes.

Risk: Spreadsheet write-back can affect the wrong row or cell if row alignment drifts during batch processing.

Mitigation: Verify adjacent row data before each write, use explicit single-cell ranges, and re-read sheets before aggregation.

Risk: Fetched pages may have ambiguous, missing, blocked, or paywalled data.

Mitigation: Flag ambiguous or unavailable values for manual review instead of guessing, and verify samples before applying reusable extraction patterns.

## Reference(s):

- [Extraction Patterns](artifact/references/extraction-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/kylinr/skills/sheet-data-enrichment)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with spreadsheet update plans, extraction notes, and summary table specifications]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or perform spreadsheet reads, URL fetching, browser-assisted extraction, single-cell write-backs, and summary sheet generation when the user approves the workflow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
