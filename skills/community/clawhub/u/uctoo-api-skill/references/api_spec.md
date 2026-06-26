# Uctoo API 规范

## 端点列表

### 用户管理 (uctoo_user)
- `GET /api/uctoo/uctoo_user/{id}` - 获取单个用户
- `GET /api/uctoo/uctoo_user/{limit}/{page}` - 获取用户列表
- `POST /api/uctoo/uctoo_user/add` - 创建用户
- `POST /api/uctoo/uctoo_user/edit` - 更新用户
- `POST /api/uctoo/uctoo_user/del` - 删除用户

### 产品管理 (product)
- `GET /api/uctoo/product/{id}` - 获取单个产品
- `GET /api/uctoo/product/{limit}/{page}` - 获取产品列表
- `POST /api/uctoo/product/add` - 创建产品
- `POST /api/uctoo/product/edit` - 更新产品
- `POST /api/uctoo/product/del` - 删除产品

### 订单管理 (order)
- `GET /api/uctoo/order/{id}` - 获取单个订单
- `GET /api/uctoo/order/{limit}/{page}` - 获取订单列表
- `POST /api/uctoo/order/add` - 创建订单
- `POST /api/uctoo/order/edit` - 更新订单
- `POST /api/uctoo/order/del` - 删除订单

### 认证
- `POST /api/uctoo/auth/login` - 用户登录

## HTTP 方法规范

- **GET**: 用于数据查询操作
- **POST**: 用于创建、更新和删除操作

## 请求格式

### GET 请求示例
```
GET /api/uctoo/uctoo_user/123
GET /api/uctoo/uctoo_user/10/1
```

### POST 请求示例
```json
POST /api/uctoo/uctoo_user/add
Content-Type: application/json
Authorization: Bearer <access_token>

{
  "username": "zhangsan",
  "email": "zhangsan@example.com",
  "phone": "13800138000"
}
```

## 响应格式

### 成功响应
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": "123",
    "username": "zhangsan",
    "email": "zhangsan@example.com"
  }
}
```

### 错误响应
```json
{
  "code": 400,
  "message": "error message",
  "data": null
}
```

## 认证

使用 JWT 进行接口权限验证：
1. 通过 `/api/uctoo/auth/login` 获取 access_token
2. 在后续请求的 Header 中添加：`Authorization: Bearer <access_token>`

### 登录请求
```json
POST /api/uctoo/auth/login
Content-Type: application/json

{
  "username": "demo",
  "password": "123456"
}
```

### 登录响应
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIs...",
    "token_type": "Bearer",
    "expires_in": 7200,
    "user": {
      "id": "1",
      "username": "demo"
    }
  }
}
```
