---
name: api-product
description: API产品项目 - 免费API组合 + 商业产品 + 部署上线
version: 1.0.0
---

# API 产品项目设计编排指南

## 概述

将免费 API 组合成商业产品的开发流程：产品创意 → API集成 → 
应用开发 → 部署上线。适合快速原型和 MVP 开发。

## 工作流程

### 阶段 1: 产品规划

**使用的 Skills**:
- writing-plans
- api-product-planning

**任务**:
- 分析可用免费 API
- 定义产品创意和商业模式
- 规划 API 组合方案

**输出**:
- requirements.md
- docs/product-plan.md
- docs/api-catalog.md

### 阶段 2: 技术方案

**使用的 Skills**:
- writing-plans

**任务**:
- 编写实现计划
- 设计 API 集成架构
- 定义部署策略

**输出**:
- IMPLEMENTATION.md
- docs/technical-design.md
- docs/deployment.md

### 阶段 3: 核心开发

**使用的 Skills**:
- test-driven-development
- subagent-driven-development

**任务**:
- API 客户端封装
- 业务逻辑层
- 数据聚合和转换
- FastAPI 端点

**输出**:
- src/api_clients/
- src/services/
- src/api/
- tests/

### 阶段 4: 集成与部署

**使用的 Skills**:
- requesting-code-review
- enterprise-web-deployment

**任务**:
- 代码安全审计
- HTTPS/反向代理配置
- 部署和监控

**输出**:
- docs/code-review.md
- docs/api-docs.md
- src/config/

## 上下文传递

context:
  writing-plans:
    input: [requirements.md]
    output: [IMPLEMENTATION.md, docs/product-plan.md]
    pass_to: test-driven-development

  test-driven-development:
    input: [IMPLEMENTATION.md, docs/api-catalog.md]
    output: [src/, tests/]
    pass_to: requesting-code-review

  requesting-code-review:
    input: [src/, tests/]
    output: [docs/code-review.md, docs/api-docs.md]

## 质量验证

validation:
  writing-plans:
    required_sections: [overview, implementation, testing]
    format: markdown
    max_length: 15000

  test-driven-development:
    test_coverage: 70
    expected_outputs: [src/, tests/]

  requesting-code-review:
    check_severity: high
    expected_outputs: [docs/code-review.md, docs/api-docs.md]

## 状态管理

state:
  checkpoints:
    - name: product_plan_complete
      after: writing-plans
    - name: core_dev_complete
      after: test-driven-development
    - name: deployment_ready
      after: requesting-code-review

  auto_save: true
  save_interval: 300
