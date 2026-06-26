# 云效 MCP Server 部署与运维

> ⚠️ **重要：必须人工手动部署**
>
> MCP Server 的部署涉及阿里云 RAM AccessKey 等敏感凭证，**必须由人工手动执行**。
>
> AI agent **不得自动执行**以下部署命令，应：
> 1. 提示用户需要手动部署 MCP Server
> 2. 引导用户阅读本文档
> 3. 等待用户确认部署完成后再使用客户端
>
> 部署前请确认：
> - 已获取阿里云 RAM AccessKey（需要有云效相关权限）
> - 本机已安装 Docker 和 Docker Compose
> - 用户已阅读并理解部署步骤

## Docker Compose 部署

```bash
mkdir -p ~/mcp/yunxiao && cd ~/mcp/yunxiao

cat > docker-compose.yml << 'EOF'
version: '3.8'
services:
  yunxiao-mcp:
    image: build-steps-public-registry.cn-beijing.cr.aliyuncs.com/build-steps/alibabacloud-devops-mcp-server:latest
    container_name: yunxiao-mcp
    ports:
      - "3000:3000"
    env_file:
      - .env
    restart: unless-stopped
    command: node dist/index.js --sse
    healthcheck:
      test: ["CMD", "wget", "-q", "--spider", "--timeout=5", "http://localhost:3000/sse"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
EOF

cat > .env << 'EOF'
ALIBABA_CLOUD_ACCESS_KEY_ID=<your_access_key_id>
ALIBABA_CLOUD_ACCESS_KEY_SECRET=<your_access_key_secret>
ALIBABA_CLOUD_REGION=cn-hangzhou
EOF

docker compose up -d
```

## MCP Server 管理

```bash
# 查看状态
docker ps --filter "name=yunxiao-mcp"

# 查看日志
docker logs yunxiao-mcp --tail 50

# 重启
cd ~/mcp/yunxiao && docker compose restart

# 停止
cd ~/mcp/yunxiao && docker compose down

# 启动
cd ~/mcp/yunxiao && docker compose up -d
```

## 故障排查

### MCP Server 无法连接

```bash
# 检查容器状态
docker ps -a --filter "name=yunxiao-mcp"

# 查看日志
docker logs yunxiao-mcp --tail 100

# 重启容器
cd ~/mcp/yunxiao && docker compose restart
```

### 客户端问题

```bash
# 重新安装依赖（在项目 client 目录下执行）
cd client && npm install
```
