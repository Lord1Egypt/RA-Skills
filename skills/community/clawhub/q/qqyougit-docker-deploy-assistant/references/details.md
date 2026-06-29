# Docker部署助手 - 详细内容参考 v1.3.0

## 一、各语言Dockerfile最佳实践

### 1.1 Node.js/Express应用
```dockerfile
# ===== 阶段1：依赖安装 =====
FROM node:18-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# ===== 阶段2：构建（如需要） =====
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# ===== 阶段3：生产运行 =====
FROM node:18-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 --ingroup nodejs appuser
COPY --from=deps --chown=appuser:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=appuser:nodejs /app/dist ./dist
USER appuser
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://localhost:3000/health || exit 1
CMD ["node", "dist/index.js"]
```

### 1.2 Python/Flask/Django应用
```dockerfile
# ===== 阶段1：构建 =====
FROM python:3.11-slim AS builder
WORKDIR /app
RUN pip install --no-cache-dir --user -r requirements.txt

# ===== 阶段2：运行 =====
FROM python:3.11-slim AS runner
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app
COPY --from=builder /root/.local /root/.local
COPY . .
RUN addgroup --system --gid 1001 pygroup && \
    adduser --system --uid 1001 --ingroup pygroup pyuser && \
    chown -R pyuser:pygroup /app
USER pyuser
EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=3s CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

### 1.3 Go应用（极小镜像）
```dockerfile
# ===== 阶段1：构建 =====
FROM golang:1.21-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -ldflags='-w -s' -o main .

# ===== 阶段2：运行（使用scratch或alpine） =====
FROM alpine:3.19
RUN apk --no-cache add ca-certificates tzdata && \
    addgroup -S appgroup && adduser -S appuser -G appgroup
WORKDIR /root/
COPY --from=builder /app/main .
USER appuser
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://localhost:8080/health || exit 1
CMD ["./main"]
```

### 1.4 Java/Spring Boot应用
```dockerfile
# ===== 阶段1：构建 =====
FROM maven:3.9-eclipse-temurin-21 AS builder
WORKDIR /app
COPY pom.xml .
RUN mvn dependency:go-offline -B
COPY src ./src
RUN mvn package -DskipTests -B

