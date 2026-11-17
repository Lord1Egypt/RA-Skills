## Description:

This skill queries hourly weather forecasts from the Shuzhi Weather API for latitude and longitude coordinates using HMAC-SHA256 authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alex098929](https://clawhub.ai/user/alex098929)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer weather questions for cities or coordinates by making authenticated Shuzhi API calls and presenting readable hourly forecast summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores Shuzhi API credentials in a local config file and the security evidence reports that malformed config errors can expose sensitive config contents.

Mitigation: Use a dedicated low-privilege Shuzhi API key, restrict permissions on ~/.openclaw/skills/shuzhi-weather/config.json, and avoid capturing stderr until config values are redacted from errors.

Risk: The security evidence recommends review before installation because credential handling has not been fixed.

Mitigation: Review the credential-handling behavior before installing and use the skill only in environments where the configured Shuzhi API account and outbound API access are appropriate.

## Reference(s):

- [Shuzhi Weather API Documentation](artifact/references/api_response_format.md)
- [Shuzhi Weather API endpoint](https://test-apisix-gateway.shuzhi.shuqinkeji.cn/2033738771717074945)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown guidance with shell commands and structured JSON weather data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided Shuzhi app_key and app_secret in a local config file before API calls can succeed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
