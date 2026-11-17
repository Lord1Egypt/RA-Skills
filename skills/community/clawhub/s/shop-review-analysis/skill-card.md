## Description:

跨平台核对实体门店的评价、价格和服务，并提供附有来源的消费建议。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xr-stb](https://clawhub.ai/user/xr-stb)

### License/Terms of Use:

MIT-0

## Use Case:

消费者和提供购物建议的助理可核对具体实体门店的近期评价、预算、菜品及服务，比较门店并判断是否值得到访。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using a logged-in browser session may expose unrelated account information.

Mitigation: Use the session only when explicitly requested for relevant review pages; avoid unrelated sensitive tabs and accounts.

Risk: Incomplete or outdated reviews may lead to misleading dining or purchase recommendations.

Mitigation: Check original source links and review dates, distinguish limited samples from overall ratings, and state coverage gaps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xr-stb/skills/shop-review-analysis)
- [Source repository (server-resolved provenance)](https://github.com/XR-stb/shop-review-analysis)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Text]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes source links, review dates, evidence coverage and comparison tables when relevant.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; bundled skill metadata says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
