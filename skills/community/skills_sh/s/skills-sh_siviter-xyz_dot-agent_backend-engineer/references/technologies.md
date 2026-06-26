# Backend Technologies

Core technologies, frameworks, databases, and message queues for modern backend development.

## Programming Languages

### Node.js/TypeScript
**Best For:**
- Full-stack JavaScript teams
- Real-time applications (WebSockets)
- Rapid prototyping with npm ecosystem
- Event-driven architectures

**Popular Frameworks:**
- **NestJS** - Enterprise-grade, TypeScript-first, modular architecture
- **Express** - Lightweight, flexible, most popular
- **Fastify** - High performance
- **tRPC** - End-to-end typesafe APIs without GraphQL

**When to Choose:** Team already using JavaScript/TypeScript, real-time features needed, rapid development priority

### Python
**Best For:**
- Data-heavy applications
- ML/AI integration
- Scientific computing
- Scripting and automation

**Popular Frameworks:**
- **FastAPI** - Modern, async, auto-generated OpenAPI docs, validation via Pydantic
- **Django** - Batteries-included, ORM, admin panel, authentication
- **Flask** - Lightweight, flexible, microservices-friendly

**When to Choose:** Data science integration, ML/AI features, rapid prototyping, team Python expertise

### Go
**Best For:**
- High-concurrency systems (goroutines)
- Microservices architectures
- CLI tools and DevOps tooling
- System programming

**Popular Frameworks:**
- **Gin** - Fast HTTP router
- **Echo** - High performance, extensible
- **Fiber** - Express-like API

**When to Choose:** Microservices, high concurrency needs, DevOps tooling, simple deployment (single binary)

### Rust
**Best For:**
- Performance-critical systems
- Memory-safe system programming
- High-reliability requirements
- WebAssembly backends

**Popular Frameworks:**
- **Axum** - Ergonomic, modular, tokio-based
- **Actix-web** - Fastest web framework
- **Rocket** - Type-safe, easy to use

**When to Choose:** Maximum performance needed, memory safety critical, low-level control required

## Databases

### PostgreSQL
**Strengths:**
- ACID compliance, data integrity
- JSON/JSONB support (hybrid SQL + NoSQL)
- Full-text search, geospatial (PostGIS)
- Advanced indexing (B-tree, Hash, GiST, GIN)
- Window functions, CTEs, materialized views

**Use Cases:**
- E-commerce (transactions critical)
- Financial applications
- Complex reporting requirements
- Multi-tenant applications

**When to Choose:** Need ACID guarantees, complex queries/joins, data integrity critical

### MongoDB
**Strengths:**
- Flexible/evolving schemas
- Horizontal scaling (sharding built-in)
- Aggregation pipeline (powerful data processing)
- GridFS for large files

**Use Cases:**
- Content management systems
- Real-time analytics
- IoT data collection
- Catalogs with varied attributes

**When to Choose:** Schema flexibility needed, rapid iteration, horizontal scaling required

### Redis
**Capabilities:**
- In-memory key-value store
- Pub/sub messaging
- Sorted sets (leaderboards)
- Geospatial indexes
- Streams (event sourcing)

**Performance:** 10-100x faster than disk-based databases

**Use Cases:**
- Session storage
- Rate limiting
- Real-time leaderboards
- Job queues
- Caching layer (90% DB load reduction)

**When to Choose:** Need sub-millisecond latency, caching layer, session management

## ORMs & Database Tools

### Modern ORMs

**Drizzle ORM** (TypeScript)
- SQL-like syntax, full type safety
- Best for: Performance-critical TypeScript apps

**Prisma** (TypeScript)
- Auto-generated type-safe client
- Database migrations included
- Best for: Rapid development, type safety

**SQLAlchemy** (Python)
- Industry standard Python ORM
- Powerful query builder
- Best for: Python backends

## Message Queues & Event Streaming

### RabbitMQ
**Best For:** Task queues, request/reply patterns

**Strengths:**
- Flexible routing (direct, topic, fanout, headers)
- Message acknowledgment and durability
- Dead letter exchanges
- Wide protocol support

**Use Cases:**
- Background job processing
- Microservices communication
- Email/notification queues

### Apache Kafka
**Best For:** Event streaming, millions messages/second

**Strengths:**
- Distributed, fault-tolerant
- High throughput
- Message replay (retention-based)
- Stream processing

**Use Cases:**
- Real-time analytics
- Event sourcing
- Log aggregation
- High-scale event streaming

## Common Pitfalls

1. **Choosing NoSQL for relational data** - Use PostgreSQL if data has clear relationships
2. **Not using connection pooling** - Implement pooling for 5-10x performance boost
3. **Ignoring indexes** - Add indexes to frequently queried columns
4. **Over-engineering with microservices** - Start monolith, split when needed
5. **Not caching** - Redis caching provides significant DB load reduction
