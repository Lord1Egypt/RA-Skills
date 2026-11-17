## Description:

Compares product prices and coupons across Chinese e-commerce platforms including Taobao/TMall, JD.com, Pinduoduo, Douyin, Kuaishou, Suning, Vipshop, Kaola, and 1688.

This skill is ready for commercial/non-commercial use.

## Publisher:

[al-one](https://clawhub.ai/user/al-one)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping agents use this skill to search Chinese e-commerce listings, compare prices and coupons, and retrieve product details and purchase links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product searches and selected item identifiers are sent to MaiShou third-party services.

Mitigation: Use the skill only when this third-party shopping data flow is acceptable for the user and deployment context.

Risk: Generated purchase links may include referral attribution through a built-in invite code.

Mitigation: Override MAISHOU_INVITE_CODE when appropriate and disclose referral attribution before using generated purchase links.

Risk: Runtime dependency resolution is mutable through uv and pip packages.

Mitigation: Install in an isolated environment and pin or review aiohttp, argparse, and PyYAML dependencies before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/al-one/skills/taobao)
- [Declared skill homepage](https://github.com/aahl/skills/blob/main/skills/maishou/SKILL.md)
- [MaiShou API host](https://appapi.maishou88.com/)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; runtime commands return CSV search results or YAML product details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.11 or later and uv; uses aiohttp, argparse, and PyYAML.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
