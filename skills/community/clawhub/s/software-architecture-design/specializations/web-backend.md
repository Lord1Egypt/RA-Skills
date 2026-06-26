# Specialization: Web / API Backend

Apply this guidance on top of the base SOP for web services, REST APIs, and microservices.

## Phase 3 — Architecture Pattern Options

| Pattern | When to choose |
|---------|---------------|
| Monolith-first | Team < 5, unclear domain boundaries, early product |
| Layered (N-tier) | Well-understood domain, moderate traffic, single team |
| Microservices | Independent scaling requirements, multiple teams, clear domain boundaries |
| Event-driven | High decoupling needed, async-heavy workflows, audit trail required |
| Plugin-based | Extensibility is a first-class requirement (users add algorithms/integrations) |

## Phase 6 — Storage Selection Rules

| Data type | Default choice | Escalate when |
|-----------|---------------|---------------|
| Relational business entities | SQLite → PostgreSQL | Need multi-process write, JSONB queries, replication |
| Session / cache / queue | In-process map → Redis | Need persistence across restarts, multi-instance |
| Files / blobs | Local filesystem | Need shared access, CDN, lifecycle policies |
| Search | Database LIKE → Elasticsearch | Full-text, facets, relevance ranking required |
| Time-series metrics | Log files → InfluxDB/TimescaleDB | High-frequency writes, retention policies, aggregations |

## Phase 7 — Common Decision Points

| Decision | Option A | Option B | Key differentiator |
|----------|----------|----------|-------------------|
| Sync vs async task execution | Sync HTTP response | Background queue + polling/webhook | Task duration > 5s → use async |
| Monolith vs microservice split | Start monolith | Extract service | Only split when you feel the pain |
| REST vs GraphQL | REST + versioning | GraphQL | Multiple clients with different data needs → GraphQL |
| Auth: session vs token | Server-side session | JWT / OAuth2 token | Stateless horizontal scaling → token |
| Queue: in-process vs broker | In-process queue | Redis / RabbitMQ / Kafka | Durability across restarts required → broker |

## Phase 8 — API Design Standards

- Always version: `/api/v1/`
- Use nouns not verbs for resources: `/tasks` not `/getTasks`
- Standard status codes: 200 GET, 201 POST, 204 DELETE, 400 validation, 401 auth, 404 not found, 409 conflict, 422 unprocessable, 500 server error
- Pagination: cursor-based preferred over offset for large datasets
- Error body: `{"error": {"code": "RESOURCE_NOT_FOUND", "message": "...", "details": {}}}`

## Phase 9 — Deployment Models

| Model | When to use |
|-------|-------------|
| Single process (no container) | Development only |
| Docker Compose single host | MVP, single-tenant, private deployment |
| Docker Compose + reverse proxy | Small production, < 100 concurrent users |
| Kubernetes | Multi-tenant, auto-scaling, multiple services |
| Serverless (FaaS) | Sporadic traffic, stateless functions, event-driven |

## Phase 10 — Web-Specific NFR

- **Rate limiting**: protect all public endpoints; use token bucket or sliding window
- **CORS**: configure explicitly; never use wildcard `*` in production
- **Input validation**: validate and sanitize at the API boundary, not just in business logic
- **SQL injection**: use parameterized queries / ORM only; never string-concatenate SQL
- **Secrets**: never in code or env vars committed to git; use vault or secrets manager
