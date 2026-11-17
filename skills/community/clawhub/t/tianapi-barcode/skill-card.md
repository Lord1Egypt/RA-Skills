## Description:

通过商品条形码查询品牌、规格、厂商、分类等商品基础信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[workxin](https://clawhub.ai/user/workxin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to look up product details from a 13-digit commodity barcode through the TianAPI Barcode service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles a TianAPI credential and may expose a key-bearing image URL in command output.

Mitigation: Use a dedicated limited-quota API key, avoid passing secrets on the command line, do not commit .env files, and treat printed image links as sensitive.

Risk: The security summary reports that the bundled script is syntactically invalid and inconsistent about the expected environment variable name.

Mitigation: Review and fix the script before use, then test API-key loading and barcode lookup with a non-sensitive test key.

## Reference(s):

- [TianAPI Barcode API documentation](https://www.tianapi.com/apiview/138)
- [ClawHub skill page](https://clawhub.ai/workxin/skills/tianapi-barcode)
- [ClawHub publisher profile](https://clawhub.ai/user/workxin)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown guidance with shell commands and product lookup text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a TianAPI Barcode API key; barcode input is expected to be a 13-digit numeric string.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
