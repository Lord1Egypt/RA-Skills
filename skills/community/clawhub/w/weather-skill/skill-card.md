## Description:

Weather Skill returns current Celsius weather details for a requested city using wttr.in, with SkillPay billing for non-demo calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loverun321](https://clawhub.ai/user/loverun321)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer city weather questions with current temperature and basic conditions. The skill is suited for lightweight weather lookup workflows that accept its third-party billing and weather data dependencies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports a public hardcoded billing API key.

Mitigation: Rotate the exposed key, remove the default key from distributed code, and require the key to be supplied through a deployment secret.

Risk: The skill sends a user identifier to SkillPay and a city or location string to wttr.in.

Mitigation: Use only where this third-party data sharing is acceptable, and disclose the billing and weather-service data flow before use.

Risk: The security review reports external billing and weather requests with limited consent and scoping.

Mitigation: Review the charging behavior before installation and require clear user approval before paid non-demo calls.

## Reference(s):

- [ClawHub Weather Skill page](https://clawhub.ai/loverun321/skills/weather-skill)
- [wttr.in weather service](https://wttr.in)
- [SkillPay](https://skillpay.me)

## Skill Output:

**Output Type(s):** [text, JSON]

**Output Format:** [JSON object with weather, payment, or error fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Successful responses include city, temperature, condition, humidity, wind, and payment status; payment-gated responses may include amount, skill ID, message, and payment URL.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
