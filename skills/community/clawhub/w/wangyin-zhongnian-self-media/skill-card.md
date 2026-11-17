## Description:

A WeChat public-account workflow for the single account "网瘾中年", covering topic screening, writing, style cleanup, AIGC compliance checks, cover generation, draft publishing, and data review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shun1989](https://clawhub.ai/user/shun1989)

### License/Terms of Use:

MIT-0

## Use Case:

External creators or operators of the "网瘾中年" WeChat account use this skill to plan, draft, check, package, and push account-specific WeChat articles. It is scoped to that account and excludes other social platforms, pure coding tasks, and video publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The draft-publishing path runs unpinned external tooling and an unreviewed local publisher script.

Mitigation: Use only in a controlled environment for the named WeChat account, replace npx -y bun with a pinned or preinstalled verified Bun executable, and audit the external baoyu-post-to-wechat publisher and credential handling before allowing draft pushes.

Risk: The skill can perform external draft-publishing writes when the user requests a WeChat draft push.

Mitigation: Require an explicit same-turn user confirmation before pushing to the draft box and stop rather than retrying through alternate channels when publishing errors occur.

## Reference(s):

- [AIGC compliance redlines](references/compliance-redlines.md)
- [Data-driven conclusions](references/data-conclusions.md)
- [WeChat writing standards](references/writing-standards.md)
- [ClawHub skill page](https://clawhub.ai/shun1989/skills/wangyin-zhongnian-self-media)
- [Artifact repository link](https://github.com/Shun1989/wangyin-zhongnian-self-media)
- [Referenced self-media workflow](https://github.com/yanhua1010/self-media-content-workflow)
- [Volcengine ARK API endpoint](https://ark.cn-beijing.volces.com/api/v3)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown articles, review notes, draft-publishing commands, cover-image paths, and data-review updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require user confirmation before external draft-publishing writes.]

## Skill Version(s):

1.1.0 (source: server release evidence, target metadata, skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
