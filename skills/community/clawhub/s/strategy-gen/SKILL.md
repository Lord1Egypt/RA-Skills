---
name: strategy-gen
description: |
  策略生成助手。给定目标与约束，套用经典框架（SWOT / OODA / 情景规划 / 第一性原理）产出结构化策略画布：现状→选项→取舍→roadmap→度量。当用户需要"帮我制定策略""怎么达成这个目标""做个战略分析""规划下一步"时调用。
agent_created: true
visibility: "public"
---

# 策略生成助手

帮用户把模糊的目标变成可执行、可度量的策略。核心：**先框架后发散，每条策略都带取舍与验证方式**。

## 适用场景
- 业务/产品/个人成长的方向规划
- 在多个选项间做有依据的取舍
- 把"想做的事"拆成带里程碑和度量的 roadmap

## 内置框架
- **SWOT**：优势/劣势/机会/威胁四象限，适合态势盘点
- **OODA**：观察→定位→决策→行动，适合动态对抗环境
- **情景规划**：最好/中性/最坏三档情景 + 触发条件，适合不确定性高
- **第一性原理**：拆到不可再分的事实，从底层重建方案
- **OKR 收口**：每个策略最终落为目标+关键结果+度量

## 标准工作流
使用 `scripts/strategy_framework.py` 生成结构化画布：
```bash
python scripts/strategy_framework.py \
  --goal "3个月内把被动收入做到月入1万" \
  --context "已有电商运营与内容生产能力，每天可投入3小时" \
  --framework swot \
  --output strategy.md
```
- 也支持 `--framework ooda|scenario|first_principles`
- 输出 markdown 画布，可直接进 `decision-review` 做后续复盘

## 质量门禁
- [ ] 策略是否回应了真实约束（而非空泛建议）
- [ ] 是否给出取舍（选 A 意味着放弃 B）
- [ ] 是否带可度量指标与时间点

## 自进化学习系统
```bash
python scripts/learner.py record . --capability "策略生成" [--fail --error <类型> --note <说明>]
python scripts/learner.py insight .
python scripts/learner.py reflect .
```
- 某框架对某类目标反复不适用 → 记录，reflect 建议默认换框架
- 用户偏好的框架 → `prefer` 记录

## 安全边界
- 策略建议仅供参考，重大决策由用户自行判断负责
- 涉及商业敏感信息时结果仅存用户指定位置
