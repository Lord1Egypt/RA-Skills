# Service Development Guide

Step-by-step guide for creating new services in Teamgram Server.

## 1. Service Structure Template

```
app/service/<service-name>/
├── cmd/
│   └── <service-name>/
│       └── main.go
├── etc/
│   └── <service-name>.yaml
├── internal/
│   ├── config/
│   │   └── config.go
│   ├── core/
│   │   ├── <feature>_logic.go
│   │   └── core.go
│   ├── dao/
│   │   └── dao.go
│   ├── server/
│   │   └── server.go
│   └── svc/
│       └── service_context.go
├── <service-name>.go
├── helper.go
└── client/
    └── client.go
```

## 2. Main Entry Point (cmd/main.go)

```go
package main

import (
    "flag"
    
    "github.com/teamgram/teamgram-server/app/service/<service-name>/internal/config"
    "github.com/teamgram/teamgram-server/app/service/<service-name>/internal/server"
    "github.com/teamgram/teamgram-server/app/service/<service-name>/internal/svc"
    
    "github.com/zeromicro/go-zero/core/conf"
    "github.com/zeromicro/go-zero/core/service"
    "github.com/zeromicro/go-zero/zrpc"
)

var configFile = flag.String("f", "etc/<service-name>.yaml", "the config file")

func main() {
    flag.Parse()
    
    var c config.Config
    // 加载配置，失败则退出
    if err := conf.Load(*configFile, &c); err != nil {
        log.Fatalf("failed to load config: %v", err)
    }
    
    // 创建服务上下文
    ctx, err := svc.NewServiceContext(c)
    if err != nil {
        log.Fatalf("failed to create service context: %v", err)
    }
    
    // 创建gRPC服务器
    s, err := zrpc.NewServer(c.RpcServerConf, func(grpcServer *grpc.Server) {
        server.Register(grpcServer, ctx)
    })
    if err != nil {
        log.Fatalf("failed to create server: %v", err)
    }
    
    defer s.Stop()
    
    serviceGroup := service.NewServiceGroup()
    serviceGroup.Add(s)
    
    // Add other services (cron jobs, consumers, etc.)
    
    serviceGroup.Start()
}
```

## 3. Configuration (etc/config.yaml)

```yaml
Name: <service-name>
Host: 0.0.0.0
Port: <port>

RpcServerConf:
  ServiceConf:
    Log:
      Mode: console
      Path: logs
      Level: info
  ListenOn: 0.0.0.0:<port>
  Etcd:
    Hosts:
      - localhost:2379
    Key: <service-name>

MySQL:
  DataSource: user:password@tcp(localhost:3306)/teamgram?charset=utf8mb4

Redis:
  Host: localhost:6379
  Type: node

Kafka:
  Brokers:
    - localhost:9092
```

## 4. Config Structures (internal/config/config.go)

```go
package config

import (
    "github.com/zeromicro/go-zero/rest"
    "github.com/zeromicro/go-zero/zrpc"
)

type Config struct {
    rest.RestConf
    RpcServerConf zrpc.RpcServerConf
    
    MySQL struct {
        DataSource string
    }
    
    Redis struct {
        Host string
        Type string
    }
    
    Kafka struct {
        Brokers []string
    }
    
    // Service-specific config
    FeatureFlag bool
    BatchSize   int
}
```

## 5. Service Context (internal/svc/service_context.go)

```go
package svc

import (
    "github.com/teamgram/teamgram-server/app/service/<service-name>/internal/config"
    "github.com/teamgram/teamgram-server/app/service/<service-name>/internal/dao"
    
    "github.com/zeromicro/go-zero/core/stores/redis"
    "github.com/zeromicro/go-zero/core/stores/sqlx"
)

type ServiceContext struct {
    Config config.Config
    
    // DAO layer
    DAO *dao.DAO
    
    // External service clients
    UserClient     *userclient.UserClient
    MessageClient  *messageclient.MessageClient
    
    // Cache
    Redis *redis.Redis
}

func NewServiceContext(c config.Config) *ServiceContext {
    conn := sqlx.NewMysql(c.MySQL.DataSource)
    
    return &ServiceContext{
        Config: c,
        DAO:    dao.NewDAO(conn),
        Redis:  redis.MustNewRedis(c.Redis),
    }
}
```

## 6. DAO Layer (internal/dao/dao.go)

```go
package dao

import (
    "context"
    
    "github.com/zeromicro/go-zero/core/stores/sqlx"
)

type DAO struct {
    db sqlx.SqlConn
}

func NewDAO(conn sqlx.SqlConn) *DAO {
    return &DAO{db: conn}
}

// Example query
func (d *DAO) GetByID(ctx context.Context, id int64) (*Model, error) {
    var m Model
    query := `SELECT * FROM table_name WHERE id = ?`
    err := d.db.QueryRowCtx(ctx, &m, query, id)
    return &m, err
}

func (d *DAO) Insert(ctx context.Context, m *Model) (int64, error) {
    query := `INSERT INTO table_name (col1, col2) VALUES (?, ?)`
    result, err := d.db.ExecCtx(ctx, query, m.Col1, m.Col2)
    if err != nil {
        return 0, err
    }
    return result.LastInsertId()
}
```

