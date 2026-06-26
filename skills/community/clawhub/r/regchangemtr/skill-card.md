## Description: <br>
Monitors FCA, PRA, APRA, SEC, and EIOPA regulatory pages for changes, summarising updates and flagging what matters for financial services teams. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quest-commits](https://clawhub.ai/user/quest-commits) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Compliance teams, consultants, fintech builders, and financial-services operators use this skill to scan public regulator pages, summarize significant regulatory updates, and produce daily or on-demand markdown digests with impact ratings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Regulatory digests may be incomplete, stale, or unsuitable as legal advice. <br>
Mitigation: Treat each digest as an early-warning aid and verify important items at the original regulator source before acting. <br>
Risk: Scheduled monitoring and local state updates may be unexpected in some workspaces. <br>
Mitigation: Confirm the daily schedule and the disclosed last-run.md state file before installing or enabling the skill. <br>
Risk: Adding untrusted regulator or publication URLs can expose the agent to unreliable content. <br>
Mitigation: Only add additional monitoring URLs that the user trusts and can validate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/quest-commits/regchangemtr) <br>
- [FCA news](https://www.fca.org.uk/news) <br>
- [Bank of England Prudential Regulation](https://www.bankofengland.co.uk/prudential-regulation) <br>
- [APRA news and publications](https://www.apra.gov.au/news-and-publications) <br>
- [MAS news](https://www.mas.gov.sg/news) <br>
- [SEC what's new](https://www.sec.gov/news/whatsnew) <br>
- [EIOPA publications](https://www.eiopa.europa.eu/publications_en) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Analysis, Files, Guidance] <br>
**Output Format:** [Markdown digest with structured summaries, impact ratings, links, and local state metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates last-run.md to reduce duplicate alerts on later runs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
