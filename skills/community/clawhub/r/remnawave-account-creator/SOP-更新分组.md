# Remnawave 用户分组更新 SOP

**版本：** 3.0  
**更新时间：** 2026-03-17 20:30  
**问题驱动：** west_pc 分组更新导致订阅地址变更事件

---

## ⚠️ 核心原则（血泪教训！）

### ❌ 错误做法（禁止使用）
```
1. 删除旧账号
2. 创建新账号
❌ 结果：订阅地址变更，客户端需要重新配置
```

### ✅ 正确做法（必须使用）
```
1. 调用 PATCH /api/users
2. 更新 activeInternalSquads 参数
✅ 结果：订阅地址不变，客户端无需更新
```

---

## 🔧 API 使用说明

### 更新用户分组

**端点：** `PATCH /api/users`

**请求体：**
```json
{
  "uuid": "用户 UUID",
  "username": "用户名",
  "activeInternalSquads": ["分组 UUID1", "分组 UUID2"]
}
```

**示例：**
```bash
curl -X PATCH "https://8.212.8.43/api/users" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "uuid": "f3ed591c-0999-4ecd-8331-f45519406bbd",
    "username": "west_pc",
    "activeInternalSquads": ["1f85b65c-c604-4ef7-9a05-7ab0a86a3194", "0a19fbb7-1fea-4862-b1b2-603994b3709a"]
  }'
```

**响应：**
```json
{
  "response": {
    "uuid": "f3ed591c-0999-4ecd-8331-f45519406bbd",
    "username": "west_pc",
    "subscriptionUrl": "https://.../sub/3Lcxcy73GPfxAPWb",
    "activeInternalSquads": [
      {"uuid": "1f85b65c...", "name": "QA Engineer"},
      {"uuid": "0a19fbb7...", "name": "Access Gateway"}
    ]
  }
}
```

---

## 📋 操作流程

### 场景 1：用户需要调整分组

**步骤：**

1. **获取用户 UUID**
   ```bash
   node search-account.js <用户名>
   # 或
   curl "https://8.212.8.43/api/users/by-username/<用户名>"
   ```

2. **获取目标分组 UUID**
   ```bash
   curl "https://8.212.8.43/api/internal-squads" | jq '.response.internalSquads[] | {name, uuid}'
   ```

3. **更新分组**
   ```bash
   curl -X PATCH "https://8.212.8.43/api/users" \
     -H "Authorization: Bearer TOKEN" \
     -H "Content-Type: application/json" \
     -d '{
       "uuid": "用户 UUID",
       "username": "用户名",
       "activeInternalSquads": ["分组 UUID1", "分组 UUID2"]
     }'
   ```

4. **验证结果**
   ```bash
   node search-account.js <用户名>
   # 检查分组是否正确，订阅地址是否未变
   ```

---

## 📖 可用分组列表

| 分组名称 | UUID |
|---------|------|
| Default-Squad | 751440da-da97-4bc9-8a18-1074994189d1 |
| xray-default | fe107de3-e8e2-43a4-ad65-7e178578e075 |
| QA Engineer | 1f85b65c-c604-4ef7-9a05-7ab0a86a3194 |
| Front-end Developer | 48a0679d-332c-444f-89b1-faee47601380 |
| TW | 25ef1b48-8b93-4d7a-b5d9-ee5073b322f8 |
| Back-end Developer | 071aee4a-1234-4c38-8f24-807c5992d9cc |
| Ops Debugging | ccca8442-b161-454c-8aeb-4e3e7754c4bd |
| Operations Team | 55a1c17f-ff96-4ed8-ac99-23d048e2bad1 |
| South Korea | 0ddb3374-2ed3-4e06-bddd-f401c987b9e1 |
| Access Gateway | 0a19fbb7-1fea-4862-b1b2-603994b3709a |

---

## ⚠️ 注意事项

### 1. 订阅地址不变
- ✅ 使用 `PATCH /api/users` 更新分组 → 订阅地址**不变**
- ❌ 删除重建账号 → 订阅地址**变更**

### 2. 多分组支持
`activeInternalSquads` 是数组，支持同时分配到多个分组：
```json
"activeInternalSquads": [
  "1f85b65c-c604-4ef7-9a05-7ab0a86a3194",  // QA Engineer
  "0a19fbb7-1fea-4862-b1b2-603994b3709a"   // Access Gateway
]
```

### 3. 必须包含的参数
- `uuid` - 用户 UUID（必需）
- `username` - 用户名（必需）
- `activeInternalSquads` - 分组 UUID 数组（必需）

### 4. 可选参数
以下参数也可以同时更新（可选）：
- `status` - 用户状态
- `trafficLimitBytes` - 流量限制
- `trafficLimitStrategy` - 流量重置策略
- `expireAt` - 过期时间
- `email` - 邮箱
- `hwidDeviceLimit` - 设备限制

---

## 🧪 测试用例

### 测试 1：更新单个分组
```bash
curl -X PATCH "https://8.212.8.43/api/users" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "uuid": "用户 UUID",
    "username": "west_pc",
    "activeInternalSquads": ["1f85b65c-c604-4ef7-9a05-7ab0a86a3194"]
  }'
```
**预期：** 用户分组更新为 QA Engineer，订阅地址不变

### 测试 2：更新多个分组
```bash
curl -X PATCH "https://8.212.8.43/api/users" \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "uuid": "用户 UUID",
    "username": "west_pc",
    "activeInternalSquads": [
      "1f85b65c-c604-4ef7-9a05-7ab0a86a3194",
      "0a19fbb7-1fea-4862-b1b2-603994b3709a"
    ]
  }'
```
**预期：** 用户分组更新为 QA Engineer + Access Gateway，订阅地址不变

### 测试 3：验证订阅地址未变
```bash
# 更新前
node search-account.js west_pc
# 记录订阅地址

# 更新分组
curl -X PATCH ...

# 更新后
node search-account.js west_pc
# 验证订阅地址相同
```

---

## 📚 相关文档

- [Remnawave API 文档](https://docs.rw/api)
- [账号创建 SOP](./SKILL.md)
- [账号搜索 SOP](./SOP-搜索账号.md)

---

## 🎯 最佳实践

1. **优先使用 PATCH 更新** - 不要删除重建
2. **更新前备份** - 记录当前分组和订阅地址
3. **更新后验证** - 确认分组正确，订阅地址未变
4. **通知用户** - 如果必须删除重建，提前告知用户

---

**最后更新：** 2026-03-17 20:30  
**更新内容：** v3.0 - 明确使用 PATCH /api/users 更新分组  
**下次审查：** 2026-04-17 或发现新问题时
