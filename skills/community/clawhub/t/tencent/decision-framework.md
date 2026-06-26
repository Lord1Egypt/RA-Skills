# Tencent Decision Framework

Use this file when the request says "Tencent" but the user has not translated that into a specific operational job.

## Start From the Job, Not the Brand

| User really needs | Likely Tencent surface | Questions to resolve first |
|-------------------|------------------------|----------------------------|
| Run application infrastructure in China or APAC | Tencent Cloud | Region, compliance, workload type, ops model |
| Reach users in a Chinese super-app context | WeChat ecosystem | Mini Program vs Official Account vs service integration |
| Coordinate internal teams and customer messaging | WeCom | Org ownership, admin constraints, external-contact model |
| Collect payments from users | WeChat Pay or partner payment flow | Merchant entity, settlement geography, compliance boundaries |
| Buy ads or growth inventory | Tencent ads surfaces | Campaign market, audience, creative constraints, measurement |
| Compare Tencent against another vendor | Mixed | Decision criteria, market, current stack, lock-in concerns |

## Decision Sequence

1. Clarify the business outcome in one sentence.
2. Name the operating region and compliance boundary.
3. Identify who owns execution rights.
4. Decide whether Tencent is the platform, the channel, or only one option in a comparison.
5. Recommend a single primary path and list rejected alternatives.

## When To Split The Answer

Split the work if the request combines:
- infrastructure plus payments
- WeChat user acquisition plus enterprise collaboration
- mainland launch planning plus international product rollout
- corporate research plus account-level implementation

One blended answer usually hides the real blockers.

## Decision Record Template

```markdown
- Job:
- Region:
- Primary Tencent surface:
- Why this path:
- Rejected paths:
- Required approvals:
- Open blockers:
```
