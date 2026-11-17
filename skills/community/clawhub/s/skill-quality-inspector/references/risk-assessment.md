# 风险评估矩阵（risk-assessment）

> 质量合格 ≠ 风险可控。本篇给出技能仓库的三维风险模型与 P1/P2/P3 定级，把"装上之后会不会咬人"算清楚。

## 一、三维风险

| 维度 | 关注点 | 典型信号 |
|------|--------|----------|
| **安全** | 装上后能否危害用户机器/凭据/数据 | prompt injection 痕迹、`os.system`/`subprocess` 危险调用、明文凭据、`curl\|bash` 远程脚本、外部内容未设边界 |
| **维护** | 仓库自身是否会悄悄烂掉 | 孤儿文件（未被路由索引）、悬空脚本引用（playbook 调不存在的脚本）、破坏 `skills-lock.json` 的路径改动 |
| **合规** | 是否守住组织规范底线 | 声明 superpower 未达标、frontmatter 缺项、`source` 缺失致来源不可追溯、registry 账实不符 |

## 二、三级定级

| 级别 | 定义 | 处置 SLA |
|------|------|----------|
| **P1 立即** | 会直接误导 Agent 路由或危害安全/数据 | 当轮修复，未修不发布 |
| **P2 本周** | 质量隐患明显但不阻断使用 | 进入本周 TODO |
| **P3 排期** | 轻微或不确定的改进项 | 进 backlog，定期复查 |

## 三、定级矩阵（维度 × 级别 触发示例）

| 维度 \ 级别 | P1 | P2 | P3 |
|-------------|----|----|----|
| 安全 | 脚本含未加边界的 `eval`/远程拉取执行 | 外部内容未提示"视为不可信" | 依赖未版本钉扎 |
| 维护 | 悬空脚本引用导致 playbook 指令不可执行 | 孤儿 reference 不可达 | 路由关键词不够具体 |
| 合规 | 声明 superpower 但 partial/legacy | frontmatter 缺 `metadata` | `source.updated` 超 180 天未标 `review_needed` |

## 四、处置流程

```
1. 信号采集：quality_audit.py + contradiction_scan.py 输出 + 安全启发式扫描 scripts/*.py
2. 三维打分：逐维度对照上表判 P1/P2/P3（安全启发式只给"可疑信号"，是否定罪需结合上下文）
3. 出矩阵：以 assets/risk-matrix.csv 为骨架，生成 维度/级别/证据/处置/SLA 清单
4. 排期：P1 当轮修、P2 本周、P3 backlog；不修的标 review_needed
5. 复盘：修复后重跑门禁，确认 P1 清零
```

## 五、典型坑

- **把"可疑"当"定罪"**：`subprocess` 调用本身不危险，需看它执行了什么；误报同样算 bug。
- **只看内容不看供应链**：外部社区技能漏洞超出本仓范围，需结合 skills.sh 三方审计（Gen Agent Trust Hub / Socket / Snyk）。
- **P1 自动修复诱惑**：风险评估只定级与建议，修复动作交仓库负责人或 `contradiction-fixer`，避免在巡检里越权改文件。

## 相关子技能与层次边界（L2→L3）

- [skills/risk-evaluator/SKILL.md](../skills/risk-evaluator/SKILL.md) — 本篇的执行落地层：本篇给"三维风险 + 三级定级 + 定级矩阵 + 处置流程 + 坑"，子技能给一次完整风险评估的执行步骤与矩阵产出（见其「工作流」与「限制」）。
- 边界：**定级标准归本篇，采信号与出矩阵归子技能**。安全启发式只给"可疑信号"，是否定罪需按本篇第五节结合上下文判断，误报同样算 bug。
- 处置联动：定级后的实际修复交 [skills/contradiction-fixer/SKILL.md](../skills/contradiction-fixer/SKILL.md)（内容矛盾类）或仓库负责人；本层严格保持"只定级、不改文件"的只读边界。
