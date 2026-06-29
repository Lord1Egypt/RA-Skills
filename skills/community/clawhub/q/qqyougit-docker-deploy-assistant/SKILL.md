---
name: docker-deploy-assistant
version: 1.3.0
description: |
  「在我电脑上明明能跑」——因为少了Docker。帮你写Dockerfile、构建镜像、配置多环境、编排docker-compose，从本地开发到服务器部署一条龙。支持Node.js/Python/Go/Java/前端全栈，覆盖CI/CD集成、安全加固、监控告警，告别环境不一致的噩梦。
  触发词：Docker部署、容器化、镜像构建、Dockerfile编写、写Docker、docker-compose编排、部署到服务器、Docker配置、Docker镜像优化、多阶段构建、Docker网络、Docker数据卷、Docker环境变量、Docker健康检查、Docker安全、容器报错排查、docker build失败、容器启动失败、Docker端口映射、Docker日志查看、Docker镜像瘦身、Dockerfile最佳实践、Docker compose up、容器编排、Docker Registry、Docker Swarm、Docker网络配置、Docker volume、Docker日志收集、Dockerfile模板、容器部署、一键部署Docker、Docker生产环境、Docker开发环境、docker镜像推送、Dockerfile多阶段、docker容器通信、Docker CI/CD、Docker自动化部署、docker镜像仓库、Docker容器监控、Docker entrypoint、docker CMD vs ENTRYPOINT、docker run参数、docker compose网络、docker secrets、docker容器资源限制、containerize、dockerize、docker deployment、Docker故障排查、Docker错误修复、Docker环境配置、Docker开发环境搭建、Docker生产环境配置、Docker一键部署、docker pull/push、Docker镜像管理、Docker容器管理
  排除：Kubernetes/K8s编排、本地开发调试（非容器化）、虚拟机管理
---

# Docker部署助手 🐳

> 「在我电脑上明明能跑」——因为少了Docker。让你的应用在任何环境都能稳定运行。

## 触发条件

### ✅ 匹配关键词（满足任一即触发）

| 类别 | 关键词 |
|------|--------|
| 通用 | Docker / 容器 / 镜像 / 容器化 / dockerize / containerize |
| 文件 | Dockerfile / docker-compose / .dockerignore / docker-entrypoint.sh |
| 动作 | 部署 / 打包 / 构建镜像 / 推送到仓库 / 上线 / 一键部署 |
| 编排 | docker-compose / 编排 / 多容器 / 服务编排 / 容器间通信 |
| 排查 | 容器报错 / 启动失败 / 端口冲突 / 镜像太大 / 构建失败 / 报错排查 |
| 优化 | 多阶段构建 / 镜像瘦身 / 安全加固 / Alpine / distroless |
| 配置 | 端口映射 / 环境变量 / 数据持久化 / 网络配置 / 健康检查 |
| CI/CD | Docker+CI / 自动构建 / 自动部署 / GitHub Actions / GitLab CI |
| 英文 | docker deployment / containerize / docker build / docker compose / dockerfile / container orchestration |
| 场景 | 开发环境容器化 / 生产环境部署 / 多环境配置 / 本地模拟生产 |

### ❌ 排除关键词（明确不触发）
- Kubernetes / K8s / Helm → 用K8s专用工具
- 虚拟机 / VMware / VirtualBox → 拒绝
- 本地开发调试（非容器化问题）→ 直接回答
- Docker Desktop安装问题 → 推荐官方文档

### 🎯 上下文条件
- 用户提到技术栈（Node/Python/Go/Java/前端） → 使用对应模板
- 用户提供报错信息 → 快速定位并修复
- 用户说"生产环境" → 启用安全加固+健康检查+日志
- 用户说"多阶段构建" → 提供完整多阶段模板

## 核心流程（9 Steps）

### Step 1: 环境诊断与需求确认
- 确认应用类型：Node.js / Python / Go / Java / PHP / 静态前端 / 多语言混合
- 确认框架版本：运行时版本 / 包管理器 / 构建工具
- 确认依赖服务：数据库(PostgreSQL/MySQL/MongoDB) / 缓存(Redis) / 消息队列(RabbitMQ/Kafka) / 对象存储
- 确认部署目标：本地开发 / 测试环境 / 预发布 / 生产环境 / 多云
- 确认资源限制：CPU核心数 / 内存大小 / 磁盘需求 / 网络带宽
- 确认特殊需求：GPU支持 / 大文件处理 / WebSocket / 长连接

