---
name: ClawHub Skill Launch Review
slug: skill-publish-readiness
description: Reviews ClawHub skills and plugins before release, from a fast launch checklist to deep evidence-based validation. Invoke before publishing or when asked whether a package is ready.
version: 2.0.0
metadata:
  openclaw:
    os: [macos]
    emoji: "🚦"
    requires:
      bins:
        - git
        - clawhub
    homepage: https://github.com/bonniegeng-max/openclaw-publisher
    install:
      - kind: node
        package: clawhub
        bins: [clawhub]
---

# ClawHub Skill Launch Review

在发布前，用同一个入口完成快速上线清单或深度发布审查。它判断的不只是“命令能不能过”，还包括“包是否完整、页面是否可信、风险是否可控、现在是否值得发”。

## 何时调用

- 用户询问 skill 或 plugin 能否发布、还缺什么、是否值得上线
- 用户要求发布前清单、dry-run 前检查、安全审查或深度发布诊断
- 用户提到旧的 `skill-launch-checklist`；直接按本 skill 的 `quick` 模式执行

不用于 Actions/registry 故障排查、发布后安装证明，也不在未获明确确认时执行正式发布。

## 模式：auto + quick/deep

`quick` 与 `deep` 是两种执行模式；`auto` 是默认选择器，不是第三套审查深度。

### auto（默认选择器）

- “快速、清单、最后看一眼、上线前漏项” → `quick`
- plugin、安全、权限、环境变量、版本冲突、差异化、真实失败或完整报告 → `deep`
- 未指定且对象简单、证据有限 → `quick`
- 出现 P0、对象类型不明、证据冲突或 quick 无法可靠结论 → 自动升级 `deep`

输出开头必须写明选择模式、选择原因和是否发生升级。

### quick

以最小读取成本完成上线闸门：验证 `SKILL.md` 与 frontmatter、名称/slug/版本一致性、首屏价值、分类与示例、明显安全问题，以及匹配对象类型的 dry-run 前置项。结论使用 `可以发 / 补完再发 / 先别发`，最多列 3 个关键问题和最小补法。

### deep

在 quick 基础上，完整核对目录、正文、示例、模板、CHANGELOG、`_meta.json`、依赖与环境声明；Plugin 额外核对 package 身份、scope 与 owner；检查凭据、危险默认行为、路径穿越、`*.pyc` / `__pycache__`；区分本地解析、dry-run、Actions、registry、moderation、inspect 与隔离安装证据；输出 P0/P1/P2、证据矩阵、差异化评分和修复后验收。

## 固定工作流

1. **识别对象**：路径、skill/plugin、目标 owner、registry latest；未知项写“未提供”。
2. **选择模式**：遵循 auto 规则，或尊重用户显式指定的 quick/deep。
3. **收集证据**：只把读到或执行到的结果记为事实；推断单独标注。
4. **运行检查**：按模式检查结构、版本、页面、环境、安全与发布动作。
5. **给出结论**：
   - `可以发`：无 P0，关键证据一致
   - `补完再发`：无致命结构问题，但存在发布前应修复项
   - `先别发`：存在 P0、安全风险、身份冲突或证据互相矛盾
6. **生成命令**：
   - Skill：`clawhub skill publish <path> --slug <stable-slug> --name "<Human Readable Name>" --dry-run --owner <owner>`
   - Plugin：先 `clawhub package validate <path>`，再 `clawhub package publish <path> --dry-run`
7. **停止边界**：只到 validation/dry-run；正式发布须再次获得用户明确确认。

## 判定原则

- dry-run 只证明当前输入可被预演，不证明已上架、过审或可安装
- `pending-publication` 不是自动等同失败，需结合 registry/moderation 证据
- 确定性配置错误先修复；仅对明确瞬时错误建议有限退避重试
- 展示名可以变化，slug 必须稳定；所有 Skill 发布命令显式传 `--slug` 与 `--name`
- 发现 package 身份、owner、scope 或版本冲突时不得给“可以发”
- 证据不足时降低置信度，不用猜测补齐结论

## 输出契约

每次输出至少包含：审查对象与实际模式、发布结论与置信度、已验证证据与未验证项、阻塞项或关键漏项、最小修复路径、下一步命令。

deep 模式另含证据矩阵、P0/P1/P2、差异化评分和修复后验收。若定位或文案需要专项处理，先交给 `skill-positioning-audit` 生成 Storefront Copy Brief，再把 brief 交给 `skill-summary-rewriter`。

## 配套文件

- `templates/publish_review_report.md`：auto/quick/deep 统一模板
- `examples/skill_good_release_candidate.md`：quick/deep 输出差异
- `examples/skill_problematic_release_candidate.md`：auto 升级示例
- `examples/plugin_scope_mismatch.md`：Plugin 身份冲突
- `examples/real_publish_failure_review.md`：真实发布链路证据分层
- `references/consistency_rules.md`：一致性与升级规则
- `references/security_review_guide.md`：安全检查
- `references/differentiation_rubric.md`：差异化评分
- `CHANGELOG.md`：版本记录

## 同系列 · skill 工程线（Skill Engineering Line）

本 skill 属于「skill 工程方法论」系列 —— 六件工具覆盖一个 skill 从定位到上线的完整链路，按需组合：

- `skill-positioning-audit` — 定方向：该卖给谁、差异化够不够
- `skill-summary-rewriter` — 写门面：摘要/简介改成能带来安装的版本
- **`skill-publish-readiness`** — 上线前：发布自查（结构 / 版本 / 页面 / 安全 / 值不值得发）**（本 skill）**
- `github-actions-clawhub-doctor` — 发不出去：定位 Actions / registry 到底卡在哪一层
- `release-proof-builder` — 上线后：证明「现在到底上线没有、能不能装」
- `skill-portfolio-growth-audit` — 看全局：整个作品集下一步押注什么

安装任意一个：`clawhub install @bonniegeng-max/<slug>`
