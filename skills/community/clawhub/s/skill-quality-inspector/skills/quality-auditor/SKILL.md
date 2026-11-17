---
name: quality-auditor
description: 技能质量检查：对照组织质量门禁（Q1–Q10/W1–W7）与 superpower 架构规范，逐项核验技能仓库并产出质量报告
source:
  type: original
  repo: skills-repo/skill-quality-inspector
  path: skills/quality-auditor/SKILL.md
  version: "1.0.0"
  updated: "2026-08-14"
metadata:
  category: 技能治理
  platform: 通用
  difficulty: 进阶
---

# 技能质量检查（quality-auditor）

> 把 AI 助手变成一名技能仓库的"质检员"：拿组织规范当尺子，逐条量一个技能仓库是否达标，并给出可执行的整改清单。

## 能力

- **门禁映射**：把 `rules/quality-gates.md` 的 Q1–Q10 / W1–W7 翻译成可勾选的核验项
- **结构核验**：根路由层、references、skills、scripts、assets 五层是否齐全且达标
- **自动化核验**：调用 [scripts/quality_audit.py](../../scripts/quality_audit.py) 跑结构 + 跨文件一致性 + 路由完整性，产出 JSON/MD 报告
- **分级判定**：依据 `rules/superpower-architecture.md` 第 3 节给出 Level A / B / partial / legacy 结论
- **清单输出**：报告按"阻断 / 警告 / 建议"三档归类，直接可用作整改 TODO

## 使用方式

```
/quality-auditor 检查 skills-repo/<repo>
/quality-auditor 对 ai-fullstack-engineer 跑一遍质量门禁
```

## 工作流

1. **确认识别**：锁定目标仓库路径，确认其为 superpower 仓库（根 `SKILL.md` 含 `metadata.architecture: superpower`）。
2. **跑脚本**：`python3 scripts/quality_audit.py --repo <path> --json`，拿到结构化结果（逐检查项 pass/warn/fail）。
3. **人工补检**：脚本管不了的项（Q1 描述是否具体、W6 references 增量性、W2 中文语境）按 [references/quality-dimensions.md](../../references/quality-dimensions.md) 的清单逐条过。
4. **定级**：结构脚本达标分 + 内容门禁结果 → 落 `Level A/B` 或标记 `partial`/`legacy`。
5. **出报告**：用 [assets/quality-report-template.md](../../assets/quality-report-template.md) 套模板，按阻断/警告/建议三档列出，交给仓库负责人整改。

## 适用场景

- 新建技能仓库提交前自检
- 定期巡检组织内所有仓库的健康度
- 合并 PR 前的质量卡点
- 评估某个仓库是否满足发布门槛

## 限制

- 不替仓库负责人拍板"是否发布"——只出报告与证据
- 语义类判断（描述是否足够具体、references 是否真有增量）仍需人工，脚本只能查结构
- 不修改目标仓库文件，只读不改（修复交给 `contradiction-fixer` / `directory-standardizer`）
