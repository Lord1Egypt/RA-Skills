---
name: "resume-analyzer"
description: "分析简历内容并提供深度审计报告，包括评分、优缺点分析和改进建议。当用户需要分析简历、获取简历优化建议或进行简历评估时调用。"
---

# 简历分析器

## 功能说明

本技能提供专业的简历分析服务，基于AI模型对简历内容进行深度审计，生成详细的分析报告。

## 分析维度

- **项目经验评分** (0-40分)：评估项目深度、技术复杂度和业务价值
- **技能匹配度** (0-20分)：评估技术栈专业度和与岗位的匹配程度
- **内容完整性** (0-15分)：评估简历信息的完整性和模块顺序合理性
- **结构清晰度** (0-15分)：评估简历结构和格式的清晰度
- **表达专业性** (0-10分)：评估语言表达的专业性和简洁性

## 输入格式

```json
{
  "resumeText": "简历文本内容"
}
```

## 输出格式

```json
{
  "overallScore": 85,
  "scoreDetail": {
    "projectScore": 35,
    "skillMatchScore": 18,
    "contentScore": 12,
    "structureScore": 13,
    "expressionScore": 7
  },
  "summary": "整体简历质量良好，项目经验丰富，但技能描述可进一步优化",
  "strengths": [
    "项目经验丰富，包含多个大型系统开发",
    "技术栈全面，涵盖主流后端技术"
  ],
  "suggestions": [
    {
      "category": "技能",
      "priority": "高",
      "issue": "技能描述过于笼统，缺乏具体技术深度",
      "recommendation": "建议具体描述使用过的技术栈版本和应用场景"
    },
    {
      "category": "项目",
      "priority": "中",
      "issue": "项目描述缺乏量化成果",
      "recommendation": "添加具体的性能优化数据或业务成果指标"
    }
  ]
}
```

## 技术优化基准

在分析简历时，会参考以下高标准场景：

### 高并发与缓存优化
- **多级缓存**：Redis + Caffeine 两级缓存架构，解决击穿/穿透/雪崩，支撑 30w+ QPS
- **原子操作**：Redis Lua 脚本实现分布式令牌桶限流或原子库存扣减

### 异步与性能调优
- **异步编排**：`CompletableFuture` 对多源 RPC 调用编排，RT 从秒级到百毫秒级
- **线程治理**：动态线程池参数监控与调整，解决父子任务线程池隔离导致的死锁问题

### 微服务架构与数据一致性
- **数据同步**：Canal + RabbitMQ/RocketMQ 实现 MySQL 增量数据实时同步至 Elasticsearch
- **分布式事务**：基于消息队列（延时消息）实现订单超时关闭或数据最终一致性
- **网关与安全**：Spring Cloud Gateway + Spring Security OAuth2 + JWT + RBAC 动态权限控制

### 复杂业务建模与设计模式
- **DDD 领域驱动**：抽象领域模型，运用工厂、策略、模板方法模式构建业务链路
- **规则引擎**：责任链模式处理前置校验，组合模式+决策树支撑复杂业务逻辑

## 分析流程

1. **名词纠错**：扫描全文，列出所有不规范的技术名词
2. **深度重写**：从简历中挑选 2-3 条核心项目描述，基于 STAR 法则进行优化重写
3. **方案优化建议**：针对简历中平庸的技术方案，给出更具竞争力的替代方案

## 使用示例

### 输入示例

```json
{
  "resumeText": "张三，Java开发工程师，5年经验，熟悉Spring Boot、MySQL、Redis等技术栈。曾参与电商系统开发，负责订单模块。"
}
```

### 输出示例

```json
{
  "overallScore": 65,
  "scoreDetail": {
    "projectScore": 25,
    "skillMatchScore": 15,
    "contentScore": 10,
    "structureScore": 10,
    "expressionScore": 5
  },
  "summary": "简历基础信息完整，但项目描述过于简单，缺乏技术深度和量化成果",
  "strengths": [
    "具有5年Java开发经验，技术栈基础扎实"
  ],
  "suggestions": [
    {
      "category": "项目",
      "priority": "高",
      "issue": "项目描述过于简单，缺乏具体职责和成果",
      "recommendation": "使用STAR法则描述项目：情境(Situation)、任务(Task)、行动(Action)、结果(Result)，添加具体的技术实现和量化成果"
    },
    {
      "category": "技能",
      "priority": "中",
      "issue": "技能描述过于笼统，缺乏具体版本和应用场景",
      "recommendation": "具体说明使用的Spring Boot版本、Redis应用场景（如缓存策略）等技术细节"
    }
  ]
}
```

## 注意事项

1. 输入的简历文本应尽量完整，包含个人信息、教育背景、工作经验、项目经验和技能等内容
2. 分析结果基于AI模型，仅供参考，最终决策需结合实际情况
3. 对于特别简短的简历，分析深度可能会受到限制