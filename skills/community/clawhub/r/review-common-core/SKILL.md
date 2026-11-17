---
name: review-common-core
description: "审稿共享引擎。提供所有审稿 skill 通用的分段标注框架、整体审稿框架、审稿核心原则、事实核查分类、审稿自查清单。不单独运行，由其他审稿 skill 引用其 references/ 目录下的文档。"
---

# 审稿共享引擎

本 skill 提供所有审稿类 skill 通用的基础设施，不单独运行。各审稿 skill 通过引用 `references/` 目录下的文档来复用共享能力。

## 引用方法

在 SKILL.md 中通过相对路径引用：

```markdown
> 共享参考：该框架定义在 review-common-core 共享引擎中。
> 详见 [review-common-core/references/xxx.md](../review-common-core/references/xxx.md)
```

## 目录结构

```
references/
├── review-principles.md              # 审稿核心原则（从19篇审稿中提炼）
├── segment-annotation-framework.md   # 统一的分段标注框架（微观逐句）
├── holistic-review-framework.md      # 整体审稿框架（宏观整体）
├── sensitivity-checklist.md          # 审稿自查清单（隐私/收入/保守偏见）
├── fact-check-framework.md           # 事实核查 6 类风险分类框架
├── dual-host-dialogue-guide.md       # 双人对话稿审稿指南
├── review-checker.md                 # 审稿完成自查清单 + JSON 校验方案（2026-06-16 新增）
└── theme-consistency-checklist.md    # 主题一致性清单 + JSON 校验格式（2026-06-20 新增）

scripts/
├── validate_checklist.py             # JSON 校验脚本（2026-06-16 新增）
└── validate_theme_consistency.py     # 主题一致性 JSON 校验脚本（2026-06-20 新增）
```

## 引用链接速查

| 引用内容 | 文件路径 | 被以下 skill 引用 |
|---------|---------|-----------------|
| 审稿核心原则 | `references/review-principles.md` | review-diagnostics |
| 分段标注框架（🎯😴🔥❓💡⚡💬🎶） | `references/segment-annotation-framework.md` | review-diagnostics |
| 整体审稿框架 | `references/holistic-review-framework.md` | review-diagnostics |
| 主题一致性清单 | `references/theme-consistency-checklist.md` | review-diagnostics |
| 双人对话稿专项指南 | `references/dual-host-dialogue-guide.md` | review-diagnostics |
| 审稿自查清单 | `references/sensitivity-checklist.md` | review-diagnostics |
| 事实核查 6 类风险框架 | `references/fact-check-framework.md` | review-diagnostics |
