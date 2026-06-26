---
name: teamgram-server-architecture
description: Teamgram Server architecture guide for building Telegram-compatible backends. Use when designing service topology, implementing MTProto services, or self-hosting Teamgram. Covers service拆分, data flow, deployment patterns, and development workflows based on the official teamgram/teamgram-server repository.
version: 1.0.1
---

# Teamgram Server Architecture

Complete architecture guide based on the official teamgram/teamgram-server repository.

⚠️ **免责声明与安全提示**

> 本技能基于对开源项目 `teamgram/teamgram-server` 的分析整理，仅供学习参考。
> 
> **重要提示**:
> - 内容可能随官方仓库更新而过时，请以官方最新版本为准
> - 生产环境使用前请自行验证所有配置和代码
> - 部署配置中的密码、密钥等必须使用强密码并通过安全方式注入
> - 建议直接参考官方文档: https://github.com/teamgram/teamgram-server
> - 生产环境部署前请进行安全审计和渗透测试

---

## Overview

Teamgram Server is an unofficial open-source MTProto server implementation in Go, compatible with Telegram clients and supporting self-hosted deployment.

**API Layer**: 223 (截至技能创建时，请以官方仓库最新版本为准)  
**MTProto Versions**: Abridged, Intermediate, Padded intermediate, Full

## Core Features

- ✅ **Private Chat** - End-to-end encrypted messaging
- ✅ **Basic Group** - Small group chats (up to 200 members)
- ⚠️ **Super Group** - Large groups (requires additional implementation)
- ✅ **Contacts** - Contact management and sync
- ✅ **Web** - Web client support

## Service Architecture

### High-Level Topology

```
                    ┌─────────────────┐
                    │   Load Balancer │
                    │    (Nginx/HA)   │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼───────┐   ┌────────▼────────┐   ┌──────▼──────┐
│   gnetway     │   │   httpserver    │   │   session   │
│  (TCP/MTProto)│   │   (HTTP API)    │   │ (WebSocket) │
└───────┬───────┘   └────────┬────────┘   └──────┬──────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                    ┌────────▼────────┐
                    │   BFF Layer     │
                    │ (Business Logic)│
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
┌───────▼───────┐   ┌────────▼────────┐   ┌──────▼──────┐
│   Service     │   │    Service      │   │   Service   │
│   Layer       │   │    Layer        │   │   Layer     │
└───────────────┘   └─────────────────┘   └─────────────┘
```

### Interface Layer (app/interface)

| Service | Protocol | Purpose |
|---------|----------|---------|
| **gnetway** | TCP/MTProto | Main client gateway, handles MTProto encryption |
| **httpserver** | HTTP/REST | Bot API and webhooks |
| **session** | WebSocket | Web client connections |

### BFF Layer (app/bff)

Backend-for-Frontend aggregation layer:
- Aggregates multiple service calls
- Handles client-specific logic
- Reduces client-side complexity

### Service Layer (app/service)

| Service | Responsibility | Key Features |
|---------|----------------|--------------|
| **authsession** | Authentication & Session | Auth key management, session validation |
| **biz** | Core Business Logic | Chat, message, user, dialog, updates |
| **dfs** | Distributed File Storage | File upload/download, MinIO integration |
| **geoip** | Geo-location | IP geolocation for security |
| **idgen** | ID Generation | Snowflake-style distributed IDs |
| **media** | Media Processing | Thumbnail generation, FFmpeg integration |
| **status** | Online Status | User presence, last seen |

### Messenger Layer (app/messenger)

| Service | Purpose |
|---------|---------|
| **msg** | Message routing and delivery |
| **sync** | Multi-device synchronization |

## Biz Service Breakdown

The `biz` service is a monolithic business logic container:

```
app/service/biz/
├── biz/        # Core business operations
├── chat/       # Group/channel management
├── code/       # Verification codes (SMS/email)
├── dialog/     # Conversation management
├── message/    # Message storage and retrieval
├── updates/    # Real-time updates push
└── user/       # User profiles and settings
```

### Recommended Refactoring

For large-scale deployments, split `biz` into:

```
chat-service/      - Group & channel management
message-service/   - Message CRUD and search
user-service/      - User profiles and contacts
notification-service/ - Push notifications
```

## Data Flow

### Message Sending Flow

```
Client → gnetway → session → msg → message (biz)
                                           ↓
                                    MySQL (persist)
                                           ↓
                                    Kafka (broadcast)
                                           ↓
                              sync → updates → Client
```

### Authentication Flow

```
Client → gnetway → authsession
                        ↓
                   MySQL (auth_keys)
                        ↓
                   Redis (sessions)
```

### File Upload Flow

```
Client → gnetway → dfs → MinIO
                  ↓
               MySQL (file_metadata)
```

## Infrastructure Dependencies

| Component | Purpose | Required |
|-----------|---------|----------|
| **MySQL 5.7+** | Primary data store | ✅ Yes |
| **Redis** | Cache, sessions, deduplication | ✅ Yes |
| **etcd** | Service discovery & config | ✅ Yes |
| **Kafka** | Message pipeline, events | ✅ Yes |
| **MinIO** | Object storage | ✅ Yes |
| **FFmpeg** | Media transcoding | ⚠️ Optional |

