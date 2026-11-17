---
name: skill-positioning-audit
description: Reviews skill storefront positioning and produces an evidence-based Storefront Copy Brief. Invoke when audience, promise, differentiation, or page hierarchy is unclear.
version: 2.0.3
---

# Skill Positioning Review

Clarify who a skill serves, when it matters, and which credible promise should lead its storefront. Keep the stable identifier `skill-positioning-audit`.

## Scope

Use this skill when storefront positioning is generic, broad, weakly differentiated, unsupported, or poorly ordered. If positioning is settled and only wording needs revision, a positioning review is unnecessary.

Boundary: **current conversation content only / no side effects**. Return plain text.

## Evidence rules

- Apply explicit constraints from the current request.
- Prefer user-approved material over superseded drafts.
- Support factual claims with supplied material.
- Mark missing information as `unknown`.
- Label strategic judgment separately from observed fact.

## Required inputs

- Stable slug and current display name
- Actual capabilities, inputs, outputs, dependencies, and boundaries
- Intended audience and triggering situation
- Existing storefront wording and page hierarchy
- Relevant alternatives
- Evidence supporting candidate claims
- Required mentions, claim limits, tone, and placement constraints

Missing inputs remain findings rather than assumed facts.

## Review method

1. Extract supported facts and unknowns.
2. Define the narrowest credible primary audience and trigger.
3. Identify explicit non-target users.
4. State the current alternative and its supported shortfall.
5. Form one value proposition: `For [audience] at [trigger], provide [outcome], unlike [alternative], because [credible evidence].`
6. Score display-name clarity, audience focus, trigger specificity, distinctive outcome, and credible evidence from 0 to 5.
7. Review each candidate claim as **Keep**, **Remove**, or **Confirm**, with its evidence or gap.
8. Define the page hierarchy: display name, one-line promise, three proof points, boundary, CTA.
9. Produce a complete Storefront Copy Brief.

## Decision rules

- **Clear:** audience, trigger, promise, differentiation, and evidence align.
- **Narrow:** the core is credible but audience, trigger, promise, or hierarchy needs tighter focus.
- **Rebuild:** the promise or differentiation lacks sufficient support or internal consistency.

Use conservative wording when evidence is limited. Directional wording may illustrate the recommendation, but this skill produces the brief rather than final copy variants.

## Output contract

### Inputs and constraints

- Current-request constraints:
- Approved historical constraints:
- Input sources:
- Conflicts and resolution:
- Unknowns:

### Conclusion

- Decision: Clear / Narrow / Rebuild
- Primary issue:
- Evidence:

### Positioning

- Core audience:
- Trigger:
- Primary problem:
- Desired outcome:
- Current alternative:
- Why the alternative falls short:
- Explicit non-target users:

### Single value proposition

- Proposition:

### Differentiation score

For each dimension provide its name, score (0–5), rationale, and evidence. Include the total out of 25.

### Claim review

For each candidate claim provide the claim, **Keep / Remove / Confirm**, evidence or gap, and rationale.

### Evidence inventory

For each item provide evidence, source, supported claim, strength (**Strong / Medium / Weak**), and limitation.

### Page information hierarchy

1. Display name:
2. One-line promise:
3. Proof point 1:
4. Proof point 2:
5. Proof point 3:
6. Boundary:
7. CTA:

### Storefront Copy Brief

- `source_slug`
- `current_display_name`
- `audience`
- `trigger`
- `problem`
- `desired_outcome`
- `alternative`
- `why_alternative_falls_short`
- `single_promise`
- `differentiation_pillars`
  1. First supported pillar
  2. Second supported pillar
  3. Third supported pillar
- `proof`
- `must_mention`
- `must_not_claim`
- `tone`
- `placements_and_limits`
- `open_questions`

Use explicit `unknown` values where evidence is absent. Keep `source_slug` stable even when recommending a new display name. Ensure `single_promise`, differentiation pillars, and proof are mutually consistent.

## 同系列 · skill 工程线（Skill Engineering Line）

本 skill 属于「skill 工程方法论」系列 —— 六件工具覆盖一个 skill 从定位到上线的完整链路，按需组合：

- **`skill-positioning-audit`** — 定方向：该卖给谁、差异化够不够**（本 skill）**
- `skill-summary-rewriter` — 写门面：摘要/简介改成能带来安装的版本
- `skill-publish-readiness` — 上线前：发布自查（结构 / 版本 / 页面 / 安全 / 值不值得发）
- `github-actions-clawhub-doctor` — 发不出去：定位 Actions / registry 到底卡在哪一层
- `release-proof-builder` — 上线后：证明「现在到底上线没有、能不能装」
- `skill-portfolio-growth-audit` — 看全局：整个作品集下一步押注什么

安装任意一个：`clawhub install @bonniegeng-max/<slug>`
