## Description: <br>
Smart AI router that automatically picks the best and cheapest LLM for each prompt, supports bring-your-own provider keys, tracks costs, and enforces budgets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LdwS123](https://clawhub.ai/user/LdwS123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route LLM prompts through Spendex, compare selected model/provider responses, and inspect account usage, credits, budgets, and savings. It is intended for workflows where cost tracking and provider routing are part of normal agent operation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompt content is routed to Spendex and selected downstream providers. <br>
Mitigation: Use the skill only when Spendex and the selected providers are trusted for the content being sent; avoid secrets, regulated data, private customer content, and confidential code unless approved. <br>
Risk: Provider keys and Spendex account access affect billing and account exposure. <br>
Mitigation: Use scoped provider keys, billing limits, and budget checks where possible, and rotate keys after discontinuing use. <br>


## Reference(s): <br>
- [Spendex AI Router ClawHub Release](https://clawhub.ai/LdwS123/spendex-ai-router) <br>
- [Spendex](https://spendex.ai) <br>
- [Spendex Chat Completions API](https://app.spendexai.com/v1/chat/completions) <br>
- [Spendex Credit Balance API](https://app.spendexai.com/api/credits/balance) <br>
- [Spendex Budgets API](https://app.spendexai.com/api/budgets) <br>
- [Spendex Realtime Usage API](https://app.spendexai.com/api/usage/realtime?stats=true) <br>
- [Spendex Savings Analytics API](https://app.spendexai.com/api/analytics/savings) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SPENDEX_API_KEY plus curl and jq to call Spendex endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
