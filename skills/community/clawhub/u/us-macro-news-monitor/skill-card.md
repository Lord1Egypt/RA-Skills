## Description:

Tracks US macro signals from Bloomberg, WSJ, and Reuters and maps potential spillover to Vietnam sectors; used when users ask about US macro news and likely impacts on Vietnamese equities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teahann](https://clawhub.ai/user/teahann)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to monitor recent US macro headlines, classify themes and tone, and map possible spillovers to Vietnam sectors and watchlists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paywalls or blocked media sources can reduce coverage and confidence.

Mitigation: Use the documented official fallback sources and report blocked or missing sources with a lower confidence rating.

Risk: Vietnam equities spillover mapping can be mistaken for investment advice.

Mitigation: Present outputs as monitoring signals and watch items, clearly mark inferred impacts, and avoid absolute buy or sell instructions.

Risk: Macro headlines can become stale quickly.

Mitigation: Include items with explicit publish or update times and state the reporting window in ICT (UTC+7).

## Reference(s):

- [Bloomberg](https://www.bloomberg.com/)
- [The Wall Street Journal](https://www.wsj.com/)
- [Reuters Markets](https://www.reuters.com/markets/)
- [Federal Reserve](https://www.federalreserve.gov/)
- [BLS Releases](https://www.bls.gov/)
- [BEA Releases](https://www.bea.gov/)
- [FRED](https://fred.stlouisfed.org/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown report with source links, theme and tone summaries, Vietnam sector spillover mapping, and watchlist items.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires current web/news access; lowers confidence when fewer than three distinct sources are accessible.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
