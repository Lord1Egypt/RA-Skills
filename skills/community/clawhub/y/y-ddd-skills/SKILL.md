---
name: Y-DDD-SKILLS
description: DDD 领域驱动设计完整技能套件。适用场景：当用户提到 DDD 领域驱动设计、或需要全面覆盖新项目开发、老项目重构、架构规范、战术设计、代码审查等多个维度时使用此总入口 Skill。该 Skill 会引导用户根据具体场景选择对应的专业 Skill。
---

# DDD 领域驱动设计（DDD）技能套件

本套件提供 DDD 领域驱动设计的完整指导，覆盖从概念理解到落地实施的各个阶段。

## 技能组合概览

```
ddd-master（总入口）
├── ddd-core-concepts      核心概念
├── ddd-architecture       架构规范
├── ddd-tactical-design     战术设计
├── ddd-new-project         新项目
├── ddd-refactoring         老项目重构
└── ddd-code-review         代码审查
```

## 场景与技能映射

| 场景 | 推荐技能 | 优先级 |
|------|---------|--------|
| 理解 DDD 核心概念，建立领域模型基础 | `ddd-core-concepts` | 始终优先 |
| 设计项目四层架构和包结构 | `ddd-architecture` | 始终优先 |
| 实现实体、值对象、聚合等战术模式 | `ddd-tactical-design` | 始终优先 |
| 从零开始搭建 DDD 新项目 | `ddd-new-project` | 新项目 |
| 老项目向 DDD 改造 | `ddd-refactoring` | 重构 |
| 审查 DDD 代码质量 | `ddd-code-review` | 审查 |

## 推荐使用路径

### 新项目开发

```
ddd-core-concepts → ddd-architecture → ddd-tactical-design → ddd-new-project
```

### 老项目重构

```
ddd-core-concepts → ddd-architecture → ddd-refactoring → ddd-code-review
```

### 代码审查

```
ddd-code-review（直接使用，检查清单配合反模式诊断树）
```

## 核心原则速查

1. **领域优先**：先理解业务，持久化是细节
2. **边界清晰**：限界上下文独立演进，防腐层隔离外部
3. **富模型**：业务逻辑封装在领域对象内，而非散落在 Service

## 各技能入口

按需激活对应的专业 Skill：

- `ddd-core-concepts`：理解领域优先 / 边界清晰 / 富模型三大原则，建立通用语言和限界上下文
- `ddd-architecture`：设计四层架构（Interfaces / Application / Domain / Infrastructure），配置 Gradle 多模块依赖
- `ddd-tactical-design`：实现实体（Entity）、值对象（Value Object）、聚合（Aggregate）、仓储（Repository）、领域事件（Domain Event）
- `ddd-new-project`：从事件风暴开始，经过限界上下文划分、领域建模、骨架生成到编码审查的完整流程
- `ddd-refactoring`：遗留系统分析、Strangler Fig 增量迁移、五类重构模式（贫血模型、跨聚合引用、万能聚合等）
- `ddd-code-review`：设计阶段 / 编码阶段 / 提交审查三阶段检查清单及五大反模式诊断树

## 代码示例语言

本套件所有代码示例以 **Java/Kotlin + Spring/JPA** 生态为主。
