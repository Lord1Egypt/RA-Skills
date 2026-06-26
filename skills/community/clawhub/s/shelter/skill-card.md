## Description: <br>
Connect to Shelter financial data to check safe-to-spend, forecast cash flow, find subscriptions, simulate purchases, get coaching, and ask Guardian AI about money using read-only access to bank data via Plaid. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[code-with-brian](https://clawhub.ai/user/code-with-brian) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to let an agent query Shelter's read-only financial API, interpret account-derived insights, and provide personal finance summaries, forecasts, alerts, affordability checks, and coaching. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Shelter API key grants access to read-only financial insights and could expose sensitive account-derived information if leaked. <br>
Mitigation: Keep SHELTER_API_KEY private, avoid committing or sharing it, use scoped keys, and revoke or rotate keys if exposure is suspected. <br>
Risk: Returned financial summaries, forecasts, and coaching can contain sensitive personal finance information. <br>
Mitigation: Use the skill only with trusted agents and avoid sending unnecessary full-context or free-form financial questions when a structured endpoint can answer the request. <br>
Risk: Financial guidance may be incomplete or misleading if account data is stale, low confidence, or outside the API's computed insight scope. <br>
Mitigation: Surface low-confidence results, prefer structured endpoints, and treat agent output as informational guidance rather than a final financial decision. <br>


## Reference(s): <br>
- [Shelter homepage](https://shelter.money) <br>
- [Agent API Data Model Reference](references/DATA_MODEL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown or plain text summaries with optional curl commands and JSON response interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SHELTER_API_KEY; responses may include sensitive financial insights and should use structured endpoints before free-form questions.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata, package.json, clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
