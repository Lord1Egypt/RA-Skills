## Description:

Automates Toutiao creator workflows for topic selection, drafting, image handling, and publishing Weitoutiao posts or longer Toutiao articles through browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wtl01](https://clawhub.ai/user/wtl01)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, media operators, and marketing teams can use this skill to prepare and publish Toutiao content with scheduled browser-driven posting. It is intended for users who already control the destination account and can review content, images, and publishing actions before release.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish through an existing logged-in browser session.

Mitigation: Use a dedicated browser profile and a limited Toutiao account, and require manual confirmation before the final publish action.

Risk: Broad trigger phrases and scheduled posting can cause unintended posts.

Mitigation: Review the destination, content, images, schedule, and final publish click for every post or scheduled run.

Risk: Automated image upload and content generation can introduce copyright, platform-policy, or content-quality issues.

Mitigation: Keep uploads in a narrow reviewed folder and manually verify image rights, topic tags, and article text before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wtl01/skills/toutiao-article-publish)
- [Toutiao Weitoutiao publish page](https://mp.toutiao.com/profile_v4/weitoutiao/publish)
- [Toutiao article publish page](https://mp.toutiao.com/profile_v4/graphic/publish)
- [The Paper](https://www.thepaper.cn/)
- [36Kr hot list](https://www.36kr.com/hot-list/catalog)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with browser automation commands and publishing workflow notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include scheduled posting cadence, image path conventions, topic tags, and verification steps for browser-driven publishing.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact package.json reports 4.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
