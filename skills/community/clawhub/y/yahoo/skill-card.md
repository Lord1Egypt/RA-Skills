## Description:

Use Yahoo Finance for quotes, symbol search, watchlists, market briefs, and catalyst-aware stock decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to resolve Yahoo Finance symbols, fetch quote snapshots, compare watchlists, and frame risk-aware stock decisions without broker order placement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The multi-ticker briefing script can read a user-supplied local file path and send each non-comment line to Yahoo Finance as a quote lookup.

Mitigation: Use --file only with a known watchlist file, preferably under ~/yahoo/, and do not provide .env files, private notes, exports, or other sensitive local files.

Risk: Ticker symbols and search queries leave the user's machine when Yahoo Finance quote or search workflows run.

Mitigation: Use the skill only when sharing those market lookups with Yahoo Finance is acceptable, and avoid including private account or holding details in search text.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/yahoo)
- [Yahoo Finance Quote Pages](https://finance.yahoo.com/quote/{symbol})
- [Yahoo Finance Search Endpoint](https://query1.finance.yahoo.com/v1/finance/search)
- [Command Recipes](commands.md)
- [Market Playbook](market-playbook.md)
- [Risk Playbook](risk-playbook.md)
- [Thesis Card](thesis-card.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown and plain text with inline shell commands and local Python script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use outbound Yahoo Finance requests for ticker symbols or search text; optional local continuity files live under ~/yahoo/ only with user approval.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
