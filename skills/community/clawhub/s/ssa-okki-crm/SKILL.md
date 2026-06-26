---
name: okki-crm-integration
description: 连接 OKKI（小满）CRM 系统，支持查询客户、创建跟进记录、管理订单等操作。频道限定触发。
---

# OKKI CRM 集成技能

## 描述
连接 OKKI（小满）CRM 系统，支持查询客户、创建跟进记录、管理订单等操作。

## ⚠️ 触发规则（重要）

**只在 `#okki` 频道触发**，其他频道不响应 OKKI 相关命令。

| 配置项 | 值 |
|--------|-----|
| 触发频道 | `#okki` (ID: `process.env.DISCORD_OKKI_CHANNEL_ID`) |
| 触发模式 | 频道限定 |
| 关键词触发 | 关闭（避免误触发） |

**行为说明**：
- ✅ 在 `#okki` 频道：自动识别并执行 OKKI 相关命令
- ❌ 在其他频道：不响应 OKKI 相关命令（可提示"请在 #okki 频道执行此操作"）

---

## 环境
- **环境**: 沙盒环境 (`api-sandbox.xiaoman.cn`)
- **配置**: `$OKKI_WORKSPACE/api/config.json` (环境变量或相对路径)
- **客户端**: `$OKKI_WORKSPACE/api/okki_client.py`

## 输出格式规范

### 查询客户列表/详情

**禁止输出 ID**（对公司_id、user_id 等），默认展示：

| 字段 | 说明 | 来源 |
|------|------|------|
| 客户名称 | 公司全称 | `name` |
| 官网 | 公司网站 | `homepage` |
| 国家/地区 | 所在国家 | `country` |
| 地址 | 详细地址 | `address` |
| 备注/简介 | 业务描述 | `remark` |
| 客户类型 | 品牌商/经销商/其他 | 从 `biz_type` 或备注推断 |
| 行业分类 | 主营产品/服务 | 从 `category` 或备注推断 |
| 创建时间 | 录入系统时间 | `create_time` |

**示例输出：**
```markdown
| 客户名称 | 官网 | 国家 | 地址 | 备注 |
|----------|------|------|------|------|
| YABER | http://yaber.jp | US | - | 家庭娱乐投影仪研发与销售 |
```

### 查询跟进记录

| 字段 | 说明 |
|------|------|
| 跟进时间 | `create_time` |
| 跟进方式 | 电话/邮件/会面/社交平台 |
| 跟进内容 | `content` |
| 负责人 | `create_user` |

### 🟢 低风险（直接执行）
- `list_companies` - 查询客户列表
- `get_company <id>` - 查询客户详情
- `list_products` - 查询产品列表
- `list_trails <company_id>` - 查询跟进动态
- `list_orders` - 查询订单列表
- `list_users` - 查询用户列表

### 🟡 中风险（首次确认）
- `create_lead <data>` - 新建线索
- `create_trail <company_id> <content>` - 提交跟进记录
- `list_leads` - 查询线索列表

### 🔴 高风险（每次确认）
- `create_company <data>` - 新建客户
- `update_company <id> <data>` - 更新客户信息
- `delete_company <id>` - 删除客户
- `create_order <data>` - 创建销售订单
- `send_email <data>` - 发送邮件

## 使用方法

### 命令行
```bash
# 查询客户列表
python3 $OKKI_WORKSPACE/api/okki_client.py list_companies

# 查询客户详情
python3 $OKKI_WORKSPACE/api/okki_client.py get_company <company_id>

# 查询跟进动态
python3 $OKKI_WORKSPACE/api/okki_client.py list_trails <company_id>
```

### Python 调用
```python
from okki_client import OKKIClient, check_risk

client = OKKIClient()

# 查询客户
result = client.list_companies()

# 提交跟进记录
result = client.create_trail(company_id=12345, content="电话沟通，有意向")

# 检查风险
risk = check_risk("create_company")  # 返回 {"level": "high", "confirm": "always", ...}
```

## 触发场景

当用户的问题涉及以下关键词时，自动使用 OKKI 技能：
- "查客户"、"客户列表"、"客户详情"
- "跟进记录"、"跟进动态"
- "订单"、"产品"、"线索"
- "OKKI"、"小满"、"CRM"

## 注意事项

1. 所有写入操作需要遵循风险检查策略
2. 沙盒环境数据与生产环境隔离
3. Token 自动缓存，过期自动刷新
  
  <description>待补充描述</description>
  <location>/Users/wilson/.openclaw/workspace/skills/okki</location>
