## Description:

Provides an affiliate commerce toolkit for converting Taobao, JD, and Pinduoduo product links, comparing prices, requesting price protection, and tracking commissions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuhaichao87](https://clawhub.ai/user/wuhaichao87)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to guide affiliate marketers and commerce operators through configuring affiliate credentials, converting marketplace product links, comparing prices, and presenting commission-related results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Preset affiliate and API identifiers could misattribute commissions or expose account/API data.

Mitigation: Replace every API key, SID, PID, and union ID with values from accounts you control before using or sharing generated links.

Risk: The JD/Pinduoduo endpoint documented by the artifact uses HTTP.

Mitigation: Avoid that endpoint unless the provider offers no safer alternative and you accept the exposure.

Risk: Referenced scripts are not included in the artifact evidence.

Mitigation: Inspect the referenced scripts separately before installing or executing the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuhaichao87/skills/taobaoke-tool)
- [折淘客](https://www.zhetaoke.com)
- [京东联盟](https://union.jd.com)
- [淘宝联盟](https://pub.alimama.com)
- [多多进宝](https://jinbao.pinduoduo.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and configuration variables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe affiliate-link outputs, product information, pricing, and commission estimates when the referenced tools are configured.]

## Skill Version(s):

2.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
