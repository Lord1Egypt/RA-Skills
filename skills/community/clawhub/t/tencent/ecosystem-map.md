# Tencent Ecosystem Map

Use this file to route a request before you recommend tools or workflows.

## Product Families

| Family | Typical User Goal | Primary Surfaces | Route Here When |
|--------|--------------------|------------------|-----------------|
| Corporate and strategy | Understand Tencent as a company, unit, or partner | `tencent.com`, investor and business pages | The request is about ownership, strategy, units, or ecosystem direction |
| Tencent Cloud | Run infrastructure, storage, databases, CDN, security, AI, or media workloads | `cloud.tencent.com`, `tencentcloud.com` | The user needs architecture, operations, migration, or pricing guidance |
| WeChat ecosystem | Reach users through Official Accounts, Mini Programs, or ecosystem integrations | `developers.weixin.qq.com` and related product pages | The request is about WeChat user journeys or developer integration |
| WeCom | Internal collaboration, customer operations, and enterprise messaging | `work.weixin.qq.com` | The request is about enterprise org workflows or admin setup |
| Payments and commerce | Collect money, settle merchant flows, or connect purchase journeys | WeChat Pay and merchant surfaces | The request involves checkout, merchants, settlement, or compliance |
| Ads and growth | Acquire users, buy media, or measure campaign performance | Tencent advertising surfaces | The request is about growth, targeting, creatives, or acquisition operations |
| Games and content | Publishing, live ops, media, or ecosystem partnerships | Tencent game and content programs | The request is about distribution or content operations rather than cloud |

## Fast Routing Questions

Ask the smallest set that removes ambiguity:

1. Is this about cloud infrastructure, customer channels, or corporate strategy?
2. Is the target market mainland China, an international audience, or both?
3. Does the user need planning only, or do they expect account-level execution?
4. Is WeChat, WeCom, or Tencent Cloud the real center of gravity?

## Misroutes To Avoid

- "Tencent" when the real request is Tencent Cloud architecture
- "WeChat" when the task is actually enterprise collaboration in WeCom
- "China payments" when the user only needs product research, not merchant integration
- "Tencent Cloud" when the user only wants market-entry advice

## Output Contract

After routing, state:
- chosen product family
- why it fits
- what it explicitly excludes for this task

If the task spans two families, split the plan into separate sections and owners.
