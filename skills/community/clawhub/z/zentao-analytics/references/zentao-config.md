# 禅道连接配置

## 🔐 配置方式

### 方式一：API 连接（推荐）

```bash
# 环境变量配置
export ZENTAO_URL=https://your-zentao.com
export ZENTAO_API_KEY=your_api_key_here

# 或在 .env 文件中配置
ZENTAO_URL=https://your-zentao.com
ZENTAO_API_KEY=your_api_key_here
```

**获取 API Key:**
1. 登录禅道
2. 进入「我的地盘」→ 「设置」→ 「API Token」
3. 生成新的 Token

### 方式二：数据库直连

```bash
# 数据库配置
export ZENTAO_DB_HOST=localhost
export ZENTAO_DB_PORT=3306
export ZENTAO_DB_NAME=zentao
export ZENTAO_DB_USER=root
export ZENTAO_DB_PASS=your_password
```

**⚠️ 安全提示:**
- 生产环境建议使用只读账号
- 不要将密码提交到版本控制
- 使用 `.env` 文件管理敏感信息

---

## 📡 API 端点

### 任务相关

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/v1/tasks` | GET | 获取任务列表 |
| `/api/v1/tasks/{id}` | GET | 获取任务详情 |
| `/api/v1/users` | GET | 获取用户列表 |
| `/api/v1/projects` | GET | 获取项目列表 |

### 请求示例

```bash
# 获取所有任务
curl -H "Authorization: Bearer $ZENTAO_API_KEY" \
  "$ZENTAO_URL/api/v1/tasks"

# 获取指定用户任务
curl -H "Authorization: Bearer $ZENTAO_API_KEY" \
  "$ZENTAO_URL/api/v1/tasks?assignedTo=zhangsan"

# 获取指定日期范围任务
curl -H "Authorization: Bearer $ZENTAO_API_KEY" \
  "$ZENTAO_URL/api/v1/tasks?openedDate=2026-02-01,2026-02-28"
```

---

## 🗄️ 数据库表结构

### 主要表

| 表名 | 说明 |
|------|------|
| `zt_task` | 任务表 |
| `zt_user` | 用户表 |
| `zt_project` | 项目表 |
| `zt_story` | 需求表 |
| `zt_bug` | Bug 表 |

### 任务表关键字段

```sql
SELECT 
  id, name, assignedTo, 
  estimate, consumed, left,
  status, pri, type,
  openedDate, startedDate, finishedDate
FROM zt_task;
```

---

## 🔧 测试连接

```bash
# 测试 API 连接
node scripts/test-connection.js

# 测试数据库连接
node scripts/test-db-connection.js
```

---

## 📝 注意事项

1. **权限**: 确保账号有查看任务和工时的权限
2. **速率限制**: API 调用频率不超过 100 次/分钟
3. **数据同步**: 建议每天同步一次，避免频繁查询
4. **时区**: 确保服务器时区与禅道一致
