# Reactive Resume 部署配置参考

## 部署方式

### 方式 1: Docker Compose（推荐）

适合自托管到 VPS 或本地服务器。

#### 基础配置

```yaml
# docker-compose.yml
version: '3.8'

services:
  app:
    image: amruthpillai/reactive-resume:latest
    ports:
      - "3000:3000"
    environment:
      - APP_URL=https://resume.yourdomain.com
      
      # 数据库
      - DATABASE_URL=postgresql://postgres:password@db:5432/reactive_resume
      
      # 认证
      - BETTER_AUTH_SECRET=your-secret-key-min-32-chars
      - BETTER_AUTH_COOKIE_DOMAIN=yourdomain.com
      
      # PDF 打印
      - PRINTER_APP_URL=http://app:3000
      - PRINTER_ENDPOINT=ws://printer:3000?token=printer-token
      
      # 存储（可选 S3）
      - STORAGE_ENDPOINT=
      - STORAGE_REGION=
      - STORAGE_BUCKET=
      - STORAGE_ACCESS_KEY_ID=
      - STORAGE_SECRET_ACCESS_KEY=
      
      # 邮件（可选）
      - SMTP_HOST=
      - SMTP_PORT=587
      - SMTP_USERNAME=
      - SMTP_PASSWORD=
      - SMTP_FROM_ADDRESS=noreply@yourdomain.com
      
      # AI（可选）
      - OPENAI_API_KEY=
      - GOOGLE_GENERATIVE_AI_API_KEY=
      - ANTHROPIC_API_KEY=
    depends_on:
      db:
        condition: service_healthy
      printer:
        condition: service_started
    restart: unless-stopped
    networks:
      - reactive-resume

  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=reactive_resume
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    networks:
      - reactive-resume

  printer:
    image: browserless/chrome:latest
    environment:
      - TOKEN=printer-token
      - ENABLE_DEBUGGER=false
      - PREBOOT_CHROME=true
      - CONNECTION_TIMEOUT=300000
    restart: unless-stopped
    networks:
      - reactive-resume

volumes:
  postgres_data:

networks:
  reactive-resume:
    driver: bridge
```

#### 启动服务

```bash
docker compose up -d
```

#### 查看日志

```bash
docker compose logs -f app
docker compose logs -f db
docker compose logs -f printer
```

#### 更新

```bash
docker compose pull
docker compose up -d
```

---

### 方式 2: Docker（单容器）

适合快速测试。

```bash
docker run -d \
  -p 3000:3000 \
  -e DATABASE_URL=postgresql://user:pass@host:5432/db \
  -e BETTER_AUTH_SECRET=your-secret \
  --name reactive-resume \
  amruthpillai/reactive-resume:latest
```

---

### 方式 3: 源码部署

适合自定义开发。

```bash
# 克隆
git clone https://github.com/amruthpillai/reactive-resume.git
cd reactive-resume

# 安装依赖
pnpm install

# 配置环境变量
cp .env.example .env
# 编辑 .env

# 构建
pnpm build

# 启动
pnpm start
```

---

## 环境变量详解

### 必需配置

| 变量 | 说明 | 示例 |
|------|------|------|
| `APP_URL` | 应用访问地址 | `https://resume.example.com` |
| `DATABASE_URL` | PostgreSQL 连接 | `postgresql://user:pass@host:5432/db` |
| `BETTER_AUTH_SECRET` | 认证密钥（32+ 字符） | `your-secret-key-min-32-chars` |

### PDF 打印

| 变量 | 说明 | 示例 |
|------|------|------|
| `PRINTER_APP_URL` | 打印服务访问地址 | `http://app:3000` |
| `PRINTER_ENDPOINT` | Browserless WebSocket | `ws://printer:3000?token=xxx` |

### 存储（可选）

默认使用本地文件系统存储。

**S3 配置**：
```bash
STORAGE_ENDPOINT=s3.amazonaws.com
STORAGE_REGION=us-east-1
STORAGE_BUCKET=resume-uploads
STORAGE_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
STORAGE_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
STORAGE_USE_PATH_STYLE=false
```

**本地存储**：留空则使用本地文件系统。

### 邮件（可选）

