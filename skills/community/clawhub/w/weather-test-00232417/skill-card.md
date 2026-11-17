## Description:

提供北京、上海等国内主要城市的实时天气查询，支持自然语言输入并返回简洁口语化天气信息。

This skill is for demonstration purposes and not for production usage.

## Publisher:

[panqiang10](https://clawhub.ai/user/panqiang10)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-speaking OpenClaw users can ask for current weather in supported major Chinese cities and receive a concise spoken-style reply. The skill is best suited for testing weather-query interactions because the artifact identifies it as a test version with limited city coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends supported city names to a public weather service.

Mitigation: Disclose network use before installation and confirm that the deployment permits sharing city query terms with the external service.

Risk: The release evidence says the weather request should use HTTPS before production use.

Mitigation: Switch the weather-service request to HTTPS and validate responses before treating the skill as production-ready.

Risk: The release evidence says the skill should declare network permission.

Mitigation: Declare the required network permission in the skill metadata before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/panqiang10/skills/weather-test-00232417)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [JSON response containing a natural-language Chinese reply]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns supported-city weather status, temperature, and wind details when available; otherwise returns a concise fallback message.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
