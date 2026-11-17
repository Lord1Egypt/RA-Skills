## Description:

Unified Research Finder helps agents search real academic literature across PubMed and Google Scholar or mirror sources, merge and deduplicate results, and report citations, abstracts, DOI/PMID links, PDFs, and no-result status without fabricating records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[georgechou17](https://clawhub.ai/user/georgechou17)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and research-focused agents use this skill to run PubMed and Google Scholar or mirror searches for academic papers, citations, abstracts, DOI/PMID links, PDFs, and deduplicated cross-database literature reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research queries are sent to PubMed, Google Scholar, and listed Scholar mirror providers.

Mitigation: Use only non-sensitive queries or confirm users are comfortable sending queries to those services before running searches.

Risk: Optional NCBI API keys may be exposed if pasted into chat or command history.

Mitigation: Use a secret manager or a tightly scoped NCBI_API_KEY environment variable, and rotate any key already shared.

Risk: The optional browser fallback may interact with anti-bot or CAPTCHA controls on target sites.

Mitigation: Enable the Playwright/browser fallback only after confirming the target sites permit that access.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/georgechou17/skills/unified-research-finder)
- [PubMed Query Syntax Quick Reference](artifact/references/pubmed-query-syntax.md)
- [NCBI API Key Registration Guide](artifact/references/register-api-key.md)
- [Scholar Sources Technical Reference](artifact/references/scholar-sources.md)
- [NCBI Account Signup](https://account.ncbi.nlm.nih.gov/signup/)
- [NCBI Account Settings](https://www.ncbi.nlm.nih.gov/account/settings/)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown literature summaries with JSON script outputs and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are based on live PubMed and Scholar or mirror responses; no-result and blocked-source cases are reported explicitly.]

## Skill Version(s):

v1.1.1 (source: frontmatter, ClawHub release metadata, CHANGELOG released 2026-07-24)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
