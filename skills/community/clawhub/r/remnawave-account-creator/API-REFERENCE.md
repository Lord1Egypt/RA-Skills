# Remnawave API 参考文档

**最后更新**: 2026-03-19 15:50  
**状态**: ✅ 已验证

---

## 🔑 认证

```
Authorization: Bearer YOUR_API_TOKEN
```

Token 位置：`~/.openclaw/workspace/.env` 中的 `REMNAWAVE_API_TOKEN`

---

## 📄 分页参数

```
✅ 正确：page=0&size=200
❌ 错误：page=1&limit=500
```

**说明**:
- `page`: 从 0 开始（0-based）
- `size`: 每页最多 200 个用户

---

## 📡 API 端点

### 1. 获取用户列表

```http
GET /api/users?page=0&size=200
```

**响应**:
```json
{
  "response": {
    "users": [
      {
        "uuid": "...",
        "username": "...",
        "email": "...",
        "activeInternalSquads": [...]
      }
    ],
    "total": 116
  }
}
```

---

### 2. 获取单个用户（按 UUID）

```http
GET /api/users/{uuid}
```

**响应**:
```json
{
  "response": {
    "uuid": "...",
    "username": "...",
    "email": "...",
    "activeInternalSquads": [...],
    "subscriptionUrl": "..."
  }
}
```

---

### 3. 获取单个用户（按用户名）

```http
GET /api/users/by-username/{username}
```

**响应**: 同上

---

### 4. 更新用户信息（包含分组）

```http
PATCH /api/users
Content-Type: application/json
```

**请求体**（必须包含完整用户数据）:
```json
{
  "uuid": "用户 UUID",
  "username": "用户名",
  "email": "邮箱",
  "status": "ACTIVE",
  "trafficLimitBytes": 107374182400,
  "trafficLimitStrategy": "WEEK",
  "expireAt": "2027-03-19T00:00:00.000Z",
  "hwidDeviceLimit": 1,
  "activeInternalSquads": [
    "分组 UUID 1",
    "分组 UUID 2"
  ],
  "description": null,
  "tag": null,
  "telegramId": null,
  "externalSquadUuid": null
}
```

**关键参数**:
- `uuid`: **必须** - 用户 UUID
- `activeInternalSquads`: **必须** - 分组 UUID 数组
- 其他字段：建议传递完整用户数据

**响应**:
```json
{
  "response": {
    "uuid": "...",
    "username": "...",
    "activeInternalSquads": [
      {"uuid": "...", "name": "分组 1"},
      {"uuid": "...", "name": "分组 2"}
    ]
  }
}
```

---

### 5. 创建用户

```http
POST /api/users
Content-Type: application/json
```

**请求体**:
```json
{
  "username": "用户名",
  "email": "邮箱",
  "hwidDeviceLimit": 1,
  "trafficLimitBytes": 107374182400,
  "trafficLimitStrategy": "WEEK",
  "expireAt": "2027-03-19T00:00:00.000Z",
  "activeInternalSquads": ["分组 UUID"]
}
```

---

### 6. 删除用户

```http
DELETE /api/users/{uuid}
```

**响应**: 200 OK

---

## 🔧 常用操作

### 为用户添加分组

**步骤**:
1. 获取用户当前信息 `GET /api/users/{uuid}`
2. 添加新分组 UUID 到 `activeInternalSquads` 数组
3. 发送完整用户数据 `PATCH /api/users`

**示例代码**:
```javascript
// 1. 获取用户
const userResp = await callApi('GET', `/api/users/${uuid}`);
const user = userResp.response;

// 2. 添加分组
const newSquads = [
  ...user.activeInternalSquads.map(s => s.uuid),
  '新分组 UUID'
];

// 3. 更新用户
const updateData = {
  uuid: user.uuid,
  username: user.username,
  email: user.email,
  status: user.status,
  trafficLimitBytes: user.trafficLimitBytes,
  trafficLimitStrategy: user.trafficLimitStrategy,
  expireAt: user.expireAt,
  hwidDeviceLimit: user.hwidDeviceLimit,
  activeInternalSquads: newSquads,
  description: user.description,
  tag: user.tag,
  telegramId: user.telegramId,
  externalSquadUuid: user.externalSquadUuid
};

const updateResp = await callApi('PATCH', '/api/users', updateData);
```

**重要**:
- ✅ 使用 `PATCH /api/users`（不是 `PUT`）
- ✅ 传递完整用户数据（包含 `uuid` 字段）
- ✅ 订阅地址不会变化

---

## ⚠️ 常见错误

### 错误 1: 404 Not Found

**原因**: 使用了错误的端点
- ❌ `PUT /api/users/{uuid}`
- ✅ `PATCH /api/users`

### 错误 2: 分页参数错误

**原因**: 使用了错误的分页参数
- ❌ `page=1&limit=500` → 只返回 25 个用户
- ✅ `page=0&size=200` → 返回 200 个用户

### 错误 3: 响应解析错误

**原因**: callApi 包装了响应
```javascript
// callApi 返回
{ status: 200, response: {...} }

// API 原始响应
{ response: {...} }

// 正确解析
const user = resp.response;  // ✅
const user = resp.response.response;  // ❌
```

---

## 📋 分组 UUID 列表

| 分组名称 | UUID |
|---------|------|
| Default-Squad | 751440da-da97-4bc9-8a18-1074994189d1 |
| xray-default | fe107de3-e8e2-43a4-ad65-7e178578e075 |
| QA Engineer | 1f85b65c-c604-4ef7-9a05-7ab0a86a3194 |
| Front-end Developer | 48a0679d-332c-444f-89b1-faee47601380 |
| Back-end Developer | 071aee4a-1234-4c38-8f24-807c5992d9cc |
| Operations Team | 55a1c17f-ff96-4ed8-ac99-23d048e2bad1 |
| Access Gateway | 0a19fbb7-1fea-4862-b1b2-603994b3709a |

配置文件：`~/.openclaw/workspace/config/remnawave-squads.json`

---

## 🛠️ 相关脚本

| 脚本 | 用途 | 状态 |
|------|------|------|
| `search-account.js` | 搜索用户 | ✅ 已修复 |
| `add-user-to-squad-generic.js` | 添加分组（通用） | ✅ 已修复 |
| `add-squad-to-user.js` | 添加分组 | ✅ 已修复 |
| `add-squad-to-iven.js` | 添加分组（示例） | ✅ 已修复 |
| `create-account.js` | 创建用户 | ✅ 正常 |
| `list-all-users.js` | 列出所有用户 | ✅ 已修复 |

---

**验证时间**: 2026-03-19 15:50  
**验证人**: 小 a
