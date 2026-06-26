---
name: teamgram-rpc-development
description: Complete guide for developing RPC services in Teamgram Server (v2.0.0). Use when creating new RPC methods, implementing business logic, or extending Teamgram functionality. Covers TL schema, DAO/Core/Server layers, error handling, performance optimization, security, testing, observability, and production best practices.
version: 2.0.0
---

# Teamgram RPC Development Guide v2.0.0

Complete guide for developing RPC services in Teamgram Server.

> 📚 **十次版本迭代优化** (v1.0.0 → v2.0.0)
> 
> 本技能经过十次迭代完善，涵盖从基础开发到生产部署的完整知识体系。

## 版本迭代历程

| 版本 | 主题 | 文档 |
|------|------|------|
| v1.0.0 | 基础开发 | 本指南 |
| v1.1.0 | 错误处理与日志 | [查看](references/v1.1.0-error-handling.md) |
| v1.2.0 | 性能优化与缓存 | [查看](references/v1.2.0-performance.md) |
| v1.3.0 | 安全最佳实践 | [查看](references/v1.3.0-security.md) |
| v1.4.0 | 测试策略 | [查看](references/v1.4.0-testing.md) |
| v1.5.0 | 可观测性 | [查看](references/v1.5.0-observability.md) |
| v1.6.0 | 数据库优化 | [查看](references/v1.6.0-database.md) |
| v1.7.0 | 消息队列 | [查看](references/v1.7.0-queue.md) |
| v1.8.0 | 熔断限流 | [查看](references/v1.8.0-circuit-breaker.md) |
| v1.9.0 | 多租户 | [查看](references/v1.9.0-multi-tenant.md) |
| v2.0.0 | 完整总结 | [查看](references/v2.0.0-final.md) |

## 快速导航

