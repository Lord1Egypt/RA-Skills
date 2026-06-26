---
name: web-fullstack
description: Web全栈项目 - React前端 + FastAPI后端 + PostgreSQL
version: 1.0.0
---

# Web 全栈项目设计编排指南

## 概述

全栈 Web 应用开发流程，前端 React + TypeScript，后端 FastAPI + PostgreSQL，
使用 skill 编排系统进行系统化开发。

## 工作流程

### 阶段 1: 需求与设计

**使用的 Skills**:
- writing-plans

**任务**:
- 收集用户需求
- 编写用户故事
- 定义数据模型和 API 接口

**输出**:
- requirements.md
- user-stories.md
- docs/api-spec.md

### 阶段 2: 技术方案

**使用的 Skills**:
- writing-plans

**任务**:
- 编写实现计划
- 制定技术架构
- 定义测试策略

**输出**:
- IMPLEMENTATION.md
- docs/technical-design.md
- docs/test-plan.md

### 阶段 3: 后端开发

**使用的 Skills**:
- test-driven-development
- subagent-driven-development

**任务**:
- 定义数据库模型（SQLAlchemy）
- 实现 REST API 端点
- 编写后端单元测试和集成测试

**输出**:
- src/backend/models/
- src/backend/api/
- src/backend/services/
- tests/backend/

### 阶段 4: 前端开发

**使用的 Skills**:
- test-driven-development
- subagent-driven-development

**任务**:
- 搭建 React 项目
- 实现页面组件
- API 集成和状态管理

**输出**:
- src/frontend/components/
- src/frontend/pages/
- src/frontend/api/
- tests/frontend/

### 阶段 5: 集成与验证

**使用的 Skills**:
- requesting-code-review

**任务**:
- 代码安全扫描
- E2E 测试
- 生成文档

**输出**:
- docs/code-review.md
- docs/api-docs.md
- tests/e2e/

## 上下文传递

context:
  writing-plans:
    input: [requirements.md]
    output: [IMPLEMENTATION.md, docs/api-spec.md]
    pass_to: test-driven-development

  test-driven-development:
    input: [IMPLEMENTATION.md, docs/api-spec.md]
    output: [src/backend/, src/frontend/, tests/]
    pass_to: requesting-code-review

  requesting-code-review:
    input: [src/, tests/]
    output: [docs/code-review.md]

## 质量验证

validation:
  writing-plans:
    required_sections: [overview, implementation, testing]
    format: markdown
    max_length: 15000

  test-driven-development:
    test_coverage: 80
    expected_outputs: [src/backend/, src/frontend/, tests/]

  requesting-code-review:
    check_severity: high
    expected_outputs: [docs/code-review.md, docs/api-docs.md]

## 状态管理

state:
  checkpoints:
    - name: design_complete
      after: writing-plans
    - name: backend_complete
      after: test-driven-development
    - name: frontend_complete
      after: test-driven-development
    - name: code_reviewed
      after: requesting-code-review

  auto_save: true
  save_interval: 300
