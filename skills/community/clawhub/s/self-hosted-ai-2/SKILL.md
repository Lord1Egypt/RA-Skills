---
name: self-hosted-ai
description: 自托管 AI 工具部署与运维助手。用于：(1) 在服务器上部署 Ollama（本地大模型）、N8N（自动化工作流）、Open WebUI 等 AI 工具，(2) 配置 Docker / Docker Compose 环境，(3) 管理模型下载和更新，(4) 排查服务故障，(5) 配置反向代理（nginx）和 HTTPS。当用户说"部署 Ollama"、"装 N8N"、"自己跑 AI"、"搭建本地大模型"、"自托管 AI 工具"时触发此技能。
---

# Self-Hosted AI 部署助手

## 核心工具栈

| 工具 | 用途 | 端口 | 关键配置 |
|---|---|---|---|
| Ollama | 本地大模型运行 | 11434 | `OLLAMA_HOST=0.0.0.0` |
| N8N | 自动化工作流 | 5678 | 用户名/密码或 OAuth |
| Open WebUI | Ollama 的 Web UI | 3000 | 连接 Ollama `:11434` |
| Docker | 容器管理 | — | 确保 Docker daemon 运行 |
| nginx | 反向代理 + HTTPS | 80/443 | certbot 申请 SSL |

## 标准部署流程（Ollama）

```bash
# 1. 安装（Linux）
curl -fsSL https://ollama.com/install.sh | sh

# 2. 拉取模型
ollama pull llama3.2        # 轻量
ollama pull qwen2.5:14b     # 中文优化
ollama pull deepseek-r1:7b  # 推理

# 3. 配置远程访问
echo 'OLLAMA_HOST=0.0.0.0' >> /etc/environment
systemctl restart ollama

# 4. 验证
curl http://localhost:11434/api/tags
```

## 标准部署流程（N8N）

```bash
# Docker Compose 方式
mkdir -p n8n && cd n8n
cat > docker-compose.yml << 'EOF'
services:
  n8n:
    image: n8nio/n8n
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=<SET_PASSWORD>
      - N8N_HOST=0.0.0.0
      - WEBHOOK_URL=https://your-domain.com/
    volumes:
      - ./data:/home/node/.n8n
EOF
docker compose up -d
```

## nginx 反向代理配置

```nginx
# /etc/nginx/sites-available/ollama
server {
    listen 80;
    server_name ollama.your-domain.com;
    location / {
        proxy_pass http://127.0.0.1:11434;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection keep-alive;
        proxy_set_header Host $host;
    }
}
```

## 常见问题

| 问题 | 解法 |
|---|---|
| Ollama 模型下载慢 | `OLLAMA_NUM_PARALLEL=1 ollama pull <model>` 或挂代理 |
| N8N 启动失败 | 检查 `docker compose logs n8n`，通常是卷权限问题 |
| 端口被占用 | `ss -tlnp | grep <port>` 查进程 |
| 内存不足跑不动模型 | Ollama 至少 8GB RAM，建议 16GB+；用 `ollama ps` 看当前加载 |

## 实用命令

```bash
ollama list                        # 列出已下载模型
ollama show <model>                # 查看模型信息
ollama run <model> "你好"          # 快速测试
docker ps                          # 查看运行中的容器
docker compose -f n8n/docker-compose.yml logs -f  # 查看 N8N 日志
```
