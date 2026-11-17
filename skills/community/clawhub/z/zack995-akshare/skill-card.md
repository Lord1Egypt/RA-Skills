## Description:

AKShare helps agents fetch and summarize Chinese market and macro-finance data through a local Python environment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zack995](https://clawhub.ai/user/zack995)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to bootstrap AKShare and run focused public-market data queries for Chinese equities, funds, macro indicators, rates, bonds, futures, commodities, and related financial datasets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The query helper can execute arbitrary Python expressions on the user's machine.

Mitigation: Use only trusted expressions, keep prompts and market-data text out of the expression path, and prefer an allowlisted AKShare function dispatcher for higher-risk environments.

Risk: The bootstrap script installs the latest AKShare package without pinned dependency versions.

Mitigation: Review the environment before deployment and pin package versions when reproducibility or change control is required.

## Reference(s):

- [AKShare common recipes](references/common-recipes.md)
- [Publisher homepage](https://github.com/Zack995)
- [ClawHub skill page](https://clawhub.ai/zack995/skills/zack995-akshare)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, Python expressions, and summarized tabular data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return CSV or JSON snippets from AKShare queries, usually truncated to a small number of rows.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
