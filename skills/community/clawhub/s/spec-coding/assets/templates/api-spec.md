# [API 名称] 规格文档

**状态**: `draft`  
**创建日期**: YYYY-MM-DD  
**负责人**: [姓名]  

---

## 1. 接口概述

| 属性 | 值 |
|------|-----|
| 路径 | `METHOD /api/v1/xxx` |
| 认证 | 需要/不需要 |
| 速率限制 | X 次/分钟 |
| 幂等性 | 是/否 |

---

## 2. 请求规格

### 2.1 请求头

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| Authorization | string | 是 | Bearer token |
| Content-Type | string | 是 | application/json |

### 2.2 路径参数

| 参数 | 类型 | 必填 | 约束 | 示例 |
|------|------|------|------|------|
| id | string | 是 | UUID 格式 | 550e8400-e29b... |

### 2.3 查询参数

| 参数 | 类型 | 默认值 | 约束 | 说明 |
|------|------|--------|------|------|
| page | number | 1 | >= 1 | 页码 |
| limit | number | 20 | 1-100 | 每页数量 |

### 2.4 请求体

```typescript
interface RequestBody {
  // 字段定义
  name: string;        // 必填，2-50 字符
  email?: string;      // 可选，邮箱格式
  tags?: string[];     // 可选，最多 10 个
}
```

---

## 3. 响应规格

### 3.1 成功响应 (200 OK)

```typescript
interface SuccessResponse {
  code: 0;
  data: {
    id: string;
    createdAt: string;  // ISO 8601
    // ...
  };
}
```

### 3.2 错误响应

| 状态码 | 错误码 | 说明 |
|--------|--------|------|
| 400 | INVALID_PARAM | 参数校验失败 |
| 401 | UNAUTHORIZED | 未认证 |
| 403 | FORBIDDEN | 无权限 |
| 404 | NOT_FOUND | 资源不存在 |
| 429 | RATE_LIMITED | 请求超限 |
| 500 | INTERNAL_ERROR | 服务器错误 |

```typescript
interface ErrorResponse {
  code: string;
  message: string;
  details?: Array<{
    field: string;
    reason: string;
  }>;
}
```

---

## 4. 边界情况

- 请求体为空时：返回 400 INVALID_PARAM
- 字段超出长度限制：截断/拒绝
- 并发请求：保证数据一致性

---

## 5. 验收测试用例

```bash
# 正常请求
curl -X POST /api/v1/xxx -d '{"name":"test"}'

# 边界测试
curl -X POST /api/v1/xxx -d '{"name":""}'  # 应返回 400

# 错误处理
curl -X POST /api/v1/xxx -d '{}'  # 缺少必填字段
```

---

## 6. 变更记录

| 日期 | 版本 | 变更内容 | 变更人 |
|------|------|----------|--------|
| | | | |