## 7. Business Logic (internal/core/core.go)

```go
package core

import (
    "context"
    
    "github.com/teamgram/teamgram-server/app/service/<service-name>/internal/svc"
)

type Core struct {
    svcCtx *svc.ServiceContext
}

func NewCore(svcCtx *svc.ServiceContext) *Core {
    return &Core{svcCtx: svcCtx}
}

func (c *Core) ProcessRequest(ctx context.Context, req *Request) (*Response, error) {
    // 1. Validate input
    if err := c.validate(req); err != nil {
        return nil, err
    }
    
    // 2. Check cache
    cached, err := c.svcCtx.Redis.Get(...)
    if err == nil {
        return cached, nil
    }
    
    // 3. Query database
    data, err := c.svcCtx.DAO.GetByID(ctx, req.ID)
    if err != nil {
        return nil, err
    }
    
    // 4. Process business logic
    result := c.process(data)
    
    // 5. Cache result
    c.svcCtx.Redis.Set(...)
    
    return result, nil
}
```

## 8. Server Handlers (internal/server/server.go)

```go
package server

import (
    "context"
    
    "github.com/teamgram/teamgram-server/app/service/<service-name>/internal/core"
    "github.com/teamgram/teamgram-server/app/service/<service-name>/internal/svc"
    
    "google.golang.org/grpc"
)

type Server struct {
    core *core.Core
}

func Register(grpcServer *grpc.Server, svcCtx *svc.ServiceContext) {
    s := &Server{core: core.NewCore(svcCtx)}
    RegisterRPCServer(grpcServer, s)
}

func (s *Server) MethodName(ctx context.Context, req *RPCRequest) (*RPCResponse, error) {
    // Convert request
    coreReq := convertRequest(req)
    
    // Call core logic
    result, err := s.core.ProcessRequest(ctx, coreReq)
    if err != nil {
        return nil, err
    }
    
    // Convert response
    return convertResponse(result), nil
}
```

## 9. Makefile Integration

Add to root Makefile:

```makefile
# Service-specific build
build-<service-name>:
	go build -o bin/<service-name> app/service/<service-name>/cmd/<service-name>/main.go

# Service-specific run
run-<service-name>:
	go run app/service/<service-name>/cmd/<service-name>/main.go -f app/service/<service-name>/etc/<service-name>.yaml
```

## 10. Testing

```go
package core_test

import (
    "context"
    "testing"
    
    "github.com/stretchr/testify/assert"
    "github.com/teamgram/teamgram-server/app/service/<service-name>/internal/core"
    "github.com/teamgram/teamgram-server/app/service/<service-name>/internal/svc"
)

func TestProcessRequest(t *testing.T) {
    // Setup
    cfg := config.Config{...}
    svcCtx := svc.NewServiceContext(cfg)
    c := core.NewCore(svcCtx)
    
    // Test case
    req := &Request{ID: 123}
    resp, err := c.ProcessRequest(context.Background(), req)
    
    // Assert
    assert.NoError(t, err)
    assert.NotNil(t, resp)
    assert.Equal(t, expected, resp.Data)
}
```

## Common Patterns

### Caching Pattern

```go
func (c *Core) GetWithCache(ctx context.Context, key string) (*Data, error) {
    // Try cache
    cacheKey := fmt.Sprintf("cache:%s", key)
    cached, err := c.svcCtx.Redis.Get(cacheKey)
    if err == nil {
        var data Data
        json.Unmarshal([]byte(cached), &data)
        return &data, nil
    }
    
    // Cache miss - query DB
    data, err := c.svcCtx.DAO.Get(ctx, key)
    if err != nil {
        return nil, err
    }
    
    // Update cache
    bytes, _ := json.Marshal(data)
    c.svcCtx.Redis.Set(cacheKey, string(bytes), 3600) // 1 hour TTL
    
    return data, nil
}
```

### Transaction Pattern

```go
func (c *Core) Transfer(ctx context.Context, from, to int64, amount int) error {
    return c.svcCtx.DAO.Transaction(func(tx *sql.Tx) error {
        // Deduct from source
        if err := c.svcCtx.DAO.DeductTx(tx, from, amount); err != nil {
            return err
        }
        
        // Add to destination
        if err := c.svcCtx.DAO.AddTx(tx, to, amount); err != nil {
            return err
        }
        
        // Record transaction
        return c.svcCtx.DAO.RecordTx(tx, from, to, amount)
    })
}
```

### Event Publishing

```go
func (c *Core) CreateEvent(ctx context.Context, data *Data) error {
    // Persist
    id, err := c.svcCtx.DAO.Insert(ctx, data)
    if err != nil {
        return err
    }
    
    // Publish event
    event := &Event{
        Type: "created",
        ID:   id,
        Data: data,
    }
    
    return c.svcCtx.Kafka.Publish("events", event)
}
```
