---
name: wecom-user-manager
description: 企业微信用户管理技能。支持管理员添加用户权限，用户首次登录自动激活。包含完整的用户生命周期管理。
metadata:
  {
    "openclaw": { "emoji": "👤", "requires": { "bins": ["python3"] } },
  }
---

# 企业微信用户管理技能

> 完整的用户生命周期管理：添加用户 → 自动激活 → 权限管理

---

## 🎯 功能概述

### 管理员视角
- ✅ 添加用户权限（支持自然语言命令）
- ✅ 发送确认卡片
- ✅ 处理回调创建用户

### 用户视角
- ✅ 首次登录自动激活
- ✅ 自动获取真实姓名
- ✅ 欢迎消息和权限信息

---

## 📱 使用流程

### 流程 1：管理员添加用户

```
管理员：添加用户 zhangsan 店长 正义路

机器人：
┌────────────────────────────────┐
│ 请确认以下信息                  │
│ UserID: zhangsan               │
│                                │
│ 角色：店长                      │
│ 门店：昆明五华区正义路 60 号红谷  │
│                                │
│ ℹ️  姓名将在首次登录时自动获取  │
│                                │
│ [✅ 确认添加] [🔄 重新选择]    │
└────────────────────────────────┘

管理员点击确认：
✅ 用户添加成功！
ℹ️  姓名将在首次登录时自动获取
```

### 流程 2：用户首次登录

```
用户（首次）：你好

机器人：
👋 欢迎使用红谷门店经营助手！

检测到您是首次使用，正在激活账户...
✅ 账户已激活

姓名：张三
企业微信 ID: zhangsan
角色：店长
门店：1 家

现在可以开始使用了！
```

### 流程 3：用户再次登录

```
用户：早上好

机器人：
早上好，张三！有什么可以帮您？
```

---

## 🔧 核心功能

### 1. 添加用户

**命令格式**：
```
添加用户 <UserID> <角色> <门店/地区>
```

**支持的角色**：
- 总部管理员/总部/管理员
- 区域经理/区域/大区
- 省份经理/省份/省级
- 城市经理/城市
- 店长
- 店员/导购

**示例**：
```
添加用户 zhangsan 店长 正义路
添加用户 liming 省份经理 云南
添加用户 wangwu 区域经理 西南区
```

### 2. 自动激活

**触发条件**：
- 用户首次发送任意消息
- 用户状态为"待激活_xxx"

**激活流程**：
1. 提取 UserID 和姓名
2. 检查用户状态
3. 更新用户名（从"待激活_" → 真实姓名）
4. 记录登录时间
5. 发送欢迎消息

### 3. 权限检查

**可以添加用户的角色**：
- ✅ 总部管理员
- ✅ 区域经理
- ✅ 省份经理

**不可以添加用户的角色**：
- ❌ 城市经理
- ❌ 店长
- ❌ 店员

---

## 📁 文件结构

```
wecom-user-manager/
├── SKILL.md                    # 技能文档（本文件）
├── handler.py                  # 消息处理器
├── auto_activate.py            # 自动激活脚本
├── references/
│   └── api-user-manager.md     # API 文档
└── tests/
    └── test_user_manager.py    # 测试脚本
```

---

## 🔗 API 接口

### add_user — 添加用户

```
wecom_mcp call user add_user '{"userid": "zhangsan", "role": "store_manager", "store_id": "xxx"}'
```

### activate_user — 激活用户

```
wecom_mcp call user activate_user '{"userid": "zhangsan", "name": "张三"}'
```

### check_user — 检查用户状态

```
wecom_mcp call user check_user '{"userid": "zhangsan"}'
```

---

## ⚠️ 注意事项

### 1. UserID 格式
- 必须是企业微信中的真实 UserID
- 可以在企业微信管理后台查看
- 格式如：`zhangsan`、`liming001`、`10001`

### 2. 姓名获取
- 添加时无需提供姓名
- 首次登录时自动从企业微信获取
- 确保 UserID 与企业微信一致

