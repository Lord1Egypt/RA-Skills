# 🚀 快速开始指南

## 5分钟快速部署

### 1. 安装 Skill

```bash
# 从 Clawhub 安装
clawhub install wecom-deep-op

# 或本地安装
cd /path/to/wecom-deep-op
npm install
npm run build
```

### 2. 配置企业微信 BOT

1. 登录 [企业微信管理后台](https://work.weixin.qq.com/)
2. 进入「应用管理」→ 「自建应用」→ 选择你的 BOT
3. 在「权限管理」中开通 MCP 权限：
   - 📄 文档管理（读写）
   - 📅 日程管理（读写）
   - 📹 会议管理（创建/查询/取消）
   - ✅ 待办事项（读写）
   - 👥 通讯录查看（受限范围）
4. 复制每个服务的 `uaKey`

### 3. 配置 OpenClaw

**方法A：环境变量（推荐）**

```bash
# 在 ~/.bashrc 或 ~/.profile 中添加
export WECOM_DOC_BASE_URL="https://qyapi.weixin.qq.com/mcp/bot/doc?uaKey=YOUR_KEY"
export WECOM_SCHEDULE_BASE_URL="https://qyapi.weixin.qq.com/mcp/bot/schedule?uaKey=YOUR_KEY"
export WECOM_MEETING_BASE_URL="https://qyapi.weixin.qq.com/mcp/bot/meeting?uaKey=YOUR_KEY"
export WECOM_TODO_BASE_URL="https://qyapi.weixin.qq.com/mcp/bot/todo?uaKey=YOUR_KEY"
export WECOM_CONTACT_BASE_URL="https://qyapi.weixin.qq.com/mcp/bot/contact?uaKey=YOUR_KEY"

# 重新加载
source ~/.bashrc
```

**方法B：mcporter.json**

```json
{
  "mcpServers": {
    "wecom-doc": { "baseUrl": "https://.../doc?uaKey=YOUR_KEY" },
    "wecom-schedule": { "baseUrl": "https://.../schedule?uaKey=YOUR_KEY" },
    "wecom-meeting": { "baseUrl": "https://.../meeting?uaKey=YOUR_KEY" },
    "wecom-todo": { "baseUrl": "https://.../todo?uaKey=YOUR_KEY" },
    "wecom-contact": { "baseUrl": "https://.../contact?uaKey=YOUR_KEY" }
  }
}
```

### 4. 测试连接

```bash
# 健康检查
wecom_mcp call wecom-deep-op.ping '{}'

# 预期输出
{
  "errcode": 0,
  "data": {
    "service": "wecom-deep-op",
    "version": "1.0.0",
    "status": "healthy"
  }
}

# 前置条件检查
wecom_mcp call wecom-deep-op.preflight_check '{}'
```

### 5. 创建第一个文档

```bash
wecom_mcp call wecom-deep-op.doc_create '{
  "doc_type": 3,
  "doc_name": "我的第一个文档"
}'

# 返回
{
  "errcode": 0,
  "docid": "dc123...",
  "url": "https://doc.weixin.qq.com/doc/..."
}
```

---

## 常用操作示例

### 创建待办

```bash
wecom_mcp call wecom-deep-op.todo_create '{
  "title": "审核合同",
  "due_time": "2026-03-23 18:00:00",
  "priority": 2,
  "desc": "请审核附件合同并反馈"
}'
```

### 预约会议

```bash
wecom_mcp call wecom-deep-op.meeting_create '{
  "subject": "周会",
  "start_time": "2026-03-22 10:00:00",
  "end_time": "2026-03-22 11:00:00",
  "attendees": ["zhangsan", "lisi"]
}'
```

### 查询日程

```bash
wecom_mcp call wecom-deep-op.schedule_list '{
  "start_time": "2026-03-21 00:00:00",
  "end_time": "2026-03-22 00:00:00"
}'
```

---

## 完整文档

- 📖 [完整 README](README.md) - 详细 API 参考和使用示例
- 📝 [发布指南](PUBLISHING.md) - 如何发布到 GitHub 和 Clawhub
- 🔧 [开发文档](CLAWHUB_PUBLISHING.md) - 开发和维护指南
- 🐙 [仓库地址](https://github.com/YOUR_USERNAME/wecom-deep-op) - GitHub 仓库（发布后填写）

---

## 故障排除

| 问题 | 解决方案 |
|------|----------|
| `Unknown MCP server` | 检查 mcporter.json 配置 |
| `Missing configuration` | 设置 WECOM_*_BASE_URL 环境变量 |
| `errcode=60001` | 在企微后台重新授权 BOT |
| `Task timeout` | 文档太大，等待或分卷导出 |

---

## 安全提示

⚠️ **本 Skill 不会存储任何你的 uaKey 或 token**。所有配置必须由用户自己管理，请妥善保管 `uaKey`（等同于密码）。

---

**需要帮助？** 查看 [README.md](README.md) 或在 [GitHub Issues](https://github.com/YOUR_USERNAME/wecom-deep-op/issues) 提问。
