## Description:

用于抖音达人数据、抖音达人信息、账号资料、创作者画像、主页信息和粉丝规模查询。覆盖 Douyin creator profiles，来自社媒数据助手 SocialDataX。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to look up Douyin creator profile details, account basics, creator positioning, and audience scale from a supported creator ID or profile link. It returns available profile facts for the agent to report to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the skill suspicious because it repeatedly invokes an unpinned, changeable CLI package; the scan was partial because two local references could not be resolved.

Mitigation: Wait until the CLI package is pinned to a reviewed version before installing, especially before providing an API key.

## Reference(s):

- [SocialDataX API access and management](https://socialdatax.com/ai?from=clawhub)
- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/socialdatax-douyin-creator-profile)

## Skill Output:

**Output Type(s):** [JSON data, Profile information]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Profile fields vary by response and may include creator name, IDs, bio, verification, audience counts, likes, location, and gender.]

## Skill Version(s):

0.1.25 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
