## Description:

用于小红书博主数据、小红书博主信息、账号资料、达人画像、主页信息和粉丝规模查询。覆盖 Xiaohongshu / XHS / RedNote creator profiles，来自社媒数据助手 SocialDataX。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

Users researching Xiaohongshu / XHS / RedNote creators can look up account basics, creator positioning, and audience scale using a profile URL or user ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the release suspicious because it repeatedly uses an unpinned latest CLI release that can access configured credentials; the assessment is partial.

Mitigation: Before installing, check whether the publisher provides a reviewed, fixed CLI version and decide whether that CLI should have access to configured credentials. Treat the assessment as incomplete because two local references could not be resolved.

## Reference(s):

- [SocialDataX API access and management](https://socialdatax.com/ai?from=clawhub)
- [ClawHub skill release](https://clawhub.ai/devinchen2014/skills/socialdatax-xhs-creator-profile)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured creator profile data in JSON with a concise text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Profile fields are included when available.]

## Skill Version(s):

0.1.21 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