## Project Structure

```
teamgram-server/
├── app/
│   ├── bff/              # Backend-for-Frontend
│   ├── interface/        # Gateway layer
│   │   ├── gnetway/      # MTProto gateway
│   │   ├── httpserver/   # HTTP API
│   │   └── session/      # WebSocket session
│   ├── messenger/        # Message routing
│   │   ├── msg/          # Message service
│   │   └── sync/         # Sync service
│   └── service/          # Core services
│       ├── authsession/  # Auth & session
│       ├── biz/          # Business logic
│       ├── dfs/          # File storage
│       ├── geoip/        # Geo location
│       ├── idgen/        # ID generator
│       ├── media/        # Media processing
│       └── status/       # Online status
├── pkg/                  # Shared packages
│   ├── code/             # Error codes
│   ├── conf/             # Configuration
│   ├── net2/             # Network utilities
│   └── ...
├── clients/              # Client SDKs
├── data/                 # SQL schemas
├── docs/                 # Documentation
└── specs/                # Architecture specs
```

## Development Workflow

### 1. Code Generation

Teamgram uses TL (Type Language) schema:

```bash
# Generate Go code from TL schema
make generate
# or
dalgenall.sh
```

### 2. Database Migration

```bash
# Initialize database
mysql -u root -p < data/teamgram.sql

# Run migrations
make migrate
```

### 3. Service Development Pattern

Each service follows this structure:

```
app/service/<name>/
├── cmd/              # Entry point
├── etc/              # Configuration
├── internal/
│   ├── config/       # Config structures
│   ├── core/         # Business logic
│   ├── dao/          # Data access
│   ├── server/       # gRPC/HTTP handlers
│   └── svc/          # Service context
└── <name>.go         # Main service file
```

### 4. Adding New RPC

1. Define in TL schema (`specs/mtproto.tl`)
2. Run code generation
3. Implement handler in `internal/core/`
4. Register in `internal/server/`
5. Update client SDKs

## Configuration

### Service Configuration (YAML)

```yaml
# app/service/biz/etc/biz.yaml
Name: biz
Host: 0.0.0.0
Port: 20001

MySQL:
  DataSource: user:password@tcp(localhost:3306)/teamgram?charset=utf8mb4

Redis:
  Host: localhost:6379

Etcd:
  Hosts:
    - localhost:2379
  Key: biz
```

### Environment Variables

```bash
# .env file
MYSQL_DATA_SOURCE=user:password@tcp(localhost:3306)/teamgram
REDIS_HOST=localhost:6379
ETCD_ENDPOINTS=localhost:2379
KAFKA_BROKERS=localhost:9092
MINIO_ENDPOINT=localhost:9000
```

## Deployment Patterns

### Docker Compose (Development)

```bash
docker-compose up -d
```

### Kubernetes (Production)

```yaml
# Example deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: teamgram-biz
spec:
  replicas: 3
  selector:
    matchLabels:
      app: teamgram-biz
  template:
    spec:
      containers:
      - name: biz
        image: teamgram/biz:latest
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
```

## Scaling Considerations

### Horizontal Scaling

- **Stateless services**: biz, httpserver, dfs (easy to scale)
- **Stateful services**: gnetway (connection-based), session (session affinity)
- **Database**: MySQL read replicas, Redis Cluster

### Vertical Scaling

- **Media service**: CPU-intensive (FFmpeg)
- **Message service**: Memory-intensive (caching)
- **Auth service**: Low resource usage

## Security Best Practices

1. **Network Isolation**
   - Internal services behind VPC
   - Only gnetway/httpserver exposed publicly

2. **Encryption**
   - MTProto end-to-end encryption
   - TLS for HTTP/WebSocket
   - mTLS between services (optional)

3. **Authentication**
   - Auth keys in secure storage
   - Session tokens with expiration
   - Rate limiting per user/IP

4. **Data Protection**
   - Database encryption at rest
   - MinIO bucket encryption
   - Backup encryption

## Monitoring

### Metrics

```
- Request rate per service
- Response latency (p50, p95, p99)
- Error rates
- Active connections
- Message throughput
```

### Logging

```go
// Structured logging
log.Info().
    Str("service", "biz").
    Str("method", "messages.sendMessage").
    Int64("user_id", userID).
    Int64("msg_id", msgID).
    Dur("latency", duration).
    Msg("request processed")
```

## References

- [Architecture DeepWiki](https://deepwiki.com/teamgram/teamgram-server)
- [Service Topology](specs/architecture.md)
- [Dependencies](specs/dependencies-and-runtime.md)
- [Official Repository](https://github.com/teamgram/teamgram-server)

## See Also

- [references/service-development.md](references/service-development.md) - Step-by-step service creation
- [references/deployment.md](references/deployment.md) - Production deployment guide
- [references/tuning.md](references/tuning.md) - Performance optimization
