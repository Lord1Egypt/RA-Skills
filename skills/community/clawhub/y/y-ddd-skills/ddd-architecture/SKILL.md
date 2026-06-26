---
name: ddd-architecture
description: DDD 四层架构与包结构规范。适用场景：搭建 DDD 项目骨架、设计包结构、配置 Gradle 多模块依赖、管理分层职责时使用。当用户提到 DDD 分层、四层架构、包结构、依赖规则、项目骨架时使用。
---

# DDD 四层架构

## 职责矩阵

| 层级 | 职责 | 允许 | 禁止 |
|------|------|------|------|
| **用户界面层**（Interfaces） | 协议适配、数据转换、输入校验 | DTO、Controller、Validator | 业务逻辑、事务控制 |
| **应用层**（Application） | 用例编排、事务边界、事件发布 | ApplicationService、Command/Query、DTO | 领域规则、持久化细节 |
| **领域层**（Domain） | 业务逻辑、规则校验、状态管理 | Entity、ValueObject、DomainService、Repository接口、DomainEvent | 依赖Spring、数据库访问、外部API调用 |
| **基础设施层**（Infrastructure） | 技术实现、持久化、消息、外部调用 | RepositoryImpl、MessagePublisher、Config、外部Client | 业务逻辑 |

## 依赖方向（强制规则）

```
Interfaces → Application → Domain ← Infrastructure
```

关键约束：
1. **领域层无任何外部依赖**（纯净 Java/Kotlin）
2. 上层通过接口调用下层，**禁止跨层调用**
3. 基础设施层通过**依赖倒置（DIP）**接入领域层

## 核心原则

- 领域层是**最核心**的一层，不依赖任何外部框架
- 基础设施层是**最外围**的一层，实现领域层定义的接口
- 应用层编排用例，**不含业务判断**
- 用户界面层负责协议转换，**不写业务逻辑**

## 参考资料

- 完整包结构模板：[references/package-structure.md](references/package-structure.md)
- Gradle 多模块依赖配置：[references/gradle-dependencies.md](references/gradle-dependencies.md)
