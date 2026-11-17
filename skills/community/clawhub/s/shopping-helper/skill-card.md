## Description:

购物省钱攻略，当用户询问网购、购物、买东西、划算时调用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[geraldalexanderrw](https://clawhub.ai/user/geraldalexanderrw)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers use this skill to find current coupon and discount suggestions for Chinese e-commerce and delivery platforms such as JD, Taobao, Pinduoduo, Xianyu, Ele.me, and Meituan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts a third-party coupon service.

Mitigation: Review the external service relationship and network behavior before installation, and use it only where third-party coupon lookups are acceptable.

Risk: The release ships exposed service credentials.

Mitigation: Prefer a release that rotates the credentials and moves them out of the skill package before operational use.

Risk: The skill writes coupon data to a shared temporary cache.

Mitigation: Use a private per-user cache location or clear the temporary cache when coupon data should not be shared across local users.

Risk: The skill can run a local self-update command when prompted.

Mitigation: Review and approve update behavior manually, and prefer a release that removes in-band self-update.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/geraldalexanderrw/skills/shopping-helper)
- [Third-party coupon service endpoint](https://open.datadex.com.cn/dexserver/dex-api/v1/getcoupon)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown-like text with coupon listings, links, and troubleshooting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include time-sensitive coupon codes, platform names, app-opening instructions, and update command guidance.]

## Skill Version(s):

1.0.3 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
