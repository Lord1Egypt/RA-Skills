---
name: review-diagnostics
description: "文稿审稿诊断工具集。提供事实核查、读者模拟、结构分析、传播力评估和反AI味检测等审稿技法。Use when: (1) 需要对文章/播客稿/视频脚本进行深度审稿 (2) 发现某段读起来不顺/走神/假/有AI味 (3) 用户要求逐句审稿、事实核查、结构评估。Not for: 语法检查、文字校对、帮写文章。"
---

# Review Diagnostics

文稿审稿的"工具箱"skill。不定义完整流程（流程在 AGENTS.md），只提供可组合的诊断技法。

## 什么时候读什么

| 要查什么 | 读这个文件 |
|---------|-----------|
| 事实正确性（6类风险 + 素材对照） | `references/fact-check.md` |
| 逐句读者反应模拟 | `references/reader-sim.md` |
| 结构/人性洞察/传播力/反AI味 | `references/structural-review.md` |
| 特定技法（解释腔/拧巴否定/绝对化降级等） | `references/techniques.md` |
| 双人对话稿专项 | `references/dual-host-dialogue.md` |

## 快速使用

```markdown
# 在审稿时按需读对应的 reference 文件
# 输出用统一模板：

## 📌 硬伤（必须改）
| 位置 | 原文 | 问题 | 建议 |
## ✍️ 风格偏离（建议改）
## 🔧 润色建议（可选）
```

## 脚本工具

审稿前后各跑一次以下脚本，确保每个环节都产生了分析产物：

| 顺序 | 脚本 | 作用 |
|------|------|------|
| 审稿前 | `python3 scripts/init_checklist.py <article-name> <version>` | 生成 checklist.json，标记所有待检项为未完成 |
| 审稿中 | （按 AGENTS.md 流程逐 stage 执行） | 完成一项就把 checklist.json 中对应项设为 True |
| 审稿后 | `python3 scripts/validate_pipeline.py docs/reviews/<article-name>/ [project-dir]` | 验证 review.md 中是否有每个阶段的标记，输出完整性报告 |

### 示例

```bash
# 开始审稿前
python3 scripts/init_checklist.py llm-wiki-todo v2

# 审稿完成后
python3 scripts/validate_pipeline.py docs/reviews/llm-wiki-todo docs/projects/llm-wiki-todo
```

### 输出格式约束

本 skill 的所有 reference 文件定义的输出格式，均被 `validate_pipeline.py` 的 stage markers 检查所覆盖。
如果 review.md 缺少某个阶段的分析产物标记，脚本会报 FAIL。

## 与其他 skill 的关系

- **gpt-review** — ChatGPT 副审。本 skill 审完后调用，交叉比对。
- **common-core** — 共享引用库（分段标注体系、自查清单等）。
