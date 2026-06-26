---
name: vision-action-evolution-loop
version: 1.0.0
author: KingOfZhao
description: 视觉-动作-进化闭环框架 —— 将感知、规划、执行、评估、进化五阶段融合为自迭代认知循环
tags: [cognition, vision, embodied-ai, vla, closed-loop, self-evolution, robotics, diepre]
license: MIT
homepage: https://github.com/KingOfZhao/AGI_PROJECT
---

# Vision-Action-Evolution Loop Skill

## 元数据

| 字段       | 值                              |
|------------|-------------------------------|
| 名称       | vision-action-evolution-loop   |
| 版本       | 1.0.0                          |
| 作者       | KingOfZhao                     |
| 发布日期   | 2026-03-31                     |
| 置信度     | 96%                            |

## 核心哲学

认知世界的本质是无穷层级的框架节点。本Skill是两个框架碰撞后的涌现节点：

```
diepre-vision-cognition (视觉感知)
        ⊗
self-evolution-cognition (自进化)
        ↓
vision-action-evolution-loop (视觉-动作-进化闭环)
```

## 五阶段闭环（映射 SOUL 五律）

| 阶段 | SOUL 五律 | 技术实现 | 输出 |
|------|----------|---------|------|
| **1. Perceive 感知** | 已知 vs 未知 | 2D视觉检测（OpenCV管道）→ 3D空间理解 | 特征图 + 置信度 |
| **2. Plan 规划** | 四向碰撞 | 多路径碰撞（VLA/2D→3D/工具增强）→ 选最优 | 动作序列 |
| **3. Execute 执行** | 执行不表演 | 机器人臂抓取/折叠/装配 | 物理动作 |
| **4. Evaluate 评估** | 人机闭环 | 质检视觉复检 + 人类确认 | 通过/退回 + 反馈 |
| **5. Evolve 进化** | 文件即记忆 | 更新世界模型 + 调整参数 | 新认知节点 |

## 三阶段桥接架构（非端到端）

```
Stage 1: 2D Detection (已实现)
  手机照片 → 透视矫正 → 二值化 → 线条检测 → SVG/DXF
  [diepre-vision-cognition]

Stage 2: 3D Spatial Understanding (桥接层)
  2D线条 → 参数化3D → 空间坐标映射 → 折叠顺序推理
  [参考文献: arXiv:2412.11892]

Stage 3: Action Planning (动作规划)
  3D模型 → 抓取点计算 → 力控参数 → 动作序列生成
  [参考文献: arXiv:2510.11027, arXiv:2510.17111]
```

## 工具增强策略

不是用VLA端到端替换现有管道，而是将OpenCV管道封装为可调用工具：

```python
# 现有管道封装为工具
tools = {
    "detect_dieline": diepre_vision.analyze,       # 2D检测
    "correct_perspective": opencv.correct_perspective, # 透视矫正
    "generate_dxf": vectorizer.to_dxf,               # 矢量化
    "estimate_3d": spatial_estimator.from_2d,         # 3D估算
    "plan_grasp": grasp_planner.calculate,            # 抓取规划
}
# VLA模型调用这些工具，而非自己做所有事
```

## 学术参考文献

1. **[Vlaser: Synergistic Embodied Reasoning](https://arxiv.org/abs/2510.11027)** — 具身推理VLA模型，动作规划的理论基础
2. **[Efficient VLA Models for Embodied Manipulation](https://arxiv.org/abs/2510.17111)** — VLA高效优化，适合本地部署
3. **[From 2D CAD to 3D Parametric via VLM](https://arxiv.org/abs/2412.11892)** — 2D→3D桥接层的核心技术
4. **[SAGE: Multi-Agent Self-Evolution](https://arxiv.org/abs/2603.15255)** — 四Agent闭环=闭环迭代的学术对应
5. **[Tool-Augmented VLLMs for CAD](https://arxiv.org/) (ICCV 2025)** — 工具增强策略的理论支撑
6. **[Self-evolving Embodied AI](https://arxiv.org/abs/2602.04411)** — 记忆自更新+任务自切换+模型自进化

## 安装命令

```bash
clawhub install vision-action-evolution-loop
# 或手动安装
cp -r skills/vision-action-evolution-loop ~/.openclaw/skills/
```

## 调用方式

```python
from skills.vision_action_evolution_loop import VisionActionEvolutionLoop

loop = VisionActionEvolutionLoop(workspace=".")

# 单次闭环
result = loop.run_cycle(
    image_path="path/to/box_photo.jpg",
    known=["2D检测已验证6/6", "Bobst±0.15mm精度"],
    unknown=["3D折叠顺序", "力控参数优化"]
)

# result 包含五个阶段输出
print(result.perception.confidence)   # 感知置信度
print(result.plan.action_sequence)     # 动作序列
print(result.evolution.new_knowledge)  # 新增认知

# 持续进化（多次迭代）
for i in range(10):
    result = loop.run_cycle(...)
    loop.inject_feedback(result.evolution.feedback)
    # 每次迭代都会更新内部世界模型
```

## 与其他 Skill 的关系

```
self-evolution-cognition (父节点: 自进化框架)
    ├── vision-action-evolution-loop (本Skill: 视觉-动作-进化)
    │       └── diepre-vision-cognition (子节点: 2D视觉检测)
    └── human-ai-closed-loop (兄弟节点: 人机闭环)

arxiv-collision-cognition (交叉引用: 论文碰撞输入)
```
