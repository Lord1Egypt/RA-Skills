## Description:

This skill retrieves real-time precious metal prices for gold, silver, platinum, palladium, and other metals from https://i.jzj9999.com/quoteh5, including bid/ask prices, daily high/low prices, and price trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[108518](https://clawhub.ai/user/108518)

### License/Terms of Use:


## Use Case:

External users, investors, jewelry businesses, collectors, and enterprise users use this skill to query current precious-metal bid/ask prices, daily ranges, and trends for monitoring, pricing, and planning decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Playwright setup may download external package code and a Chromium browser at install time.

Mitigation: Pin Playwright in the consuming project, use a lockfile, inspect dependency changes, and run the skill in a non-privileged environment.

Risk: Automated queries may be affected by source-site rules, rate limits, anti-automation controls, or proxy policy.

Mitigation: Check the source site's rules before frequent queries, use reasonable request intervals, and avoid bypassing access controls.

Risk: Returned prices are reference data for Rongtongjin's own precious-metal business and may be stale or unsuitable for financial decisions.

Mitigation: Present prices as reference-only, include the update time when available, and verify against authoritative sources before trading, purchasing, or pricing decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/108518/skills/skill-goldprice)
- [Rongtongjin Precious-Metal Quote Page](https://i.jzj9999.com/quoteh5)
- [Rongtongjin Website](https://i.jzj9999.com)
- [Playwright Documentation](https://playwright.dev/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples, JavaScript snippets, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces price lookup guidance and example output; live results depend on network access, Playwright/Chromium availability, and the source site's current page structure.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
