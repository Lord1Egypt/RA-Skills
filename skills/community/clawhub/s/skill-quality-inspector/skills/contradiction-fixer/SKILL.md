---
name: contradiction-fixer
description: 技能矛盾点修复：识别并修复 README/SKILL.md/references 之间的数字不一致、规则冲突、断链与术语不一致
source:
  type: original
  repo: skills-repo/skill-quality-inspector
  path: skills/contradiction-fixer/SKILL.md
  version: "1.0.0"
  updated: "2026-08-14"
metadata:
  category: 技能治理
  platform: 通用
  difficulty: 进阶
---

# 技能矛盾点修复（contradiction-fixer）

> 把 AI 助手变成一名"对账员"：专门揪出一个技能仓库内部自相矛盾的地方——数字对不上、规则打架、链接断了、术语飘了。

## 能力

- **数字对账**：README/SKILL.md 声称的"N 个子技能 / M 篇 references"与实际目录数是否一致
- **断链检测**：markdown 里指向 `references/` `scripts/` `assets/` 的相对链接是否落到真实文件
- **重复标题**：同一文件内重复出现的标题（往往是复制粘贴残留或隐形冲突）
- **术语不一致**：同一概念在库内写法漂移（如"Level A"与"A 级"混用、"路由表"与"能力索引"混称）
- **规则冲突**：两篇 references 对同一事项的口径相反（如一处说"必须"另一处说"可选"）

## 使用方式

```
/contradiction-fixer 修复 skills-repo/<repo> 的矛盾点
/contradiction-fixer 扫描 career-coach 的断链与数字不一致
```

## 工作流

1. **扫描**：`python3 scripts/contradiction_scan.py --repo <path> --json`，得到断链 / 重复标题 / 数字矛盾 / 术语漂移四类 findings。
2. **定性**：参照 [references/contradiction-detection.md](../../references/contradiction-detection.md) 的矛盾类型学，给每条 finding 定严重度（阻断 / 警告）。
3. **优先修阻断项**：数字对账失败、断链、规则冲突先修——它们会直接误导 Agent 路由。
4. **术语统一**：选一个规范写法，全库替换；在根 `SKILL.md` 或 AGENTS.md 固定术语表，防止复发。
5. **回归**：修完重跑脚本，确认 findings 归零（或仅剩可接受的建议项）。

## 适用场景

- 仓库多人协作后出现的"改了 README 没改 SKILL.md"类漂移
- 大规模改写 README 后安装命令 / 清单表丢失（D32 实证陷阱）
- 合并多个 references 后出现的口径冲突

## 限制

- 语义级"规则冲突"需要 Agent 读懂两篇文档才可能发现，脚本只能标记可疑信号
- 不擅自删除内容——数字/术语矛盾优先"让文案成真"（补齐产物）而非改小口径糊弄
- 修复后必须重跑门禁，确认没引入新的路由孤儿
