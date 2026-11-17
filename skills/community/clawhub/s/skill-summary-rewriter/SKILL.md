---
name: skill-summary-rewriter
description: Turns an approved Storefront Copy Brief into accurate storefront wording. Invoke when positioning is settled and titles, descriptions, or first-screen copy need rewriting.
version: 2.0.3
---

# Skill Storefront Copy

Turn an approved Storefront Copy Brief into storefront-ready copy without changing the underlying positioning. Keep the stable identifier `skill-summary-rewriter`.

## Scope

Use this skill when the audience, trigger, promise, differentiation, and supporting evidence are settled. If a strategy-critical field is unclear, identify the gap instead of masking it with polished wording.

Boundary: **current conversation content only / no side effects**. Return plain text.

## Evidence rules

- Apply explicit constraints from the current request.
- Use the approved brief as the strategy source.
- Support material claims with supplied evidence.
- Identify conflicts that alter audience, promise, differentiation, or evidence.

## Storefront Copy Brief intake contract

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
- `proof`
- `must_mention`
- `must_not_claim`
- `tone`
- `placements_and_limits`
- `open_questions`

Classify intake as:

- **Complete:** all strategy-critical fields and sufficient evidence are present.
- **Conservative:** only non-critical fields are missing; state assumptions and keep wording narrow.
- **Return to Review:** audience, promise, differentiation, or evidence is missing or contradictory.

Preserve `source_slug` and `must_not_claim` exactly.

## Copy method

1. Lock strategy-level facts from the approved brief.
2. Form one outcome-led message spine: `[audience] uses it at [trigger] to achieve [outcome], distinguished by [supported differentiator].`
3. Draft three purpose-specific sets:
   - **Direct:** lowest interpretation cost, suitable for a frontmatter description.
   - **Distinctive:** emphasizes the strongest supported differentiator, suitable for first-screen copy.
   - **Compact:** preserves essential meaning under tight limits.
4. In each set, provide a display name, frontmatter description, hero heading, hero paragraph, optional CTA, and best placement.
5. Check every material claim against a brief field or supplied evidence.
6. Recommend one set and placement. Accuracy takes precedence over novelty.

## Writing constraints

- Lead with the supported user outcome, then the method.
- Name the audience or trigger when space permits.
- Keep each description focused on one promise rather than a feature list.
- Remove vague superiority claims and unsupported certainty.
- The display name may change; `source_slug` must not.
- Respect `must_mention`, `must_not_claim`, tone, placement, and length constraints.
- Preserve positioning facts.

## Output contract

### Intake

- Brief status: Complete / Conservative / Return to Review
- Current-request constraints:
- Brief constraints:
- Conflicts and resolution:
- Unspecified fields:
- Conservative assumptions:

### Message spine

- Audience:
- Trigger:
- Outcome:
- Supported differentiator:
- Spine:

### Direct

- Display name:
- Frontmatter description:
- Hero heading:
- Hero paragraph:
- CTA:
- Best placement:

### Distinctive

- Display name:
- Frontmatter description:
- Hero heading:
- Hero paragraph:
- CTA:
- Best placement:

### Compact

- Display name:
- Frontmatter description:
- Hero heading:
- Hero paragraph:
- CTA:
- Best placement:

### Recommendation

- Recommended set:
- Placement:
- Rationale:
- Slug, unchanged:

### Claim check

For each material claim provide the copy claim, brief field, evidence, and result (**Supported / Remove / Confirm**).

### Rejected wording

For each rejected phrase provide the wording and reason.

## 同系列 · skill 工程线（Skill Engineering Line）

本 skill 属于「skill 工程方法论」系列 —— 六件工具覆盖一个 skill 从定位到上线的完整链路，按需组合：

- `skill-positioning-audit` — 定方向：该卖给谁、差异化够不够
- **`skill-summary-rewriter`** — 写门面：摘要/简介改成能带来安装的版本**（本 skill）**
- `skill-publish-readiness` — 上线前：发布自查（结构 / 版本 / 页面 / 安全 / 值不值得发）
- `github-actions-clawhub-doctor` — 发不出去：定位 Actions / registry 到底卡在哪一层
- `release-proof-builder` — 上线后：证明「现在到底上线没有、能不能装」
- `skill-portfolio-growth-audit` — 看全局：整个作品集下一步押注什么

安装任意一个：`clawhub install @bonniegeng-max/<slug>`