### 3. 门店搜索
- 支持模糊搜索
- 输入关键词即可（如"正义路"）
- 如有多个匹配，会提示选择

### 4. 配置文件同步
- 工作区和插件目录的 users.json 需要保持同步
- 激活后自动同步

---

## 🧪 测试用例

### 测试 1：添加用户
```bash
python3 handler.py handle_message "添加用户 zhangsan 店长 正义路" "hq_admin_001"
```

### 测试 2：自动激活
```bash
python3 auto_activate.py check_and_activate "zhangsan" "张三"
```

### 测试 3：权限检查
```bash
python3 handler.py check_permission "store_clerk_001"
# 应返回：无权限
```

---

## 📊 用户状态流转

```
添加用户 → 待激活_xxx → (首次登录) → 真实姓名 → (后续登录) → 更新 last_login
```

| 状态 | username 前缀 | 操作 |
|------|--------------|------|
| 待激活 | `待激活_` | 激活并更新用户名 |
| 已激活 | 其他 | 仅更新 last_login |

---

## 🎯 典型场景

### 场景 1：新店开业添加店长

```
管理员：添加用户 zhangsan 店长 正义路
→ 发送确认卡片
→ 管理员确认
→ 用户创建成功

zhangsan 首次登录：
→ 自动激活
→ 发送欢迎消息
→ 开始使用
```

### 场景 2：批量添加店员

```
管理员：添加用户 liming 店员 正义路
管理员：添加用户 wangwu 店员 正义路
管理员：添加用户 zhaoliu 店员 正义路

liming 首次登录：
→ 自动激活
→ "欢迎使用，liming！"
```

### 场景 3：添加省份经理

```
管理员：添加用户 sunqi 省份经理 云南
→ 发送确认卡片（不需要门店）
→ 管理员确认
→ 用户创建成功（可访问云南省所有门店）

sunqi 首次登录：
→ 自动激活
→ "欢迎使用，sunqi！您管理云南省所有门店"
```

---

## 🔍 故障排查

### 问题 1：用户未自动激活

**症状**：用户发送消息后，username 仍然是"待激活_xxx"

**解决**：
```bash
# 手动激活
python3 auto_activate.py check_and_activate "userid" "姓名"

# 检查配置文件
cat config/users.json | grep "userid"
```

### 问题 2：权限不足

**症状**：店长尝试添加用户时收到"权限不足"提示

**解决**：
- 只有总部/区域/省份经理可以添加用户
- 联系总部管理员添加

### 问题 3：配置文件不同步

**症状**：插件目录已激活，工作区仍是待激活

**解决**：
```bash
# 同步配置文件
cp plugin/config/users.json workspace/config/users.json
```

---

## 📝 最佳实践

### 1. 自动激活流程

```javascript
// 企业微信插件消息处理
async function onMessage(message) {
    const { from_userid, from_name } = message;
    
    // 1. 自动激活
    const result = await activateUser(from_userid, from_name);
    
    // 2. 如果是首次激活，发送欢迎消息
    if (result.activated) {
        await sendWelcomeMessage(from_userid, result.message);
    }
    
    // 3. 继续处理其他消息
    await handleMessage(message);
}
```

### 2. 配置文件管理

```bash
# 启动时同步
cp workspace/config/users.json plugin/config/users.json

# 关闭时同步
cp plugin/config/users.json workspace/config/users.json
```

### 3. 日志记录

```python
# 记录用户操作
logging.info(f"添加用户：{userid}, 角色：{role}")
logging.info(f"激活用户：{userid}, 姓名：{name}")
```

---

## 🎊 总结

**wecom-user-manager** 是一个完整的用户管理 Skill，包含：

1. ✅ **添加用户** - 支持自然语言命令
2. ✅ **自动激活** - 首次登录自动完成
3. ✅ **权限管理** - 严格的权限控制
4. ✅ **欢迎消息** - 个性化的用户体验

---

**最后更新**: 2026-03-28  
**版本**: v1.0 (合并版)  
**状态**: ✅ 已部署
