---
name: skill-collision-engine
version: 1.0.0
author: KingOfZhao
description: Skill碰撞引擎 —— 让Skill之间自动四向碰撞生成新Skill的元引擎，Skill工厂的自进化核心
tags: [cognition, meta-skill, skill-factory, collision-reasoning, self-evolution, framework-generation, cross-domain]
license: MIT
homepage: https://github.com/KingOfZhao/AGI_PROJECT
---

# Skill Collision Engine

## 元数据

| 字段       | 值                              |
|------------|-------------------------------|
| 名称       | skill-collision-engine         |
| 版本       | 1.0.0                          |
| 作者       | KingOfZhao                     |
| 发布日期   | 2026-03-31                     |
| 置信度     | 96%                            |

## 核心哲学

> 认知世界的本质是无穷层级的框架节点。
> Skill碰撞引擎让节点之间自动碰撞，产生新的认知节点。
> 这不是简单的Skill组合，是**认知层面的结构化涌现**。

```
Skill A ⊗ Skill B → 四向认知碰撞 → 新 Skill C

self-evolution ⊗ diepre-vision → vision-action-evolution-loop ✓ (已验证)
self-evolution ⊗ arxiv-collision → [待碰撞]
diepre-vision ⊗ diepre-embodied → [待碰撞]
任意 Skill ⊗ 任意外部知识 → [待碰撞]
```

## 三大核心能力

### 1. Skill-Skill 碰撞（认知涌现，非机械组合）

不是简单拼接两个SKILL.md，而是对两个Skill的认知框架做四向碰撞：

```
输入:
  Skill A 的已知集合 FA + 未知集合 VA + 推理框架 RA
  Skill B 的已知集合 FB + 未知集合 VB + 推理框架 RB

碰撞过程:
  正面碰撞: FA ∩ FB 的重叠区域 → 直接可迁移的认知
  反面碰撞: FA 中的已知 是否能解决 VB 中的未知？
  侧面碰撞: RA 和 RB 的非主要特性碰撞 → 隐藏新认知
  整体碰撞: A+B 的研究方向趋势 → 新的框架方向

输出:
  新 Skill C 的已知集合 FC = (FA ∩ FB) ∪ 碰撞新增认知
  新 Skill C 的未知集合 VC = VA ∪ VB - 碰撞已解决
  新 Skill C 的推理框架 RC = RA ⊗ RB 的融合框架
  置信度: 每个认知点独立标注
```

**为什么不是机械组合？**
- 机械组合 = A的SKILL.md + B的SKILL.md 拼接 → 没有新认知
- 认知碰撞 = A和B的已知/未知交集 → 产生A和B都不单独拥有的**涌现认知**
- 关键：涌现认知出现在 FA∩VB 和 FB∩VA 的交叉区域

### 2. SOUL 领域适配（通用框架 → 专用Skill）

SOUL哲学是**通用认知框架**，任何人/任何职业都可以直接使用：

```
通用 SOUL 框架:
  1. 已知 vs 未知    → 每个职业有不同的"已知"和"未知"
  2. 四向碰撞推理    → 推理方法不变，碰撞对象变
  3. 人机闭环        → 每个职业有不同的实践验证方式
  4. 文件即记忆      → 每个职业有不同的记忆类型
  5. 置信度+红线      → 每个职业有不同的红线

适配流程:
  输入: 职业名称 + 该职业的核心知识领域
  输出: 领域专用 Skill（SOUL框架 + 领域已知/未知 + 领域四向碰撞实例）

示例适配:
  程序员 → programmer-cognition（代码审查四向碰撞、bug模式已知/未知）
  医生   → physician-cognition（症状推理四向碰撞、诊断已知/未知）
  教师   → educator-cognition（学情分析四向碰撞、教学效果已知/未知）
  企业家 → entrepreneur-cognition（市场判断四向碰撞、商业模式已知/未知）
  设计师 → designer-cognition（用户研究四向碰撞、设计决策已知/未知）
  科研人员 → researcher-cognition（文献碰撞四向碰撞、假设已知/未知）
```

