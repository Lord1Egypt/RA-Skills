# Deployment Kit Skill

**version**: 0.1.0

OpenClaw 生产部署套件 - Docker + CI/CD + 健康检查

## 功能特性

- **Docker 容器化**: 多阶段构建，优化镜像大小
- **Docker Compose**: 一键启动完整服务栈
- **CI/CD 流水线**: GitHub Actions 自动构建、测试、部署
- **健康检查**: 网关、磁盘、内存、日志监控
- **安全扫描**: Trivy 漏洞扫描

## 快速开始

### 1. Docker 部署

```bash
cd skills/deployment-kit

# 构建镜像
npm run docker:build

# 运行容器
npm run docker:run

# 查看日志
docker logs -f openclaw
```

### 2. Docker Compose 部署

```bash
cd docker

# 启动所有服务
docker-compose up -d

# 查看状态
docker-compose ps

# 查看日志
docker-compose logs -f openclaw
```

### 3. 健康检查

```bash
# 本地检查
npm run health:check

# 或直接使用脚本
node scripts/health-check.js
```

## 目录结构

```
deployment-kit/
├── docker/
│   ├── Dockerfile          # 多阶段构建
│   └── docker-compose.yml  # 完整服务栈
├── .github/workflows/
│   └── ci-cd.yml          # GitHub Actions
├── scripts/
│   └── health-check.js    # 健康检查
└── package.json
```

## CI/CD 流水线

### 工作流阶段

1. **Lint**: 代码风格检查
2. **Test**: 多版本 Node.js 测试
3. **Build**: 构建 Docker 镜像
4. **Security**: Trivy 安全扫描
5. **Deploy**: 自动部署到 staging/production

### 触发条件

- **Push to develop**: 部署到测试环境
- **Push to main**: 部署到生产环境
- **Release published**: 构建版本镜像

## 健康检查

### 检查项

| 检查项 | 说明 | 阈值 |
|--------|------|------|
| Gateway | 网关 HTTP 响应 | 200 OK |
| Disk Space | 磁盘使用率 | Warning: 80%, Critical: 90% |
| Memory | 内存使用率 | Warning: 80%, Critical: 90% |
| Logs | 近期错误数 | Warning: >10 错误 |

### 使用示例

```javascript
import { runHealthChecks } from './scripts/health-check.js';

const result = await runHealthChecks();
console.log(result);
// {
//   gateway: { status: 'ok' },
//   disk: { status: 'ok', usage: '45%' },
//   memory: { status: 'ok', usage: '60%' },
//   logs: { status: 'ok', recentErrors: 0 }
// }
```

## Docker 镜像

### 构建参数

```dockerfile
# 基础镜像
FROM node:20-alpine

# 非 root 用户
USER openclaw

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:18789/health || exit 1
```

### 镜像特性

- ✅ 多阶段构建（优化大小）
- ✅ 非 root 用户运行（安全）
- ✅ 时区设置（Asia/Shanghai）
- ✅ 健康检查（自动重启）
- ✅ 数据持久化（Volumes）

## 配置

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| NODE_ENV | 运行环境 | production |
| TZ | 时区 | Asia/Shanghai |
| OPENCLAW_CONFIG | 配置文件路径 | /app/config/openclaw.json |

### 端口映射

| 端口 | 服务 | 说明 |
|------|------|------|
| 18789 | OpenClaw Gateway | 主服务端口 |
| 9090 | Prometheus | 监控（可选） |
| 3100 | Loki | 日志（可选） |

## 监控（可选）

### Prometheus + Grafana

```yaml
# docker-compose.yml 已包含
services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
  
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
```

## 注意事项

1. **首次运行**: 需要配置 OPENAI_API_KEY 等环境变量
2. **数据持久化**: 使用 Docker Volumes 保存数据
3. **日志管理**: 定期清理日志文件，避免磁盘满
4. **安全**: 生产环境使用 HTTPS，配置防火墙

## License

MIT