**新手指南**: 从 [Development Workflow](#development-workflow) 开始

**生产优化**: 查看 [v1.2.0性能优化](references/v1.2.0-performance.md) 和 [v1.3.0安全](references/v1.3.0-security.md)

**问题排查**: 参考 [v1.1.0错误处理](references/v1.1.0-error-handling.md) 和 [v1.5.0可观测性](references/v1.5.0-observability.md)

## Overview

Teamgram uses gRPC for inter-service communication and MTProto for client-server communication. This guide covers both.

## RPC Types

### 1. Internal RPC (Service-to-Service)
```protobuf
// Internal gRPC between services
service BizService {
  rpc MessagesSendMessage(MessagesSendMessageReq) returns (Updates);
  rpc UsersGetUsers(UsersGetUsersReq) returns (Vector<User>);
}
```

### 2. External RPC (Client-to-Server)
```tl
// MTProto RPC for Telegram clients
messages.sendMessage#520c3870 peer:InputPeer message:string = Updates;
users.getUsers#d91a548 id:Vector<InputUser> = Vector<User>;
```

## Development Workflow

### Step 1: Define TL Schema

```tl
// File: specs/mtproto.tl

// Request/Response types
premium.getStatus#d0b5e0f2 user_id:long = PremiumStatus;
premium.purchase#8f8c0e1c user_id:long plan_id:int payment_method:string = Bool;

// Object types
premiumStatus#9a4f3e2d user_id:long status:int expires_at:long = PremiumStatus;
```

**Naming Conventions**:
- Method: `category.actionName` (camelCase)
- Constructor ID: `#8hexdigits` (random or sequential)
- Types: PascalCase

### Step 2: Generate Go Code

```bash
# Generate from TL schema
make generate
# or
go run cmd/mtprotoc/main.go -I specs/ -o app/

# Output files:
# app/mtproto/premium_get_status.go
# app/mtproto/premium_purchase.go
# app/mtproto/premium_status.go
```

### Step 3: Create Database Schema

```sql
-- File: data/schema/premium.sql

CREATE TABLE user_premium (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    status TINYINT DEFAULT 0 COMMENT '0=none, 1=basic, 2=premium',
    plan_id INT DEFAULT 0,
    expires_at BIGINT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_user_id (user_id),
    INDEX idx_expires (expires_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE premium_transactions (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    plan_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    payment_method VARCHAR(50),
    status TINYINT DEFAULT 0 COMMENT '0=pending, 1=success, 2=failed',
    transaction_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### Step 4: Implement DAO Layer

```go
// File: app/service/biz/internal/dao/premium_dao.go

package dao

import (
    "context"
    "database/sql"
    "time"
    
    "github.com/teamgram/teamgram-server/app/service/biz/internal/model"
    "github.com/zeromicro/go-zero/core/stores/sqlx"
)

type PremiumDAO struct {
    db sqlx.SqlConn
}

func NewPremiumDAO(db sqlx.SqlConn) *PremiumDAO {
    return &PremiumDAO{db: db}
}

// GetPremiumStatus 获取用户会员状态
func (d *PremiumDAO) GetPremiumStatus(ctx context.Context, userID int64) (*model.UserPremium, error) {
    var m model.UserPremium
    query := `SELECT * FROM user_premium WHERE user_id = ?`
    err := d.db.QueryRowCtx(ctx, &m, query, userID)
    if err == sqlx.ErrNotFound {
        // 返回默认状态（非会员）
        return &model.UserPremium{UserID: userID, Status: 0}, nil
    }
    return &m, err
}

// CreateOrUpdatePremium 创建或更新会员状态
func (d *PremiumDAO) CreateOrUpdatePremium(ctx context.Context, userID int64, status int32, planID int, expiresAt int64) error {
    query := `
        INSERT INTO user_premium (user_id, status, plan_id, expires_at) 
        VALUES (?, ?, ?, ?)
        ON DUPLICATE KEY UPDATE 
        status = VALUES(status), 
        plan_id = VALUES(plan_id), 
        expires_at = VALUES(expires_at)
    `
    _, err := d.db.ExecCtx(ctx, query, userID, status, planID, expiresAt)
    return err
}

// CreateTransaction 创建交易记录
func (d *PremiumDAO) CreateTransaction(ctx context.Context, txn *model.PremiumTransaction) (int64, error) {
    query := `
        INSERT INTO premium_transactions 
        (user_id, plan_id, amount, currency, payment_method, status, transaction_id) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
    `
    result, err := d.db.ExecCtx(ctx, query,
        txn.UserID, txn.PlanID, txn.Amount, txn.Currency,
        txn.PaymentMethod, txn.Status, txn.TransactionID,
    )
    if err != nil {
        return 0, err
    }
    return result.LastInsertId()
}

// UpdateTransactionStatus 更新交易状态
func (d *PremiumDAO) UpdateTransactionStatus(ctx context.Context, txnID int64, status int32) error {
    query := `UPDATE premium_transactions SET status = ? WHERE id = ?`
    _, err := d.db.ExecCtx(ctx, query, status, txnID)
    return err
}
```

### Step 5: Implement Core Logic

```go
// File: app/service/biz/internal/core/premium_core.go

package core

import (
    "context"
    "errors"
    "time"
    
    "github.com/teamgram/teamgram-server/app/service/biz/internal/dao"
    "github.com/teamgram/teamgram-server/app/service/biz/internal/model"
    "github.com/teamgram/teamgram-server/app/service/biz/internal/svc"
)

var (
    ErrInvalidPlan = errors.New("invalid premium plan")
    ErrPaymentFailed = errors.New("payment processing failed")
)

type PremiumCore struct {
    svcCtx *svc.ServiceContext
    dao    *dao.PremiumDAO
}

func NewPremiumCore(svcCtx *svc.ServiceContext) *PremiumCore {
    return &PremiumCore{
        svcCtx: svcCtx,
        dao:    dao.NewPremiumDAO(svcCtx.DB),
    }
}

// GetPremiumStatus 获取用户会员状态
func (c *PremiumCore) GetPremiumStatus(ctx context.Context, userID int64) (*model.PremiumStatus, error) {
    // 1. 查询数据库
    premium, err := c.dao.GetPremiumStatus(ctx, userID)
    if err != nil {
        return nil, err
    }
    
    // 2. 检查是否过期
    now := time.Now().Unix()
    if premium.Status > 0 && premium.ExpiresAt < now {
        // 已过期，更新状态
        premium.Status = 0
        _ = c.dao.CreateOrUpdatePremium(ctx, userID, 0, 0, 0)
    }
    
    return &model.PremiumStatus{
        UserID:    userID,
        Status:    premium.Status,
        ExpiresAt: premium.ExpiresAt,
    }, nil
}

// PurchasePremium 购买会员
func (c *PremiumCore) PurchasePremium(ctx context.Context, userID int64, planID int, paymentMethod string) error {
    // 1. 验证套餐
    plan := c.getPlanByID(planID)
    if plan == nil {
        return ErrInvalidPlan
    }
    
    // 2. 创建交易记录
    txn := &model.PremiumTransaction{
        UserID:        userID,
        PlanID:        planID,
        Amount:        plan.Price,
        Currency:      plan.Currency,
        PaymentMethod: paymentMethod,
        Status:        0, // pending
    }
    
    txnID, err := c.dao.CreateTransaction(ctx, txn)
    if err != nil {
        return err
    }
    
    // 3. 调用支付网关（异步处理）
    go c.processPayment(txnID, userID, plan)
    
    return nil
}

// processPayment 处理支付（异步）
func (c *PremiumCore) processPayment(txnID int64, userID int64, plan *Plan) {
    ctx := context.Background()
    
    // 调用支付接口...
    // 成功后在回调中：
    
    // 1. 更新交易状态
    _ = c.dao.UpdateTransactionStatus(ctx, txnID, 1) // success
    
    // 2. 更新用户会员状态
    expiresAt := time.Now().AddDate(0, plan.DurationMonths, 0).Unix()
    _ = c.dao.CreateOrUpdatePremium(ctx, userID, 1, plan.ID, expiresAt)
    
    // 3. 发送通知
    c.svcCtx.PushClient.SendToUser(ctx, userID, "Premium activated!")
}

func (c *PremiumCore) getPlanByID(planID int) *Plan {
    plans := map[int]*Plan{
        1: {ID: 1, Name: "Basic", Price: 4.99, DurationMonths: 1},
        2: {ID: 2, Name: "Premium", Price: 49.99, DurationMonths: 12},
    }
    return plans[planID]
}

type Plan struct {
    ID             int
    Name           string
    Price          float64
    Currency       string
    DurationMonths int
}
```

### Step 6: Implement RPC Server

```go
// File: app/service/biz/internal/server/premium_server.go

package server

import (
    "context"
    
    "github.com/teamgram/teamgram-server/app/mtproto"
    "github.com/teamgram/teamgram-server/app/service/biz/internal/core"
    "github.com/teamgram/teamgram-server/app/service/biz/internal/svc"
)

func (s *Server) PremiumGetStatus(ctx context.Context, req *mtproto.TLPremiumGetStatus) (*mtproto.PremiumStatus, error) {
    // 1. 调用Core层
    status, err := s.premiumCore.GetPremiumStatus(ctx, req.UserId)
    if err != nil {
        return nil, err
    }
    
    // 2. 转换为MTProto对象
    return &mtproto.TLPremiumStatus{
        UserId:    status.UserID,
        Status:    status.Status,
        ExpiresAt: status.ExpiresAt,
    }, nil
}

func (s *Server) PremiumPurchase(ctx context.Context, req *mtproto.TLPremiumPurchase) (*mtproto.Bool, error) {
    // 1. 调用Core层
    err := s.premiumCore.PurchasePremium(ctx, req.UserId, int(req.PlanId), req.PaymentMethod)
    if err != nil {
        return mtproto.BoolFalse, err
    }
    
    return mtproto.BoolTrue, nil
}
```

### Step 7: Register RPC

```go
// File: app/service/biz/internal/server/server.go

func Register(grpcServer *grpc.Server, svcCtx *svc.ServiceContext) {
    s := &Server{
        svcCtx:      svcCtx,
        premiumCore: core.NewPremiumCore(svcCtx),
        // ... other cores
    }
    
    // Register all services
    mtproto.RegisterBizServiceServer(grpcServer, s)
}
```

### Step 8: Testing

```go
// File: app/service/biz/internal/core/premium_core_test.go

package core_test

import (
    "context"
    "testing"
    
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/mock"
    "github.com/teamgram/teamgram-server/app/service/biz/internal/core"
)

func TestGetPremiumStatus(t *testing.T) {
    // Setup
    svcCtx := setupTestContext()
    c := core.NewPremiumCore(svcCtx)
    
    // Test: Non-premium user
    status, err := c.GetPremiumStatus(context.Background(), 123456)
    
    // Assert
    assert.NoError(t, err)
    assert.Equal(t, int32(0), status.Status)
    assert.Equal(t, int64(123456), status.UserID)
}

func TestPurchasePremium(t *testing.T) {
    // Setup with mocked payment gateway
    svcCtx := setupTestContext()
    c := core.NewPremiumCore(svcCtx)
    
    // Execute
    err := c.PurchasePremium(context.Background(), 123456, 1, "stripe")
    
    // Assert
    assert.NoError(t, err)
    // Verify transaction created...
}
```

## Advanced Patterns

### 1. Rate Limiting

```go
func (s *Server) PremiumPurchase(ctx context.Context, req *mtproto.TLPremiumPurchase) (*mtproto.Bool, error) {
    // Check rate limit
    key := fmt.Sprintf("rate_limit:purchase:%d", req.UserId)
    count, err := s.svcCtx.Redis.Incr(key)
    if err == nil && count > 10 {
        return nil, errors.New("rate limit exceeded")
    }
    s.svcCtx.Redis.Expire(key, 3600) // 1 hour
    
    // Process...
}
```

### 2. Caching

```go
func (c *PremiumCore) GetPremiumStatus(ctx context.Context, userID int64) (*model.PremiumStatus, error) {
    // Try cache
    cacheKey := fmt.Sprintf("premium:%d", userID)
    cached, err := c.svcCtx.Redis.Get(cacheKey)
    if err == nil {
        var status model.PremiumStatus
        json.Unmarshal([]byte(cached), &status)
        return &status, nil
    }
    
    // Cache miss - query DB
    status, err := c.dao.GetPremiumStatus(ctx, userID)
    if err != nil {
        return nil, err
    }
    
    // Update cache
    data, _ := json.Marshal(status)
    c.svcCtx.Redis.Set(cacheKey, string(data), 300) // 5 min TTL
    
    return status, nil
}
```

### 3. Distributed Transactions

```go
func (c *PremiumCore) PurchaseWithTransaction(ctx context.Context, userID int64, planID int) error {
    return c.svcCtx.DB.Transact(func(tx *sql.Tx) error {
        // Deduct balance
        if err := c.dao.DeductBalanceTx(tx, userID, amount); err != nil {
            return err
        }
        
        // Create premium record
        if err := c.dao.CreatePremiumTx(tx, userID, planID); err != nil {
            return err
        }
        
        // Record transaction
        return c.dao.RecordTransactionTx(tx, userID, amount)
    })
}
```

## Common Mistakes

### 1. Not Handling Context Cancellation
```go
// Wrong
func (c *Core) LongOperation(ctx context.Context) {
    time.Sleep(10 * time.Second) // Blocks even if client disconnected
}

// Correct
func (c *Core) LongOperation(ctx context.Context) error {
    select {
    case <-ctx.Done():
        return ctx.Err()
    case <-time.After(10 * time.Second):
        return nil
    }
}
```

### 2. Ignoring Database Errors
```go
// Wrong
data, _ := c.dao.Get(ctx, id) // Silent failure!

// Correct
data, err := c.dao.Get(ctx, id)
if err != nil {
    if err == sqlx.ErrNotFound {
        return nil, status.Error(codes.NotFound, "not found")
    }
    return nil, status.Error(codes.Internal, err.Error())
}
```

### 3. Not Using Transactions
```go
// Wrong - partial failure possible
c.dao.DeductBalance(ctx, userID, amount)
c.dao.AddPremium(ctx, userID, planID) // May fail after deduction!

// Correct - atomic operation
c.svcCtx.DB.Transact(func(tx *sql.Tx) error {
    c.dao.DeductBalanceTx(tx, userID, amount)
    c.dao.AddPremiumTx(tx, userID, planID)
    return nil
})
```

## References

- [TL Language Spec](https://core.telegram.org/mtproto/TL)
- [gRPC Go Documentation](https://grpc.io/docs/languages/go/)
- [Go Database/SQL Tutorial](https://golang.org/doc/tutorial/database-access)

See [references/rpc-patterns.md](references/rpc-patterns.md) for common patterns.
