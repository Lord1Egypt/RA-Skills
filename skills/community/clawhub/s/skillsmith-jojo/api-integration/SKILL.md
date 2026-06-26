---
name: api-integration
description: |
  API 集成技能模板，用于快速构建与各种 API 交互的技能。
  使用场景：
  - 用户说"帮我调用某个 API"
  - 用户说"获取某个服务的数据"
  - 用户说"发送数据到 API"
  - 用户说"检查 API 状态"
metadata:
  openclaw:
    emoji: "📡"
    requires:
      bins:
        - python3
---

# API 集成技能模板

## 核心脚本

### api-client.py
通用 HTTP 客户端，支持 GET/POST/PUT/DELETE，自动处理 JSON

### auth.py
支持 OAuth 2.0、API Key、Bearer Token 等多种认证方式

### rate-limit.py
速率限制管理，防止 API 调用超限

## 快速开始

### 1. 安装依赖
```bash
pip install requests python-dotenv
```

### 2. 使用示例
```python
from scripts.api-client import APIClient
client = APIClient(base_url="https://api.example.com")
response = client.get("/users")
```

## 安全注意事项

- 不要硬编码 API Key
- 使用环境变量或配置文件
- 定期轮换 token
