## Description:

Queries public Chinese mutual fund rating data from StockStar by fund code or fund name across seven rating institutions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stockstar1996](https://clawhub.ai/user/stockstar1996)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to look up StockStar public fund ratings by six-digit fund code or fund name, then summarize the available institution ratings in Chinese.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may contact fund.stockstar.com and refresh a local ratings cache during lookup.

Mitigation: Run it in a normal least-privilege agent environment and allow network access only when StockStar fund-rating lookups are expected.

Risk: The security guidance notes cache temp-file handling and trigger wording should be tightened before shared writable deployment.

Mitigation: Avoid installing it in a shared writable skill directory until those hardening notes are resolved.

Risk: Fund ratings can be stale, unavailable, or absent for some institutions when upstream pages or cached dates differ.

Mitigation: Present the rating date and unavailable status from the tool output, and do not invent missing ratings.

## Reference(s):

- [StockStar Fund Ratings](https://fund.stockstar.com)
- [ClawHub skill page](https://clawhub.ai/stockstar1996/skills/stockstar-fund-rating)
- [Publisher profile](https://clawhub.ai/user/stockstar1996)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Chinese prose or Markdown table generated from JSON CLI results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initialize or refresh a local fund ratings cache before answering.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
