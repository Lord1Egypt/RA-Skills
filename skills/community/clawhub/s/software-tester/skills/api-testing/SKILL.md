---
name: api-testing
description: REST/GraphQL API 测试：curl/httpie 请求构造、状态码验证、响应检查
source:
  type: derived
  repo: skills-repo/software-tester
  path: skills/api-testing/SKILL.md
  version: 1.0.0
  updated: 2026-07-26
  url: https://skills.sh/briiirussell/cybersecurity-skills/api-audit
metadata:
  category: API 测试
  platform: API
  difficulty: 入门
---

# API 测试与审计

> REST 和 GraphQL API 的测试方法：请求构造、参数校验、鉴权测试、响应验证。

## 能力

- **请求构造**：GET/POST/PUT/DELETE/PATCH 各类请求，自定义 Header/Body/Query
- **参数测试**：边界值、空值、特殊字符、超长输入、类型错误
- **鉴权测试**：无 Token、过期 Token、错误权限、CORS 策略
- **响应验证**：状态码、响应体结构、错误信息格式、响应时间
- **GraphQL**：Query/Mutation 测试、深度限制、字段级权限

## 使用方式

```
/api-testing 测试这个 REST 端点的参数校验
/api-testing 验证这个 API 的鉴权是否正确
/api-testing 对这个 GraphQL 接口做安全测试
```

## 工作流

1. 确定测试端点和 API 文档（OpenAPI/GraphQL Schema）
2. 设计测试矩阵：正常 + 异常 + 边界 + 安全
3. 逐条构造请求并执行
4. 验证状态码和响应体
5. 输出测试报告（通过/失败/风险）

## 适用场景

- API 端点冒烟测试
- 参数校验和安全测试
- 鉴权和权限模型验证
- 新接口上线前检查

## 相关参考（Playbook）

- REST/GraphQL 测试矩阵、示例与鉴权测试清单 → [references/api-testing.md](../../references/api-testing.md)（§测试矩阵四象限、§REST/GraphQL 示例、§鉴权测试清单）
- 契约测试（接口形状与字段级验证，属 API 测试范畴）→ [references/contract-testing.md](../../references/contract-testing.md)（§核心概念、§与 E2E/API 测试关系）
- API 安全深度测试（OWASP API Top 10）→ [references/security-testing.md](../../references/security-testing.md)（§检查清单、§与 API 测试关系）

## 限制

- 不替代专业的 API 测试框架（Postman/Bruno/Supertest）
- 不涉及性能测试和压力测试
- 不涉及 OAuth 复杂鉴权流程