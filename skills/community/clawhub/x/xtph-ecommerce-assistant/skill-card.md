## Description:

帮助电商卖家连接店铺、通过图片查找 1688 同款或低价货源，并预览和发布选定商品。

This skill is ready for commercial/non-commercial use.

## Publisher:

[daiyangyang103240](https://clawhub.ai/user/daiyangyang103240)

### License/Terms of Use:

MIT-0

## Use Case:

电商卖家可连接并查看店铺及授权状态，使用图片寻找 1688 货源，并在检查铺货预览后发布选定商品。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local shop session token grants access to a connected seller account.

Mitigation: Install on a trusted machine, protect the local session, and never expose the token in responses.

Risk: Publishing a wrong or unreviewed product can affect a live storefront.

Mitigation: Review selected items and previews before confirmation; use automatic publishing only when explicitly requested and preview-ready.

Risk: Incomplete product attributes or compliance details can prevent safe publishing.

Mitigation: Do not guess missing details or force publication; review blockers and use the provided manual-restock link when needed.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/daiyangyang103240/skills/xtph-ecommerce-assistant)
- [小天铺货](https://puhuo.huitun.com)
- [Agent protocol](references/api-protocol.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise Chinese text and Markdown tables with product links, previews, and publishing results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Shows at most 10 image-search matches in response order; provides browser links when manual action is needed.]

## Skill Version(s):

1.0.16 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
