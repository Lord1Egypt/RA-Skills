## Description:

查询全国各省份最新汽油及柴油价格。

This skill is ready for commercial/non-commercial use.

## Publisher:

[workxin](https://clawhub.ai/user/workxin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to retrieve current gasoline and diesel prices for Chinese provinces through TianAPI and present the returned fuel-grade prices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TianAPI credentials can be exposed through command-line arguments, copied GET URLs, or committed .env files.

Mitigation: Prefer TIANAPI_OIL_PRICE_KEY, avoid pasting URLs or commands that contain the key, keep scripts/.env out of version control, and use a quota-limited key that can be rotated.

Risk: Province queries and the TianAPI key are sent to a third-party API provider.

Mitigation: Install and use the skill only when sharing those queries and credentials with TianAPI is acceptable.

Risk: The script documents JSON mode but does not define a --json parser argument.

Mitigation: Validate the CLI before depending on JSON output, or patch the script to add the missing --json option.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/workxin/skills/tianapi-oil-price)
- [TianAPI oil price API documentation](https://www.tianapi.com/apiview/104)
- [Publisher profile](https://clawhub.ai/user/workxin)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell commands and oil price results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and TIANAPI_OIL_PRICE_KEY; sends the selected province and API key to TianAPI.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
