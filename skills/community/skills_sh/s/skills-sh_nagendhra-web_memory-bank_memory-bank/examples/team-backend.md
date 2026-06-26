# Project Memory
Last updated: 2025-04-05 | Session 12 | Branch: main
Health: 7/10 (2 stale file refs from infra work)

## Project Overview
Internal order management REST API. Go 1.22, Chi, PostgreSQL, Redis. Docker + AWS ECS. Serves dashboard (React) and mobile app (Flutter).

## Where We Left Off
- **Task:** Rate limiting middleware `internal/middleware/ratelimit.go`
- **Status:** WIP. Token bucket algo done, Redis backend next
- **Next:** [AK] Wire Redis counter in `ratelimit.go:47`, add per-endpoint config in `internal/config/ratelimit.yaml`
- **Open:** Rate limit by API key or IP? Leaning API key (all clients authenticated)

## Blockers
- Rate limit thresholds need product sign-off. Using 100 req/min placeholder.

## Key Decisions
| Decision | Who | Why |
|----------|-----|-----|
| Chi over Gin | JS | Better middleware composability, stdlib-aligned |
| sqlc over GORM | JS | Type-safe generated code, no reflection |
| ECS Fargate over EKS | MR | Simpler ops, lower cost at current scale |
| JWT with refresh rotation | JS | 15min access / 7day refresh, rotate on use |
| slog over zerolog | MR | Stdlib, good enough for structured logging |

## Key Files
| File | Purpose |
|------|---------|
| `internal/middleware/ratelimit.go` | Rate limiting |
| `internal/middleware/auth.go` | JWT validation |
| `internal/handlers/orders.go` | Order CRUD |
| `internal/service/order_service.go` | Business logic |
| `internal/repository/queries.sql` | sqlc definitions |
| `internal/cache/redis.go` | Redis client |

## Active Work
- [ ] [AK] Rate limiting Redis backend (WIP)
- [ ] [JS] Order search with PG full-text (TODO)
- [ ] [MR] Grafana dashboards for latency (WIP)
- [ ] [AK] Swagger/OpenAPI docs (TODO)

## Completed
- [S1-4] Setup, Docker, CI, DB schema
- [S5-6] [JS] Auth endpoints, JWT + refresh
- [S7] [MR] Terraform: ECS, RDS, ElastiCache
- [S8-9] [JS] Order CRUD + pagination
- [S10] [JS] Redis caching, [AK] validation middleware
- [S11] [JS] Webhooks, [MR] ElastiCache Terraform
- [S12] [AK] Rate limit algo, [MR] slog + CloudWatch

## Architecture
```
Request -> Chi Router -> Auth MW (JWT) -> Rate Limit MW -> Handler -> Service -> Repository (Redis cache -> PostgreSQL)
```
- MW order matters: auth before rate limit (need API key for per-key limits)
- Repo checks Redis first, falls through to PG. Writes invalidate cache.
- `make generate` after SQL changes (sqlc).

## Known Issues
- [JS] Refresh token race condition under concurrent requests. OK for internal, needs fix before external. Issue #34.
- [MR] ECS health check timeouts during deploy. Grace period added, not root-caused.

## External Context
- PG on RDS: `DATABASE_URL`
- Redis on ElastiCache: `REDIS_URL`
- CI/CD: GitHub Actions -> ECR -> ECS (`.github/workflows/deploy.yml`)
