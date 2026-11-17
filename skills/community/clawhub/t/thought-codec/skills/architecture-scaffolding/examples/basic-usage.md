# Architecture Scaffolding Example / 架构级脚手架生成示例

## Scenario

A user wants to turn a membership points idea into an engineering-ready design.

用户希望将会员积分想法转化为可进入工程实现的设计。

## Prompt

```text
Use the Architecture Scaffolding Skill.

Goal: Build a membership points system for an online pet supplement store.
Users: Customers, store operators, and support staff.
Rules:
- Customers earn points from purchases, reviews, and referrals.
- Points can be spent on coupons.
- Membership level changes the earning multiplier.
- Operators need to audit point changes.

Output:
- Mermaid architecture diagram
- Domain model
- API contracts
- Implementation scaffold
- Validation checklist
```

## Expected Output Shape

- System summary.
- Assumptions and open questions.
- Architecture diagram.
- Entities such as `Customer`, `PointLedger`, `MembershipLevel`, `Coupon`.
- API contracts for earning, spending, querying, and auditing points.
- Implementation scaffold that separates computation from presentation.

## Review Checks

- Business rules are not mixed with UI rendering.
- Every point change has an audit trail.
- API names reflect domain meaning.
- Open questions are explicit instead of silently invented.
