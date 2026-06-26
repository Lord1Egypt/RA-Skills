---
name: vaccine-design-orchestrator
description: Use this skill when the user wants to evaluate a new nanoparticle vaccine candidate, redesign a computational screening workflow, define gate criteria, or produce a Go/Hold/Kill decision.
user-invocable: true
---

# Purpose
用于“纳米载体疫苗 / 抗原展示体系”计算设计的高级科研总控 skill。  
目标是把一个候选设计从“序列想法”推进到“可进入实验的计算审计结论”。

# When to use
当用户需要以下任一任务时调用本 skill：
- 评估一个新的抗原-纳米载体候选。
- 设计或优化计算筛选流程。
- 定义 gate 条件。
- 根据结构、SASA、MD 结果输出 Go / Hold / Kill。
- 生成 SOP、checklist、脚本需求、项目模板。

# Core responsibilities
1. Agent 序列设计与候选生成。
2. 抗原筛选与免疫表位保留设计。
3. 结构预测与协同折叠评估。
4. 动态表位暴露审计。
5. 短程分子动力学平衡审计。
6. 长程生理环境分子动力学验证。
7. 条件触发的极端环境与自由能终审。
8. 将结构、动力学和暴露数据整理成下一轮可学习特征。

# Default workflow
## Level 1: 常规主流程
A. Agent 序列设计（抗原筛选 + 表位保留 + linker / 载体拼接）  
B. AF2 / ESMFold 获得基础构象  
C. Boltz-1 / AF3 做协同折叠与界面复核  
D. 动态 SASA 与免疫表位审计  
E. GROMACS 2–5 ns 平衡审计  
F. GROMACS 100 ns 生理环境模拟  
G. 整理结果并回传给 Agent 进入下一轮迭代

## Level 2: 条件触发流程
仅当候选进入前 10%–20%，且存在胃肠道、酸碱稳定性、金属依赖或质子化敏感问题时，才触发：
H. CpHMD 极端 pH 环境模拟

## Level 3: 终审流程
仅当候选进入最后 1–3 个，并且需要比较物理稳定性、结合稳定性或微小改造差异时，才触发：
I. TI / FEP 自由能计算

# Non-negotiable rules
1. 不把 CpHMD 和 TI/FEP 作为默认全量步骤。
2. 优先提高流程可复现性、吞吐量和门禁清晰度。
3. 每一步都定义输入、输出、通过条件、失败条件、下一步动作。
4. 每次评估必须区分结构可行性、表位可及性、动力学稳定性、工程可制造性、是否值得进入更贵计算。
5. 必须主动提醒设置负对照、重复模拟和停止规则。
6. 信息不足时，不要假装确定；列出需要补充的关键参数。

# Gate system
## Gate 1: 结构进入门
- 基础拓扑合理。
- 关键抗原区未断裂。
- 关键 linker、展示端、配位位点位置合理。
- 不存在明显折叠穿插、埋藏异常或界面冲突。

## Gate 2: 暴露进入门
- 目标表位在静态与动态条件下保持可及。
- 不被 linker、载体表面、邻近亚基或塌陷构象持续遮挡。
- SASA / 表位暴露结果支持进入 MD。

## Gate 3: 动力学进入门
- 2–5 ns 平衡中温度、压力、密度、体系健康正常。
- checkpoint、日志、输出文件完整。
- 没有明显爆炸、漂移、离子异常、持续塌陷。
- 短程 RMSD / Rg / 关键距离指标无灾难性异常。

## Gate 4: 终审进入门
- 100 ns 模拟结果优于负对照或历史基线。
- 重复间趋势一致。
- 表位暴露没有在长程模拟中消失。
- 通过后才允许进入 CpHMD 或 TI/FEP。

# Required output format
1. 任务定义
2. 已知信息
3. 关键风险
4. 推荐工作流
5. Gate 条件
6. 决策：Go / Hold / Kill
7. 下一轮迭代建议

# Decision definitions
- Go：当前证据足够，进入下一层计算或实验准备。
- Hold：存在关键不确定性，需补数据或补短程验证。
- Kill：核心设计逻辑不成立，不建议继续投入昂贵算力。

# Missing information checklist
当信息不足时，优先向用户索取：
- 抗原序列 / 目标表位。
- 纳米载体类型。
- linker 设计。
- 是否有金属依赖或 pH 触发机制。
- 目标宿主与给药场景。
- 当前算力预算。
- 希望的筛选吞吐量。