### 3. 工厂元进化（自改进碰撞质量）

引擎通过验证反馈持续优化自身：

```
进化循环:
  1. 读取所有已发布 Skill 的 VERIFICATION_LOG.md
  2. 分析: 哪些碰撞产生的Skill验证置信度高？哪些低？
  3. 提取: 高置信度碰撞的共同特征（输入类型、碰撞方向权重、领域特征）
  4. 更新碰撞参数:
     - direction_weights = {正面: 0.3, 反面: 0.25, 侧面: 0.2, 整体: 0.25}
     - domain_affinity_map = {包装: [diepre, vision], AI: [evolution, arxiv], ...}
     - threshold_adjustments = 基于历史置信度的动态阈值
  5. 下次碰撞使用优化后的参数
```

## 支持的外部知识源

```
1. ArXiv 论文        → arxiv-collision-cognition（已有）
2. GitHub 仓库/README → 代码能力碰撞
3. Wikipedia 条目     → 基础概念碰撞
4. 网页/PDF           → 通用知识碰撞
5. YouTube/播客文字稿  → 口述知识碰撞
6. 人类对话记录        → 实践知识碰撞（最高价值）
```

## 安装命令

```bash
clawhub install skill-collision-engine
# 或手动安装
cp -r skills/skill-collision-engine ~/.openclaw/skills/
```

## 调用方式

```python
from skills.skill_collision_engine import SkillCollisionEngine

engine = SkillCollisionEngine(workspace=".", skills_dir="./skills")

# 1. Skill-Skill 碰撞
result = engine.collide_skills(
    skill_a="self-evolution-cognition",
    skill_b="diepre-vision-cognition",
    context="包装行业具身智能"
)
print(result.new_skill_name)      # "vision-action-evolution-loop"
print(result.emergent_insights)   # 涌现认知列表
print(result.confidence)          # 0.96

# 2. SOUL 领域适配
profession_skill = engine.adapt_soul(
    profession="程序员",
    domain_knowledge=["代码审查", "bug模式识别", "架构设计"],
    domain_unknown=["生产环境行为", "并发安全"],
    practice_methods=["Code Review", "单元测试", "生产监控"]
)
# 输出: programmer-cognition Skill

# 3. 外部知识碰撞
result = engine.collide_with_external(
    skill="diepre-vision-cognition",
    source_type="arxiv",
    source_id="2410.05340",
    context="VLM生成CAD的技术可行性"
)

# 4. 工厂元进化
engine.self_evolve()  # 读取验证日志，优化碰撞参数
```

## 当前 Skill 碰撞矩阵（已发布6个 Skill）

```
                  self-evo  diepre-vis  human-ai  arxiv  vis-act  embodied
self-evolution       -       ✓(已碰撞)    ×        ×      ×         ×
diepre-vision        ✓          -         ×        ×      ×         ×
human-ai-closed      ×          ×         -        ×      ×         ×
arxiv-collision      ×          ×         ×        -      ×         ×
vis-act-loop         ×          ×         ×        ×      -         ×
diepre-embodied      ×          ×         ×        ×      ×         -

✓ = 已碰撞产生新Skill
× = 待碰撞（潜在新Skill方向）
```

## 学术参考文献

1. **[A Survey of Self-Evolving Agents](https://arxiv.org/abs/2507.21046)** — 自进化Agent综述，元进化的理论基础
2. **[SAGE: Multi-Agent Self-Evolution](https://arxiv.org/abs/2603.15255)** — 多Agent碰撞产生新认知
3. **[Group-Evolving Agents](https://arxiv.org/abs/2602.04837)** — 群体进化+经验共享（←Skill碰撞的经验来源）
4. **[Self-evolving Embodied AI](https://arxiv.org/abs/2602.04411)** — 元进化+自改进循环
5. **[Beyond RAG for Agent Memory](https://arxiv.org/abs/2602.02007)** — 记忆聚合（←碰撞结果的知识存储）
6. **[Memory in the Age of AI Agents](https://arxiv.org/abs/2512.13564)** — 长时序记忆（←进化历史持久化）
