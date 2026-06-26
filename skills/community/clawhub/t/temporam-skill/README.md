# Temporam Temp Mail Skill

基于 [Temporam API](https://www.temporam.com/docs/api-reference) 的临时邮箱 Agent Skill，提供临时邮箱地址生成、邮件列表查询和邮件内容获取功能。适用于需要邮箱验证或临时通信的自动化场景。

## 功能

- **获取可用域名** — 从 Temporam 服务获取可用的邮箱域名列表
- **生成临时邮箱** — 自动生成随机的临时邮箱地址
- **查询邮件列表** — 查看指定临时邮箱收到的邮件，支持分页
- **获取邮件内容** — 根据邮件 ID 获取完整的邮件详情
- **获取最新邮件** — 直接获取指定邮箱最近收到的一封邮件（含完整内容），适合轮询验证码等场景

## 项目结构

```
.
├── SKILL.md          # Skill 定义与使用说明
├── clawhub.json      # ClawHub 发布元数据
├── mcp_server.py     # MCP Server（基于 FastMCP）
└── scripts/
    └── client.py     # Python 客户端封装
```

## 快速开始

### 环境要求

- Python 3.10+
- 有效的 Temporam API Key

### 安装依赖

```bash
pip install requests mcp
```

### 配置 API Key

```bash
export TEMPORAM_API_KEY="your_api_key_here"
```

### 作为 MCP Server 运行

```bash
python mcp_server.py
```

### 作为 Python 客户端使用

```python
from scripts.client import TemporamClient

client = TemporamClient()

# 生成临时邮箱
email = client.generate_random_email()
print(f"临时邮箱: {email}")

# 查询邮件列表
emails = client.list_emails(email)

# 获取邮件内容
detail = client.get_email_detail("<email_id>")

# 获取最新邮件（适合轮询场景）
latest = client.get_latest_email(email)
```

## MCP Tools

| Tool | 说明 |
|------|------|
| `get_domains` | 获取可用邮箱域名列表 |
| `list_emails` | 查询指定邮箱的邮件列表 |
| `get_email_content` | 根据 ID 获取邮件完整内容 |
| `get_latest_email` | 获取指定邮箱最近收到的一封邮件（含完整内容） |

## 许可证

MIT
