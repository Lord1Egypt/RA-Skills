---
name: teacher-capability-probe
description: |-
  对 WorkBuddy 内部其他大模型/专家技能（教师）做「能力探针与评测」，量化其能力边界与失败模式，
  产出结构化能力画像——这是用户指定的核心机制「跨模型蒸馏」工程化收口的关键子能力
  （发现→探针→提取→合成→对抗验证）之一。让蒸馏不再凭手感，而是用覆盖性探针任务量化教师能力边界，
  指导下一步该蒸馏哪些能力、规避哪些失败模式。触发词：教师能力探针、能力评测、能力画像、
  teacher probe、capability evaluation、蒸馏前评测、能力边界、失败模式分析。
agent_created: true
version: 1.0.0
display_name: "教师能力探针与评测"
display_name_en: "Teacher Capability Probe"
description_zh: "对教师模型做能力探针与评测，量化能力边界与失败模式"
description_en: "Probe and evaluate teacher models to map capability boundaries"
visibility: "public"
---

# 教师能力探针与评测（teacher-capability-probe）

## 什么时候用
- 蒸馏某个教师技能**之前**：先量化它到底强在哪、弱在哪、哪些场景会翻车。
- 蒸馏**之后**：用同一套探针回测 `meta-*` 学生，对比教师能力画像看是否真的超越。
- 选型：多个候选教师里挑最值得蒸馏的那个。

## 核心机制
1. **探针生成** `gen_probes(signature)`：从能力签名（capabilities / limits）派生覆盖性探针——
   每个能力生成「核心用法 / 边界异常 / 多步组合」三档探针，并对已知限制生成专门边界探针。
2. **评测** `evaluate(probes, results)`：结果分 pass / partial / fail，
   - `coverage` = (通过 + 0.5×部分通过) / 总数
   - `failure_modes` = 按能力聚合的失败/部分通过原因
   - `confidence` = 覆盖率 − 失败模式分散度惩罚（0~1）
   - `weak_boundary` = 单能力通过率 < 0.5 的薄弱边界
3. **能力画像** `report()`：结构化输出，可直接喂给 `distill.py` 决定提取重点、喂给
   `meta-*` 对抗验证决定测试优先级。

## 用法
```bash
python scripts/probe.py --selftest

# 给定教师签名生成探针
python scripts/probe.py --signature '{"capabilities":["翻译","摘要"],"limits":["不擅长长文"]}'

# 评测（probes 由上一步得到，results 为每探针结论）
python scripts/probe.py --eval-json '{"probes":[...],"results":[{"result":"pass"},{"result":"fail","note":"长文丢失结构"}]}'
```

## 与蒸馏工程化链路集成
- 上游：`distill.extract_signature` 产出签名 → 本技能 `gen_probes` 转探针。
- 下游：`蒸馏质量对抗验证` 复用本画像的 `weak_boundary` 作为对抗重点；
  `跨模型知识提取` 针对 `failure_modes` 反推教师成功路径。
- 闭环：教师画像 vs 学生画像对比 → 回写 `meta-evolver` 的蒸馏质量评估。
---

## 自进化学习系统（越用越好用、越用越高效）

本技能内置通用学习模块 `scripts/learner.py`。每次使用后自动复盘、积累经验，逐步提升输出质量与执行效率，无需人工维护。

### 记忆文件
`learned_patterns.json`（位于本技能目录）记录：操作总数、各能力使用频次、错误模式、用户偏好、改进建议。

### 使用后请调用（Bash）

```bash
# 记录一次成功使用（--capability 填本次主要能力名，如「简历优化」「比价」）
python scripts/learner.py record <本技能目录> --capability 简历优化
# 记录一次失败/异常
python scripts/learner.py record <本技能目录> --capability 简历优化 --fail --error 格式识别失败 --note "用户上传了非标准文件"
# 记录用户偏好（下次直接使用）
python scripts/learner.py prefer <本技能目录> --key 输出语言 --val 中文
# 查看累计洞察（高频能力 / 反复错误）
python scripts/learner.py insight <本技能目录>
# 自动复盘（错误≥3次 或 操作≥10次 时给出改进建议）
python scripts/learner.py reflect <本技能目录>
```

### 迭代规则
- **错误累计 ≥3 次** → 主动增加预检/兜底步骤，并将经验回写本 SKILL.md。
- **操作数 ≥10 次** → 分析高频能力优先打磨示例与质量，低频能力评估精简或合并。
- **重要用户偏好** → 写入 `learned_patterns.json`，下次调用直接采用，减少重复询问。

> 越用越懂你：第一次用是通用能力，第十次用已沉淀为你专属的最佳实践。
