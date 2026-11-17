## Description:

Sports Inc SportsLink API adapter pulls dealer invoice documents from the SportsWeb Invoice Center, normalizes them for payables workflows, recovers scanned invoice line detail through PDF/OCR review, and marks documents consumed after import.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmtucker](https://clawhub.ai/user/zmtucker)

### License/Terms of Use:

MIT-0

## Use Case:

Accounts payable agents and operators use this skill to retrieve Sports Inc dealer invoices, identify documents that need line recovery, reconcile scanned invoice lines, and pass verified invoices into a payable-matching workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires live SportsLink API keys and may use SportsWeb portal credentials.

Mitigation: Install only for authorized Sports Inc dealer accounts, store secrets in the platform secret broker or protected environment variables, and never pass credentials in chat or command JSON.

Risk: The skill handles financial records and can mark invoice documents historical.

Mitigation: Use dry-run or manual review until the billing workflow is confirmed, and mark documents historical only after the downstream bill has been created successfully.

Risk: Endpoint overrides, persisted browser sessions, downloaded PDFs, and diagnostic captures can expose invoice data if stored loosely.

Mitigation: Keep SPORTSINC_API_URL at the default unless using a verified test endpoint, place SPORTSINC_WEB_STATE_PATH and SPORTSINC_PDF_DIR in private per-user directories, and clean diagnostic captures after use.

## Reference(s):

- [SportsLink API Reference](references/sportslink_api.md)
- [PDF Extraction Guide](references/pdf_extraction.md)
- [SportsWeb Portal Flow Notes](references/sportsweb_flow_notes.md)
- [Sports Inc Homepage](https://www.sportsinc.com)
- [SportsLink API Base URL](https://api.sportsinc.com/)
- [SportsWeb Home](https://swv3.sportsinc.com/home)
- [SportsWeb Invoice Center](https://swv2h.sportsinc.com/)
- [ClawHub Skill Page](https://clawhub.ai/zmtucker/skills/sportsinc-sportslink)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Shell commands, Guidance]

**Output Format:** [JSON objects from helper commands and compact Markdown summaries for delegated tasks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs normalized invoice records, scanned-document recovery status, reconciliation results, and operational next steps.]

## Skill Version(s):

0.7.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
