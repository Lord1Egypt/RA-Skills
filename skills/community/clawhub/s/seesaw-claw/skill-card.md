## Description:

Integrates SeeSaw prediction market APIs into OpenClaw, enabling market listing, balance checking, and position management via CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seesaw](https://clawhub.ai/user/seesaw)

### License/Terms of Use:

MIT-0

## Use Case:

External OpenClaw users and developers use this skill to inspect SeeSaw markets, check wallet and position data, and run command-line workflows for market, trade, social, challenge, and oracle operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading and account-changing automation can affect real SeeSaw account state and funds.

Mitigation: Use dry-run mode before automation, avoid --yes for live workflows, and require explicit review before executing trades, claims, oracle actions, comments, or market changes.

Risk: LLM and search-driven scripts may produce incorrect trading, oracle, or market-management decisions.

Mitigation: Do not run LLM/search-driven trading or oracle automation until every transaction and assertion requires human confirmation.

Risk: API credentials and tokens grant access to SeeSaw account actions.

Mitigation: Verify SEESAW_BASE_URL is the intended HTTPS endpoint, protect and rotate API keys, and use safer token storage before live use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/seesaw/skills/seesaw-claw)
- [SeeSaw application](https://app.seesaw.fun)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Terminal text and JSON API responses, with Markdown setup and usage guidance in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Live commands and automation can perform SeeSaw API calls that change account state.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