### Step 2: Dockerfile编写与优化
- 选择最优基础镜像（Alpine优先，考虑体积和安全）
- 设置工作目录、创建非root用户（安全最佳实践）
- 分层复制：先复制依赖文件（利用缓存）→ 安装依赖 → 复制源码
- 配置环境变量（NODE_ENV / PYTHONUNBUFFERED等）
- 暴露端口（EXPOSE）
- 设置启动命令（CMD vs ENTRYPOINT选择）
- 添加HEALTHCHECK指令（生产环境必选）
- 配置.dockerignore减少构建上下文

### Step 3: 多阶段构建优化
- **阶段1-构建阶段**：安装构建工具、编译代码、运行测试
- **阶段2-依赖阶段**：仅安装生产依赖
- **阶段3-运行阶段**：使用最小基础镜像（alpine/distroless/scratch），仅复制必要产物
- 最终镜像瘦身：去除构建工具 / 源码 / 文档 / 测试文件
- 多架构支持：amd64/arm64双架构构建（使用 docker buildx）

### Step 4: docker-compose编排
- 定义服务拓扑：app / database / cache / nginx / worker / celery
- 配置端口映射（对外端口:容器端口）和内部网络
- 配置数据卷（命名卷/绑定挂载）及数据备份策略
- 配置环境变量（.env文件 + 变量替换）
- 配置服务依赖和健康检查顺序（depends_on + condition）
- 配置重启策略（unless-stopped / always / on-failure）
- 配置资源限制（memory / cpus）
- 配置日志驱动和轮转（json-file / fluentd）

### Step 5: 安全加固
- 非root用户运行（创建专用用户组和用户）
- 只读文件系统（关键目录可写）
- 敏感信息管理（Docker Secrets / 外部密钥管理Vault）
- 镜像漏洞扫描（Trivy / Snyk / Clair）
- 网络隔离（仅暴露必要端口、内部网络隔离）
- 基础镜像定期更新（使用版本锁定，不使用latest）
- 限制容器capabilities（--cap-drop=ALL --add-cap=）
- 不在镜像中存储 secrets（运行时注入）

### Step 6: 数据持久化策略
- 命名卷（named volumes）：数据库数据、日志、可更新配置
- 绑定挂载（bind mounts）：源代码（开发环境）、配置（生产环境）
- tmpfs挂载：敏感数据、临时文件
- 数据备份策略：定时备份到对象存储
- 数据迁移方案：volume backup/restore脚本

### Step 7: CI/CD集成（可选）
- **GitHub Actions**：
  - 自动构建：代码推送触发镜像构建
  - 多平台构建：matrix strategy for multiple architectures
  - 自动测试：构建后运行容器测试（集成测试/健康检查）
  - 自动推送：推送到Docker Hub / ECR / ACR / 私有仓库
  - 自动部署：SSH到服务器拉取并重启（docker-compose pull && up -d）
- **GitLab CI**：
  - 使用GitLab Container Registry
  - Auto DevOps配置
- **Jenkins**：
  - Pipeline as Code
  - Blue-Green部署

### Step 8: 监控与运维
- **日志收集**：JSON日志格式 + 日志轮转（max-size + max-file）
- **健康检查**：HTTP探针（推荐）/ TCP探针 / exec探针
- **资源监控**：CPU / 内存 / 网络 / 磁盘使用率
- **告警配置**：异常时通知（邮件 / 钉钉 / Slack / 企业微信 / Prometheus Alertmanager）
- **备份策略**：数据卷定时备份到S3/OSS/MinIO
- **回滚方案**：版本标签管理 + 快速回退脚本

### Step 9: 生产环境 Checklist
- [ ] 基础镜像使用具体版本（非latest）
- [ ] 非root用户运行
- [ ] 添加HEALTHCHECK
- [ ] 配置日志轮转
- [ ] 设置资源限制（memory/cpus）
- [ ] 镜像漏洞扫描通过
- [ ] 敏感信息使用环境变量或Secrets
- [ ] 数据卷持久化配置
- [ ] 备份策略已配置
- [ ] 回滚脚本已准备

## 输出模板

**Dockerfile 模板：**
```dockerfile
# ============================================
# 多阶段构建 Dockerfile
# ============================================

# ===== 阶段1：依赖安装 =====
FROM node:18-alpine AS deps
WORKDIR /app
# 先复制依赖文件，利用Docker缓存
COPY package*.json ./
RUN npm ci --only=production

# ===== 阶段2：构建 =====
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# ===== 阶段3：生产运行 =====
FROM node:18-alpine AS runner
WORKDIR /app

# 环境配置
ENV NODE_ENV=production
ENV PORT=3000

# 安全：创建非root用户
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 --ingroup nodejs appuser

# 复制依赖（来自deps阶段）
COPY --from=deps --chown=appuser:nodejs /app/node_modules ./node_modules

# 复制构建产物（来自builder阶段）
COPY --from=builder --chown=appuser:nodejs /app/dist ./dist

# 切换到非root用户
USER appuser

# 暴露端口
EXPOSE 3000

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget -qO- http://localhost:3000/health || exit 1

# 启动命令
CMD ["node", "dist/index.js"]
```

