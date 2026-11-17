## Description:

Connect to Shelter financial data so an agent can check safe-to-spend, predict cash crunches, find subscriptions, simulate purchases, provide coaching, and ask Guardian AI about money using read-only access to bank-derived insights via Plaid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[code-with-brian](https://clawhub.ai/user/code-with-brian)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an agent answer personal-finance questions from Shelter account insights, including cash-flow status, forecasts, alerts, savings opportunities, affordability checks, and coaching. The skill is read-only and requires a Shelter API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API key or confidential financial insights could be exposed if requests are sent to an unintended endpoint.

Mitigation: Keep SHELTER_API_URL unset unless deliberately using a trusted HTTPS Shelter endpoint, treat API responses and /v1/ask prompts as confidential financial data, and rotate the Shelter API key if it may have been sent to an unexpected endpoint.

Risk: Install instructions can create supply-chain risk if the user installs a package identity other than the one they intend to trust.

Mitigation: Install only from the intended package identity and verify the npm package name before using the README command.

## Reference(s):

- [Shelter homepage](https://shelter.money)
- [Agent API Data Model Reference](references/DATA_MODEL.md)
- [ClawHub skill page](https://clawhub.ai/code-with-brian/skills/shelter)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API response interpretation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses SHELTER_API_KEY and optional SHELTER_API_URL; API responses contain financial insights and should be treated as confidential.]

## Skill Version(s):

1.0.3 (source: server release metadata, package.json, clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
