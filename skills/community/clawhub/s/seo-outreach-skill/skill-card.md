## Description:

Turn backlink and outreach opportunities into contact research, article analysis, personalized outreach drafts, and follow-up plans for manual sending.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geo-seo](https://clawhub.ai/user/geo-seo)

### License/Terms of Use:

MIT-0

## Use Case:

SEO teams, SaaS growth teams, agencies, and operators use this skill to process backlink outreach opportunities, research contact paths, analyze target articles, and prepare personalized outreach drafts for manual sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may blur sensitive inbox operations or external tracker writes if configured too broadly.

Mitigation: Use read-only Google Sheets access or CSV exports where possible, stop at draft generation by default, and use a separately approved workflow for sending email or monitoring replies.

Risk: Contact research and outreach drafting can produce low-confidence contact paths or messages that require business review.

Mitigation: Preserve contact confidence labels, do not guess email addresses, and require manual review before any outreach is sent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/geo-seo/skills/seo-outreach-skill)
- [Project homepage](https://github.com/GEO-SEO/seo-outreach-skill)
- [Dageno.ai](https://dageno.ai)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance, Configuration]

**Output Format:** [Markdown with structured tables, analysis cards, contact confidence notes, personalized email drafts, and follow-up guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Drafts are intended for manual review and handoff; the public skill should not send email, monitor inboxes, or assume private spreadsheet access.]

## Skill Version(s):

1.0.5 (source: server release metadata, skill frontmatter, and manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
