## Description:

Backtest and deploy trading strategies on Superior Trade's managed cloud.

This skill is ready for commercial/non-commercial use.

## Publisher:

[superior-ai](https://clawhub.ai/user/superior-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading developers use this skill to design, backtest, configure, and deploy Superior Trade strategies against supported exchange workflows. It is intended for agent-assisted trading operations where users review strategy behavior and explicitly confirm live actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required API key can start live trading and move supported funds.

Mitigation: Install only for trusted Superior Trade workflows, keep the key scoped to the intended account where possible, review backtests, and require explicit user confirmation before live trading or deposits.

Risk: An Aerodrome flow may lead an agent to request private keys or seed phrases.

Mitigation: Never provide private keys, seed phrases, or wallet credentials in chat; stop the workflow if those secrets are requested.

Risk: An Aerodrome flow may lead an agent to inspect local developer paths outside the package.

Mitigation: Do not allow inspection of files outside the skill package unless the user separately authorizes the specific files.

## Reference(s):

- [Superior Trade ClawHub skill page](https://clawhub.ai/superior-ai/skills/superior-skills)
- [Superior Trade account and API key page](https://account.superior.trade)
- [Superior Trade API endpoint](https://api.superior.trade)
- [Hyperliquid public info endpoint](https://api.hyperliquid.xyz/info)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown, JSON snippets, Python strategy code, shell commands, and API request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include trading strategy templates, backtest/deployment payloads, safety checklists, and API-call instructions for the user's configured Superior Trade account.]

## Skill Version(s):

4.5.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
