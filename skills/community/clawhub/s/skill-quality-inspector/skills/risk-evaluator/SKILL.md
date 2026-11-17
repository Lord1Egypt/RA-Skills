---
name: risk-evaluator
description: 技能风险评估：从安全、维护、合规三维对技能仓库定级（P1/P2/P3），给出处置优先级与 SLA
source:
  type: original
  repo: skills-repo/skill-quality-inspector
  path: skills/risk-evaluator/SKILL.md
  version: "1.0.0"
  updated: "2026-08-14"
metadata:
  category: 技能治理
  platform: 通用
  difficulty: 专家
---

# 技能风险评估（risk-evaluator）

> 把 AI 助手变成一名"风险官"：不只看一个技能写得漂不漂亮，更看它装上之后会不会咬人——安全、维护、合规三个维度的隐患都要算清。

## 能力

- **安全维度**：prompt injection 痕迹、凭据明文、外部内容未设边界、`curl|bash` 式远程脚本、脚本未做权限最小化
- **维护维度**：孤儿文件（references/scripts 未被路由索引）、悬空脚本引用（playbook 调了不存在的脚本）、破坏下游 `skills-lock.json` 的路径改动
- **合规维度**：门禁失配（声明 superpower 却未达标）、frontmatter 缺项、source 字段缺失导致来源不可追溯
- **定级矩阵**：三维 × P1（立即）/ P2（本周）/ P3（排期）三级，输出可排期的处置清单
- **SLA 建议**：按级别给出修复时限与负责人归属

## 使用方式

```
/risk-evaluator 评估 skills-repo/<repo> 的风险
/risk-evaluator 给 security-guardian 做一次安全与维护巡检
```

## 工作流

1. **采集信号**：结合 [scripts/quality_audit.py](../../scripts/quality_audit.py) 与 [scripts/contradiction_scan.py](../../scripts/contradiction_scan.py) 的输出，叠加本技能的安全启发式（扫描 `scripts/*.py` 里的 `os.system`/`subprocess`/`curl`/`eval` 危险调用）。
2. **三维打分**：按 [references/risk-assessment.md](../../references/risk-assessment.md) 的矩阵逐维度判 P1/P2/P3。
3. **出矩阵**：用 [assets/risk-matrix.csv](../../assets/risk-matrix.csv) 作为维度骨架，生成该仓库的风险清单（维度 / 级别 / 证据 / 处置 / SLA）。
4. **排期**：P1 当轮修，P2 进本周，P3 进 backlog；不修的标注 `review_needed`。

## 适用场景

- 发布新仓库前的最后一道安全卡点
- 定期安全巡检（尤其含 `scripts/` 的工程域仓库）
- 接手他人仓库时的健康度摸底

## 限制

- 安全启发式是"可疑信号"而非"定罪"——`subprocess` 调用本身不一定危险，需结合上下文判定
- 不自动修复 P1——只定级与建议，修复动作交由对应仓库负责人或 `contradiction-fixer`
- 外部供应链风险（上游社区技能漏洞）超出本仓库范围，建议结合 skills.sh 三方审计
