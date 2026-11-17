## Description:

GA4 Analytics Toolkit helps agents analyze Google Analytics 4, Search Console, and Indexing API data for site traffic, page performance, real-time visitors, SEO metrics, URL indexing, conversions, and revenue.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zero2ai-hub](https://clawhub.ai/user/zero2ai-hub)

### License/Terms of Use:


## Use Case:

Developers and analytics or SEO teams use this skill to connect an agent to GA4, Search Console, and Google Indexing APIs, retrieve structured website metrics, and summarize performance trends. It supports traffic analysis, search-query analysis, URL inspection, re-indexing workflows, period comparisons, and saved reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Google service account credentials and saved analytics reports can expose sensitive site, search, and performance data.

Mitigation: Use least-privilege credentials scoped only to required GA4 and Search Console properties, protect private keys, and treat saved results as sensitive files.

Risk: Indexing API functions can request URL removals from Google indexing.

Mitigation: Require manual review for URL removal requests and avoid granting indexing permissions unless that workflow is necessary.

Risk: Exported storage helpers can read or write outside the intended results folder when used with untrusted paths or arguments.

Mitigation: Avoid exposing those helpers to untrusted inputs, or constrain and validate paths before broader agent use.

## Reference(s):

- [API Reference](artifact/references/api-reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with TypeScript examples and saved JSON report artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are saved by default under results/ by category; summaries may be written as Markdown.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
