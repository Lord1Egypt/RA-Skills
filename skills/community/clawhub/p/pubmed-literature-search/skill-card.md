## Description:

Chinese-language skill for PubMed clinical literature retrieval and analysis that helps agents build user-confirmed searches, apply JCR quartile and impact-factor filters, rank results, and produce structured literature reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flash9107](https://clawhub.ai/user/flash9107)

### License/Terms of Use:

MIT-0

## Use Case:

Clinical researchers, medical writers, and review teams use this Chinese-language skill to design PubMed searches, confirm search terms, rank clinical literature with JCR quartiles and impact factors, and generate concise literature reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Medical literature-search outputs may be incomplete, outdated, or clinically misinterpreted if used without expert review.

Mitigation: Review medical outputs independently before relying on them, and verify important papers, PMIDs, search terms, date ranges, and JCR data against authoritative sources.

Risk: The workflow expects PubMed/NCBI queries and any JCR Excel file the user provides, so result quality depends on external data availability and user-supplied journal data.

Mitigation: Confirm the search strategy with the user before retrieval and use current, trusted JCR data when applying quartile or impact-factor filters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flash9107/skills/pubmed-literature-search)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown literature-search report with tables and analysis summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include confirmed PubMed search terms, time range, result counts, Top 10 article recommendations, JCR quartile and impact factor fields, research-type distributions, journal distributions, and trend summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
