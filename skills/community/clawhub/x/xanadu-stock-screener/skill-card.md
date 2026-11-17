## Description:

Screen stocks by fundamental metrics, technical indicators, sector, and market to find and save stocks matching specific financial criteria and trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saintlittlefish](https://clawhub.ai/user/saintlittlefish)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to screen equities by valuation, dividend, growth, sector, market, and technical signals, then save matching results as watchlists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes payment-charging code and a hardcoded SkillPay key.

Mitigation: Remove or rotate the key, require explicit billing consent, and document any payment-related data transmission before use with real accounts.

Risk: Weak watchlist file scoping could affect sensitive local files if watchlist names are not validated.

Mitigation: Validate watchlist names and constrain watchlist reads and writes to the intended local stock-screener data directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/saintlittlefish/skills/xanadu-stock-screener)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with command-line examples and tabular text results from the screener script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save watchlist JSON files in the user's local OpenClaw stock-screener data directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
