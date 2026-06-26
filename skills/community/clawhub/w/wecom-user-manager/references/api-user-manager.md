# 添加用户 API 接口

## 接口说明

通过 MCP tool 协议封装的添加用户功能。

## 操作

### add_user — 添加用户权限

使用 `wecom_mcp` tool 调用：

```
wecom_mcp call user add_user '{"userid": "zhangsan", "role": "store_manager", "store_id": "416759_1714379448487"}'
```

**入参说明：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| userid | string | ✅ | 企业微信 UserID |
| role | string | ✅ | 角色：headquarter/region/province/city/store_manager/store |
| store_id | string | ⚠️ | 门店 ID（店长/店员必填） |
| region | string | ⚠️ | 大区（区域经理必填） |
| province | string | ⚠️ | 省份（省份经理必填） |
| city | string | ⚠️ | 城市（城市经理必填） |

**返回格式：**

```json
{
  "errcode": 0,
  "errmsg": "ok",
  "data": {
    "user_id": "zhangsan",
    "username": "待激活_zhangsan",
    "user_type": "store_manager",
    "permission_level": "analyze",
    "store_ids": ["416759_1714379448487"],
    "created_at": "2026-03-28T09:27:10.053935"
  }
}
```

**返回字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| errcode | integer | 返回码，0 表示成功 |
| errmsg | string | 错误信息 |
| data | object | 用户数据 |
| data.user_id | string | 用户 ID |
| data.username | string | 用户名（首次登录时更新） |
| data.user_type | string | 用户类型 |
| data.permission_level | string | 权限等级 |
| data.store_ids | array | 可访问的门店 ID 列表 |
| data.created_at | string | 创建时间 |

---

### activate_user — 激活用户（首次登录时调用）

使用 `wecom_mcp` tool 调用：

```
wecom_mcp call user activate_user '{"userid": "zhangsan", "name": "张三"}'
```

**入参说明：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| userid | string | ✅ | 企业微信 UserID |
| name | string | ✅ | 从企业微信获取的姓名 |

**返回格式：**

```json
{
  "errcode": 0,
  "errmsg": "ok",
  "data": {
    "user_id": "zhangsan",
    "username": "张三",
    "user_type": "store_manager",
    "activated": true
  }
}
```

---

## 错误码

| errcode | errmsg | 说明 |
|---------|--------|------|
| 0 | ok | 成功 |
| 40001 | invalid userid | UserID 不存在 |
| 40002 | invalid role | 角色无效 |
| 40003 | user exists | 用户已存在 |
| 40004 | permission denied | 权限不足 |
| 40005 | store not found | 门店不存在 |

---

## 使用示例

### 示例 1：添加店长

```
wecom_mcp call user add_user '{"userid": "zhangsan", "role": "store_manager", "store_id": "416759_1714379448487"}'
```

### 示例 2：添加省份经理

```
wecom_mcp call user add_user '{"userid": "liming", "role": "province", "province": "云南"}'
```

### 示例 3：激活用户

```
wecom_mcp call user activate_user '{"userid": "zhangsan", "name": "张三"}'
```

---

## 注意事项

1. **权限检查**：只有总部管理员、区域经理、省份经理可以添加用户
2. **UserID 唯一性**：UserID 不能重复
3. **门店要求**：店长/店员必须指定门店
4. **地区要求**：区域/省份/城市经理必须指定对应地区
5. **姓名获取**：添加时无需提供姓名，首次登录时自动从企业微信获取