# ===== 阶段2：运行 =====
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
RUN addgroup -S spring && adduser -S spring -G spring
COPY --from=builder /app/target/*.jar app.jar
RUN chown spring:spring app.jar
USER spring
EXPOSE 8080
ENV JAVA_OPTS="-Xmx512m -Xms256m"
HEALTHCHECK --interval=30s --timeout=10s CMD wget -qO- http://localhost:8080/actuator/health || exit 1
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar app.jar"]
```

### 1.5 React/Vue前端应用
```dockerfile
# ===== 阶段1：构建 =====
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

# ===== 阶段2：Nginx运行 =====
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
COPY default.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s CMD wget -qO- http://localhost/health || exit 1
CMD ["nginx", "-g", "daemon off;"]
```

### 1.6 Next.js应用
```dockerfile
FROM node:18-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
ENV NEXT_TELEMETRY_DISABLED 1
RUN npm run build

FROM node:18-alpine AS runner
WORKDIR /app
ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 nextjs
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static
USER nextjs
EXPOSE 3000
ENV PORT 3000
CMD ["node", "server.js"]
```

## 二、docker-compose高级配置

### 2.1 Nginx反向代理配置
```nginx
# nginx/conf.d/default.conf
upstream app_backend {
    server app:3000;
}

server {
    listen 80;
    server_name example.com www.example.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name example.com www.example.com;

    # SSL证书
    ssl_certificate /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;

    # 安全头
    add_header Strict-Transport-Security "max-age=31536000" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;

    # 静态资源缓存
    location /static/ {
        proxy_pass http://app_backend;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # API请求
    location /api/ {
        proxy_pass http://app_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 300s;
    }

    # WebSocket
    location /ws {
        proxy_pass http://app_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    # 前端路由（SPA）
    location / {
        proxy_pass http://app_backend;
        try_files $uri $uri/ /index.html;
    }
}
```

### 2.2 多环境配置
```yaml
# docker-compose.dev.yml（开发环境）
version: '3.8'
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    volumes:
      - .:/app  # 挂载源码，支持热重载
      - /app/node_modules
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
    command: npm run dev

# docker-compose.prod.yml（生产环境）
version: '3.8'
services:
  app:
    image: myapp:${TAG:-latest}
    restart: unless-stopped
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '1.0'
```

### 2.3 .env 文件配置
```bash
# .env（不要提交到git！）
# 应用配置
APP_NAME=myapp
APP_PORT=3000
TAG=latest

# 数据库配置
DB_HOST=postgres
DB_PORT=5432
DB_NAME=myapp_db
DB_USER=myapp_user
DB_PASSWORD=your_secure_password_here

# Redis配置
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password_here

# JWT密钥
JWT_SECRET=your_jwt_secret_here

# 第三方服务
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_app_password
```

## 三、镜像构建优化技巧

### 3.1 镜像大小优化清单
| 优化手段 | 节省大小 | 难度 |
|---------|---------|------|
| 使用Alpine基础镜像 | 50-150MB | ⭐ |
| 多阶段构建 | 200-500MB | ⭐⭐ |
| 合并RUN指令 | 10-50MB | ⭐ |
| .dockerignore排除不必要文件 | 5-50MB | ⭐ |
| 清理apt缓存 | 10-30MB | ⭐ |
| 不安装文档和手册 | 5-20MB | ⭐ |
| 使用distroless/scratch | 额外50-100MB | ⭐⭐⭐ |
| 压缩构建产物 | 10-30MB | ⭐⭐ |

### 3.2 .dockerignore模板
```
# 版本控制
.git
.gitignore
.svn

# 依赖目录（应通过COPY安装）
node_modules
__pycache__
.venv
vendor

# 构建产物（应在构建阶段生成）
dist
build
.next
.nuxt
target

# 日志和临时文件
*.log
*.tmp
*.swp

# 开发配置
.vscode
.idea
.env*
.dockerignore

# 文档（镜像中不需要）
README.md
CHANGELOG.md
docs/

# 测试相关
coverage/
.nyc_output/
*.test.*
*.spec.*

# 系统文件
.DS_Store
Thumbs.db
```

### 3.3 构建缓存优化
```dockerfile
# ❌ 错误：每次源码变更都重建依赖
COPY . .
RUN npm install

# ✅ 正确：先复制依赖文件，源码放最后
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
```

## 四、部署与运维脚本

### 4.1 部署脚本 deploy.sh
```bash
#!/bin/bash
set -e

# 配置
APP_NAME="myapp"
TAG=${1:-latest}
REGISTRY="registry.example.com"
SERVER="deploy@example.com"
DEPLOY_DIR="/opt/${APP_NAME}"

echo "🚀 开始部署 ${APP_NAME}:${TAG}"

# 构建镜像
echo "==> 构建镜像..."
docker build -t ${APP_NAME}:${TAG} .

# 打标签并推送
echo "==> 推送镜像..."
docker tag ${APP_NAME}:${TAG} ${REGISTRY}/${APP_NAME}:${TAG}
docker push ${REGISTRY}/${APP_NAME}:${TAG}

# 部署到服务器
echo "==> 部署到服务器..."
ssh ${SERVER} << EOF
    cd ${DEPLOY_DIR}
    docker-compose pull
    docker-compose up -d
    # 等待健康检查
    sleep 10
    docker-compose ps
EOF

# 清理本地
echo "==> 清理..."
docker system prune -f

echo "✅ 部署完成!"
```

### 4.2 回滚脚本 rollback.sh
```bash
#!/bin/bash
set -e

APP_NAME="myapp"
BACKUP_TAG=${1}
SERVER="deploy@example.com"
DEPLOY_DIR="/opt/${APP_NAME}"

if [ -z "$BACKUP_TAG" ]; then
    echo "❌ 请指定回滚版本: ./rollback.sh <tag>"
    exit 1
fi

echo "⏪ 回滚到 ${APP_NAME}:${BACKUP_TAG}"

ssh ${SERVER} << EOF
    cd ${DEPLOY_DIR}
    export TAG=${BACKUP_TAG}
    docker-compose pull
    docker-compose up -d
    sleep 10
    docker-compose ps
EOF

echo "✅ 回滚完成!"
```

### 4.3 备份脚本 backup.sh
```bash
#!/bin/bash
set -e

APP_NAME="myapp"
BACKUP_DIR="/backups/${APP_NAME}"
DATE=$(date +%Y%m%d_%H%M%S)
RETENTION_DAYS=30

echo "💾 开始备份 ${APP_NAME} - ${DATE}"

# 创建备份目录
mkdir -p ${BACKUP_DIR}

# 备份数据库
docker exec postgres pg_dump -U myapp_user myapp_db | \
    gzip > ${BACKUP_DIR}/db_${DATE}.sql.gz

# 备份数据卷
docker run --rm -v ${APP_NAME}_app-data:/data -v ${BACKUP_DIR}:/backup \
    alpine tar czf /backup/data_${DATE}.tar.gz -C /data .

# 清理旧备份
find ${BACKUP_DIR} -name "*.gz" -mtime +${RETENTION_DAYS} -delete

echo "✅ 备份完成: ${BACKUP_DIR}"
ls -lh ${BACKUP_DIR}/*${DATE}*
```

## 五、安全最佳实践

### 5.1 安全检查清单
```bash
#!/bin/bash
# 安全扫描脚本

echo "🔍 安全扫描开始..."

# 1. 漏洞扫描
echo "==> Trivy漏洞扫描..."
trivy image --severity HIGH,CRITICAL myapp:latest

# 2. 检查非root用户
echo "==> 检查运行用户..."
docker inspect myapp --format='{{.Config.User}}'

# 3. 检查特权模式
echo "==> 检查特权模式..."
docker inspect myapp --format='{{.HostConfig.Privileged}}'

# 4. 检查只读文件系统
echo "==> 检查只读文件系统..."
docker inspect myapp --format='{{.HostConfig.ReadonlyRootfs}}'

# 5. 检查端口暴露
echo "==> 检查端口暴露..."
docker inspect myapp --format='{{json .NetworkSettings.Ports}}'

echo "✅ 安全检查完成"
```

### 5.2 安全配置建议
| 安全项 | 推荐配置 | 说明 |
|--------|----------|------|
| 运行用户 | 非root专用用户 | 防止容器逃逸 |
| 文件系统 | 只读（关键目录可写） | 防止文件篡改 |
| 网络 | 最小暴露 | 仅暴露必要端口 |
| Capabilities | --cap-drop=ALL | 最小权限原则 |
| Secrets | Docker Secrets/环境变量 | 不硬编码在镜像中 |
| 基础镜像 | 具体版本+安全更新 | 不使用latest |
| 漏洞扫描 | 每次构建自动扫描 | Trivy/Snyk |
| 日志 | 不包含敏感信息 | 脱敏处理 |

## 六、故障排查速查

### 6.1 容器启动失败
```bash
# 查看容器日志
docker logs -f <container_name> --tail 100

# 查看容器详细信息
docker inspect <container_name>

# 查看容器状态
docker ps -a | grep <container_name>

# 进入容器排查
docker exec -it <container_name> /bin/sh

# 检查端口占用
lsof -i :<port>
netstat -tlnp | grep <port>
```

### 6.2 网络问题排查
```bash
# 查看Docker网络
docker network ls
docker network inspect <network_name>

# 检查容器IP
docker inspect <container_name> --format='{{.NetworkSettings.IPAddress}}'

# 测试容器间通信
docker exec <container1> ping <container2>

# 检查端口映射
docker port <container_name>
```

### 6.3 性能问题排查
```bash
# 查看容器资源使用
docker stats

# 查看容器进程
docker top <container_name>

# 查看容器磁盘使用
docker system df
docker volume ls
```
