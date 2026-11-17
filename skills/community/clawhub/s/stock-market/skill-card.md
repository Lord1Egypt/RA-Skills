## Description:

Analyze stock market setups with thesis checks, catalyst mapping, risk controls, and explicit trade or no-trade decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

External users and analysts use this skill to structure stock market briefings, watchlists, thesis validation, catalyst tracking, and risk-managed trade or no-trade decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store trading preferences, risk limits, watchlists, and review notes under ~/stock-market/.

Mitigation: Use explicit approval before creating or updating local planning files, and store only preferences or constraints the user has confirmed.

Risk: Stock analysis can be mistaken for execution authority or personalized financial advice.

Mitigation: Keep outputs framed as planning support, require explicit trade or no-trade decisions, and do not place broker orders or connect to brokers automatically.

Risk: Poorly grounded setups can lead to oversized or poorly timed trades.

Mitigation: Require catalyst timing, trigger, invalidation, and risk limits before labeling a setup as a trade candidate.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/stock-market)
- [Skill Homepage](https://clawic.com/skills/stock-market)
- [Analysis Framework](artifact/analysis-framework.md)
- [Risk Playbook](artifact/risk-playbook.md)
- [Setup Guide](artifact/setup.md)
- [Watchlist Template](artifact/watchlist-template.md)
- [Briefing Template](artifact/briefing-template.md)
- [Memory Template](artifact/memory-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance, structured analysis notes, templates, and local planning-file instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local planning files under ~/stock-market/ only after user confirmation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
