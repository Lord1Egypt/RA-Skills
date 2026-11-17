## Description:

Smart AI router - automatically picks the best and cheapest LLM for every prompt, supports bring-your-own-key provider routing, tracks costs, and enforces budgets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ldws123](https://clawhub.ai/user/ldws123)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route LLM chat-completion requests through Spendex, inspect credit balance and budgets, and review usage or cost-savings data for their connected providers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and conversation history may be sent to Spendex and routed to connected model providers.

Mitigation: Use only after reviewing Spendex data handling and provider-routing controls; avoid secrets, credentials, private source code, regulated data, and confidential conversations.

Risk: The example curl payload substitutes user prompt text directly into JSON.

Mitigation: Rewrite the command to JSON-encode prompt text safely before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ldws123/skills/spendex-ai-router)
- [Spendex](https://spendex.ai)
- [Spendex Chat Completions API](https://app.spendexai.com/v1/chat/completions)
- [Spendex Credit Balance API](https://app.spendexai.com/api/credits/balance)
- [Spendex Budgets API](https://app.spendexai.com/api/budgets)
- [Spendex Usage API](https://app.spendexai.com/api/usage/realtime?stats=true)
- [Spendex Savings Analytics API](https://app.spendexai.com/api/analytics/savings)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SPENDEX_API_KEY plus curl and jq; routes user prompts and conversation history through an external Spendex API.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
