## Description:

用于小红书博主数据、小红书博主信息、账号资料、达人画像、主页信息和粉丝规模查询。覆盖 Xiaohongshu / XHS / RedNote creator profiles，来自 SocialDataX 社媒数据助手。

This skill is ready for commercial/non-commercial use.

## Publisher:

[devinchen2014](https://clawhub.ai/user/devinchen2014)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can look up Xiaohongshu, XHS, or RedNote creator profile details using a creator ID or profile link. The skill returns available profile fields such as bio and audience counts for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI package is unpinned and may change, creating a supply-chain risk; the scan is incomplete because two referenced local paths were missing.

Mitigation: Review and pin the CLI package to a version you trust before installation, and review the missing referenced files when available.

Risk: Profile lookup inputs are sent to SocialDataX.

Mitigation: Use the skill only with lookup inputs you are comfortable sharing with SocialDataX.

## Reference(s):

- [SocialDataX API access](https://socialdatax.com/ai?from=clawhub)
- [ClawHub skill page](https://clawhub.ai/devinchen2014/skills/socialdatax-xhs-creator-profile)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON profile data with a concise factual summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available profile fields vary by lookup; distinguish returned profile facts from strategic interpretation.]

## Skill Version(s):

0.1.20 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
