# 测试计划

## 测试范围

### 单元测试
- models/: User/AuditLog 序列化、验证
- services/: 注册/登录/权限 业务逻辑
- utils/: 密码哈希/Token生成/校验

### 集成测试
- API 端点请求/响应
- 数据库 CRUD
- Redis 缓存行为

### E2E 测试
- 注册 → 登录 → 操作 完整流程
- 权限切换生效验证
- 审计日志记录验证

## 测试矩阵

| 场景 | 输入 | 预期结果 | 类型 |
|------|------|----------|------|
| 有效注册 | valid email + strong pwd | 201 Created | 单元 |
| 弱密码 | valid email + "123" | 400 + 错误码 | 单元 |
| 重复邮箱 | 已注册邮箱 | 409 Conflict | 集成 |
| 正确登录 | valid credentials | 200 + JWT | 集成 |
| 5次错误 | wrong password x5 | 423 Locked | 集成 |
| 角色赋值 | admin → editor | 200 + 即时生效 | E2E |

## 覆盖率目标
- 行覆盖率: >= 80%
- 分支覆盖率: >= 70%
- 关键路径: 100%