用于邮件验证和密码重置。

```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_ADDRESS=noreply@yourdomain.com
SMTP_SECURE=false
```

### AI 功能（可选）

```bash
OPENAI_API_KEY=sk-...
GOOGLE_GENERATIVE_AI_API_KEY=...
ANTHROPIC_API_KEY=sk-ant-...
```

---

## 反向代理配置

### Nginx

```nginx
server {
    listen 80;
    server_name resume.yourdomain.com;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Caddy

```caddyfile
resume.yourdomain.com {
    reverse_proxy localhost:3000
}
```

---

## HTTPS 配置

### 使用 Let's Encrypt

```bash
# 安装 certbot
sudo apt install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d resume.yourdomain.com

# 自动续期
sudo certbot renew --dry-run
```

### Docker 中使用 Traefik

```yaml
# docker-compose.yml
services:
  traefik:
    image: traefik:v2.10
    command:
      - "--providers.docker=true"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.letsencrypt.acme.tlschallenge=true"
      - "--certificatesresolvers.letsencrypt.acme.email=your@email.com"
      - "--certificatesresolvers.letsencrypt.acme.storage=/letsencrypt/acme.json"
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./letsencrypt:/letsencrypt

  app:
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.app.rule=Host(`resume.yourdomain.com`)"
      - "traefik.http.routers.app.entrypoints=websecure"
      - "traefik.http.routers.app.tls.certresolver=letsencrypt"
```

---

## 数据库备份

### 手动备份

```bash
docker compose exec db pg_dump -U postgres reactive_resume > backup.sql
```

### 恢复

```bash
docker compose exec -T db psql -U postgres reactive_resume < backup.sql
```

### 自动备份（cron）

```bash
# /etc/cron.daily/postgres-backup
#!/bin/bash
docker compose exec db pg_dump -U postgres reactive_resume > /backups/backup-$(date +\%Y\%m\%d).sql
find /backups -name "*.sql" -mtime +7 -delete
```

---

## 监控和日志

### 健康检查

```bash
curl http://localhost:3000/api/health
```

### 查看日志

```bash
# 应用日志
docker compose logs -f app

# 数据库日志
docker compose logs -f db

# 打印服务日志
docker compose logs -f printer
```

### 性能监控

使用 Docker 内置工具：

```bash
docker stats
docker inspect reactive-resume_app_1
```

---

## 故障排查

### 常见问题

**Q: 应用启动失败？**
A: 检查日志 `docker compose logs app`，确认环境变量配置正确。

**Q: PDF 导出失败？**
A: 确认 Browserless 服务运行，检查 `PRINTER_ENDPOINT` 配置。

**Q: 数据库连接失败？**
A: 确认 PostgreSQL 运行，检查 `DATABASE_URL` 格式。

**Q: 邮件发送失败？**
A: 检查 SMTP 配置，确认使用应用专用密码（如 Gmail）。

**Q: 内存不足？**
A: 增加服务器内存或限制 Docker 容器内存：
```yaml
services:
  app:
    deploy:
      resources:
        limits:
          memory: 1G
```

---

## 性能优化

### 数据库优化

```sql
-- 添加索引
CREATE INDEX CONCURRENTLY idx_resumes_user_id ON resumes(user_id);
CREATE INDEX CONCURRENTLY idx_resumes_updated_at ON resumes(updated_at);
```

### 缓存配置

使用 Redis 缓存（可选）：

```yaml
services:
  redis:
    image: redis:7-alpine
    restart: unless-stopped
    
  app:
    environment:
      - REDIS_URL=redis://redis:6379
```

### CDN 配置

静态资源使用 CDN：

```bash
# 环境变量
PUBLIC_ASSET_URL=https://cdn.yourdomain.com
```

---

## 安全建议

### ✅ 推荐

- 使用强密码和 HTTPS
- 定期更新 Docker 镜像
- 限制数据库访问（仅内网）
- 启用防火墙
- 定期备份数据
- 监控异常登录

### ❌ 避免

- 使用默认密码
- 暴露数据库端口到公网
- 禁用 HTTPS
- 忽略安全更新

---

*参考：[官方自部署文档](https://docs.rxresu.me/self-hosting/docker)*