**docker-compose.yml 模板：**
```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
      args:
        NODE_ENV: production
    image: myapp:${TAG:-latest}
    container_name: myapp
    restart: unless-stopped
    ports:
      - "${APP_PORT:-3000}:3000"
    environment:
      - NODE_ENV=production
      - DB_HOST=postgres
      - DB_PORT=5432
      - DB_NAME=${DB_NAME}
      - DB_USER=${DB_USER}
      - DB_PASSWORD=${DB_PASSWORD}
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    env_file:
      - .env
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_started
    volumes:
      - app-data:/app/data
      - ./logs:/app/logs
    networks:
      - backend
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '1.0'
        reservations:
          memory: 256M
          cpus: '0.5'
    logging:
      driver: json-file
      options:
        max-size: '10m'
        max-file: '3'

  postgres:
    image: postgres:15-alpine
    restart: unless-stopped
    container_name: postgres
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_INITDB_ARGS: '--encoding=UTF8'
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql:ro
    networks:
      - backend
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '1.0'

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    container_name: redis
    command: >
      redis-server
      --appendonly yes
      --requirepass ${REDIS_PASSWORD}
      --maxmemory 256mb
      --maxmemory-policy allkeys-lru
    volumes:
      - redis-data:/data
    networks:
      - backend
    healthcheck:
      test: ["CMD", "redis-cli", "-a", "${REDIS_PASSWORD}", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5

  nginx:
    image: nginx:alpine
    restart: unless-stopped
    container_name: nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/conf.d:/etc/nginx/conf.d:ro
      - ./certbot/conf:/etc/letsencrypt:ro
      - ./certbot/www:/var/www/certbot:ro
      - nginx-cache:/var/cache/nginx
      - nginx-run:/var/run
    depends_on:
      - app
    networks:
      - backend
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost/health"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  app-data:
  postgres-data:
  redis-data:
  nginx-cache:
  nginx-run:

networks:
  backend:
    driver: bridge
```

## 常见问题速查

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| 端口被占用 | 宿主机端口冲突 | 修改映射端口或停掉占用进程 |
| 权限拒绝 | root运行+文件权限 | 创建非root用户，chown文件 |
| 镜像太大 | 包含构建工具/源码/文档 | 使用多阶段构建+Alpine镜像 |
| 构建缓存失效 | COPY顺序不对 | 先复制package.json，后复制源码 |
| 容器内连不上DB | 网络不通/主机名错误 | 使用docker-compose服务名代替localhost |
| 环境变量未生效 | .env文件路径错误/格式错误 | 检查env_file路径和变量名格式 |
| 容器不断重启 | 启动命令报错 | `docker logs <container>` 查看日志 |
| 磁盘空间不足 | 镜像/容器/构建缓存堆积 | `docker system prune` 清理 |
| 容器内中文乱码 | 字符集未设置 | 添加 ENV LANG=C.UTF-8 |
| 文件权限错误 | UID/GID不一致 | 使用 `--chown` 参数指定所有者 |
| 内存溢出(OOM) | 应用内存泄漏或限制太小 | 添加 memory limit 或检查应用 |
| 构建超时 | 网络慢或依赖太多 | 换国内镜像源或增加 timeout |
| Pull镜像失败 | 网络问题或镜像不存在 | 检查镜像名/换镜像源/配置代理 |

## 边界约束

1. **多架构支持**：如需amd64/arm64双架构，使用 `docker buildx`
2. **敏感信息**：禁止在Dockerfile中硬编码密钥，使用环境变量或Docker Secrets
3. **镜像大小**：优先使用Alpine镜像，Go应用目标<50MB，Node应用<200MB
4. **安全**：禁止以root用户运行容器，必须创建专用用户
5. **健康检查**：生产环境必须添加HEALTHCHECK
6. **版本锁定**：基础镜像必须指定具体版本号，禁止用latest
7. **日志管理**：配置日志轮转（max-size+max-file），防止磁盘爆满
8. **资源限制**：生产环境必须设置memory/CPUs限制
9. **数据持久化**：数据库等有状态服务必须使用命名卷

## Output Language
中文输出
