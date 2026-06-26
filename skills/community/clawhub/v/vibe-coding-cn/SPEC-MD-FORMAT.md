# SPEC.md 格式指南

**基于 ClawHub Spec 技能调研总结**

---

## 📋 SPEC.md 标准结构

### GitHub Spec-Kit 格式

```markdown
# Project Name - Specification

## 1. Overview（项目概述）

### 1.1 Problem Statement（问题陈述）
清晰描述要解决的问题

### 1.2 Goals（目标）
- 主要目标
- 次要目标

### 1.3 Non-Goals（非目标）
- 明确不包含的内容

---

## 2. Requirements（需求）

### 2.1 Functional Requirements（功能需求）
| ID | 需求描述 | 优先级 | 验收标准 |
|----|---------|--------|---------|
| FR-001 | 用户可以登录 | P0 | 能成功登录 |
| FR-002 | 用户可以登出 | P0 | 能成功登出 |

### 2.2 Non-Functional Requirements（非功能需求）
- 性能要求
- 安全要求
- 可扩展性要求

---

## 3. Design（设计）

### 3.1 Architecture（架构）
```
┌─────────┐
│  Frontend │
├─────────┤
│  Backend  │
├─────────┤
│  Database │
└─────────┘
```

### 3.2 Data Model（数据模型）
```typescript
interface User {
  id: string;
  name: string;
  email: string;
}
```

### 3.3 API Design（API 设计）
| Endpoint | Method | Description |
|----------|--------|-------------|
| /api/login | POST | 用户登录 |
| /api/logout | POST | 用户登出 |

---

## 4. Implementation Plan（实现计划）

### 4.1 Phase 1: 基础功能
- [ ] 用户认证
- [ ] 数据模型

### 4.2 Phase 2: 核心功能
- [ ] 主要业务逻辑
- [ ] API 实现

### 4.3 Phase 3: 测试与优化
- [ ] 单元测试
- [ ] 性能优化

---

## 5. Testing Strategy（测试策略）

### 5.1 Unit Tests（单元测试）
- 测试覆盖率目标：80%

### 5.2 Integration Tests（集成测试）
- API 测试
- 数据库测试

### 5.3 E2E Tests（端到端测试）
- 关键用户流程

---

## 6. Deployment（部署）

### 6.1 Environment（环境）
- Development
- Staging
- Production

### 6.2 CI/CD Pipeline
- 自动化测试
- 自动化部署

---

## 7. Approval（审批）

- [ ] Product Owner 审批
- [ ] Tech Lead 审批
- [ ] 团队审批

**审批日期**: YYYY-MM-DD

---

## 8. Changelog（变更日志）

| 版本 | 日期 | 变更内容 | 作者 |
|------|------|---------|------|
| v1.0 | 2026-04-06 | 初始版本 | Author |
```

---

## 🎯 Spec-First Development 格式

**Spec-First Development 技能使用的简化格式**：

```markdown
# SPEC.md

## 1. Context（背景）
- 当前问题
- 为什么需要这个功能

## 2. Goals（目标）
- 具体目标列表
- 成功标准

## 3. Approach（方法）
- 技术方案
- 架构决策

## 4. Implementation Details（实现细节）
### 4.1 File Structure
```
src/
  ├── components/
  ├── services/
  └── utils/
```

### 4.2 Key Functions
- `function1()`: 说明
- `function2()`: 说明

## 5. Testing（测试）
- 测试计划
- 验收标准

## 6. Approval
- [ ] 用户确认（说"go"继续）
```

---

## 📊 Spec Miner 提取的 SPEC 格式

**从代码逆向提取的 SPEC 格式**：

```markdown
# Extracted Specification

## 1. System Overview
- 从代码分析的系统架构
- 主要组件和依赖

## 2. Features（功能清单）
### 2.1 Authentication
- 登录功能（auth/login.js）
- 登出功能（auth/logout.js）
- 注册功能（auth/register.js）

### 2.2 Data Management
- CRUD 操作（services/data.js）
- 数据验证（validators/*.js）

## 3. API Endpoints
| Endpoint | Method | Handler |
|----------|--------|---------|
| /api/users | GET | usersController.getAll |
| /api/users/:id | GET | usersController.getById |

## 4. Data Models
```typescript
interface User {
  id: string;
  name: string;
  // 从代码推断的字段
}
```

## 5. Dependencies
- express: ^4.18.0
- mongoose: ^7.0.0

## 6. Missing Features（可能缺失的功能）
- ⚠️ 未找到错误处理
- ⚠️ 未找到日志记录
```

---

## 🎯 Vibe Coding v4.0 推荐格式

**结合各家所长的推荐格式**：

