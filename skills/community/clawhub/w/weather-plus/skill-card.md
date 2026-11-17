## Description:

Get current weather, multi-day forecasts, clothing recommendations, and feels-like comfort information for cities worldwide, with optional SkillPay billing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elevo11](https://clawhub.ai/user/elevo11)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to retrieve current weather, short forecasts, feels-like conditions, and clothing guidance for a named city. Deployers can also use its billing command when per-call SkillPay charging is intended.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The billing command can perform real SkillPay charges and defaults to charging unless another mode is selected.

Mitigation: Require explicit user approval before charge or payment-link actions and use the billing command only where per-call billing is intended.

Risk: Credential handling may expose the SkillPay API key if it is passed on the command line or logged by surrounding systems.

Mitigation: Provide SKILLPAY_API_KEY through a protected environment variable and avoid passing API keys as command-line arguments.

## Reference(s):

- [Clothing Index Reference](references/clothing-index.md)
- [wttr.in weather data endpoint](https://wttr.in/{encoded}?format=j1)
- [SkillPay billing API endpoint](https://skillpay.me/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON command output, with Markdown command examples in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Weather commands require a city; forecast accepts up to seven days; billing requires SKILLPAY_API_KEY.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
