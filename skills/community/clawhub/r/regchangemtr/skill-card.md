## Description:

Monitors FCA, PRA, APRA, SEC, and EIOPA regulatory pages for changes. Summarises updates, flags what matters for financial services teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quest-commits](https://clawhub.ai/user/quest-commits)

### License/Terms of Use:

MIT-0

## Use Case:

Financial services compliance teams, consultants, fintech teams, and regulated-industry builders use this skill to scan public regulator pages, summarize significant updates, and produce daily or on-demand markdown digests with impact ratings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Regulator pages, links, or publication formats can change, which may cause missed or misclassified updates.

Mitigation: Review and adjust the listed regulators, source URLs, focus sectors, and alert threshold before deployment and during periodic compliance checks.

Risk: The local last-run.md state file can suppress repeat alerts if its timestamp or counts are stale or incorrect.

Mitigation: Inspect or reset last-run.md when changing the monitoring schedule, after failed runs, or when backfilling older regulatory updates.

Risk: Summaries and impact ratings may be incomplete or unsuitable as final compliance advice.

Mitigation: Route high-impact and deadline-bearing items through qualified compliance or legal review before acting.

## Reference(s):

- [FCA News](https://www.fca.org.uk/news)
- [PRA Prudential Regulation](https://www.bankofengland.co.uk/prudential-regulation)
- [APRA News and Publications](https://www.apra.gov.au/news-and-publications)
- [MAS News](https://www.mas.gov.sg/news)
- [SEC What's New](https://www.sec.gov/news/whatsnew)
- [EIOPA Publications](https://www.eiopa.europa.eu/publications_en)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown daily or on-demand digest with structured summaries, impact ratings, links, and optional local state metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update last-run.md to track the last scan timestamp, item count, and high-impact count.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