```markdown
# {项目名} - Specification

**版本**: v1.0  
**日期**: 2026-04-06  
**状态**: Draft / Approved / Implemented

---

## 1. Overview（概述）

### 1.1 Problem（问题）
用 1-2 句话描述要解决的问题

### 1.2 Goals（目标）
- **主要目标**: 最重要的目标
- **次要目标**: 其他目标

### 1.3 Non-Goals（非目标）
明确不包含的内容，避免范围蔓延

---

## 2. Requirements（需求）

### 2.1 User Stories（用户故事）
| ID | 作为... | 我想要... | 以便... | 优先级 |
|----|--------|---------|--------|--------|
| US-001 | 用户 | 登录系统 | 访问个人数据 | P0 |
| US-002 | 用户 | 修改密码 | 保证账户安全 | P1 |

### 2.2 Functional Requirements（功能需求）
| ID | 需求描述 | 验收标准 | 优先级 |
|----|---------|---------|--------|
| FR-001 | 用户登录 | Given 正确凭证，When 点击登录，Then 成功登录 | P0 |
| FR-002 | 密码验证 | Given 错误密码，When 尝试登录，Then 显示错误 | P0 |

### 2.3 Non-Functional Requirements（非功能需求）
- **性能**: 页面加载 < 2 秒
- **安全**: 密码加密存储
- **可用性**: 99.9% uptime

---

## 3. Design（设计）

### 3.1 Architecture（架构）
```
┌─────────────┐
│   Frontend   │
│  (React)    │
├─────────────┤
│   Backend    │
│  (Node.js)  │
├─────────────┤
│   Database   │
│  (MongoDB)  │
└─────────────┘
```

### 3.2 Data Model（数据模型）
```typescript
interface User {
  id: string;        // 唯一标识
  email: string;     // 邮箱
  password: string;  // 加密密码
  createdAt: Date;   // 创建时间
}
```

### 3.3 API Design（API 设计）
| Endpoint | Method | Request | Response |
|----------|--------|---------|----------|
| /api/login | POST | {email, password} | {token, user} |
| /api/logout | POST | {token} | {success} |

---

## 4. Implementation（实现）

### 4.1 File Structure（文件结构）
```
src/
├── components/
│   ├── Login.jsx
│   └── Register.jsx
├── services/
│   ├── auth.service.js
│   └── user.service.js
└── utils/
    └── validators.js
```

### 4.2 Key Functions（关键函数）
- `login(email, password)`: 用户登录
- `logout(token)`: 用户登出
- `validateEmail(email)`: 邮箱验证

### 4.3 Technical Decisions（技术决策）
| 决策 | 选择 | 理由 |
|------|------|------|
| 前端框架 | React | 团队熟悉，生态丰富 |
| 数据库 | MongoDB | 灵活 schema，快速开发 |

---

## 5. Testing（测试）

### 5.1 Unit Tests（单元测试）
- [ ] 测试登录函数
- [ ] 测试验证函数
- 覆盖率目标：80%

### 5.2 Integration Tests（集成测试）
- [ ] 测试 API 端点
- [ ] 测试数据库操作

### 5.3 Acceptance Criteria（验收标准）
- [ ] 用户可以成功登录
- [ ] 错误密码显示错误信息
- [ ] 登出后 token 失效

---

## 6. Traceability（追溯矩阵）

| 需求 ID | 实现文件 | 测试文件 | 状态 |
|--------|---------|---------|------|
| FR-001 | auth.service.js | auth.test.js | ✅ |
| FR-002 | validators.js | validators.test.js | ✅ |

---

## 7. Approval（审批）

### 7.1 Review Checklist
- [ ] 需求完整
- [ ] 设计合理
- [ ] 技术可行
- [ ] 测试覆盖

### 7.2 Approvals
- [ ] Product Owner: ________ 日期：____
- [ ] Tech Lead: ________ 日期：____

---

## 8. Changelog（变更日志）

| 版本 | 日期 | 变更内容 | 作者 | 审批状态 |
|------|------|---------|------|---------|
| v1.0 | 2026-04-06 | 初始版本 | Author | Draft |
| v1.1 | 2026-04-07 | 添加 API 设计 | Author | Approved |
```

---

## 🎯 关键要素对比

### 必备要素（必须有）

| 要素 | Spec-Kit | Spec-First | Spec Miner | Vibe Coding |
|------|---------|-----------|-----------|-------------|
| **问题陈述** | ✅ | ✅ | ⚠️ | ✅ |
| **功能需求** | ✅ | ✅ | ✅ | ✅ |
| **架构设计** | ✅ | ⚠️ | ✅ | ✅ |
| **数据模型** | ✅ | ⚠️ | ✅ | ✅ |
| **API 设计** | ✅ | ❌ | ✅ | ✅ |
| **测试策略** | ✅ | ⚠️ | ❌ | ✅ |
| **验收标准** | ✅ | ✅ | ❌ | ✅ |
| **追溯矩阵** | ❌ | ❌ | ❌ | ✅ |

### 可选要素（建议有）

| 要素 | 说明 |
|------|------|
| **非功能需求** | 性能、安全、可用性 |
| **技术决策** | 为什么选这个技术 |
| **变更日志** | 版本历史 |
| **审批记录** | 谁批准的 |

---

## 📝 最佳实践

### ✅ 应该做的

1. **简洁清晰** - 每个部分 1-2 段话
2. **具体可衡量** - 验收标准要量化
3. **图文并茂** - 架构图、流程图
4. **版本控制** - 记录变更历史
5. **团队审批** - 确保共识

### ❌ 不应该做的

1. **过于详细** - 不是设计文档
2. **技术堆砌** - 只写必要的
3. **没有验收** - 必须有验收标准
4. **一人决定** - 团队审批
5. **一成不变** - 允许迭代更新

---

## 🎯 使用示例

### 场景 1: 新功能开发

```markdown
# 用户登录功能 - SPEC.md

## 1. Overview
**问题**: 用户无法访问个人数据
**目标**: 实现安全的用户登录
**非目标**: 注册功能（另案处理）

## 2. Requirements
| ID | 需求 | 验收标准 |
|----|------|---------|
| FR-001 | 用户登录 | Given 正确凭证，When 登录，Then 成功 |

## 3. Design
**架构**: React + Node.js + JWT
**API**: POST /api/login

## 4. Implementation
**文件**: 
- src/components/Login.jsx
- src/services/auth.service.js

## 5. Testing
**单元测试**: 登录函数测试
**验收**: 可以成功登录

## 6. Approval
- [ ] PO 审批
- [ ] Tech Lead 审批
```

---

**最后更新**: 2026-04-06  
**版本**: v1.0
