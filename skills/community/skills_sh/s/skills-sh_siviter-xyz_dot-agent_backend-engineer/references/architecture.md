# Backend Architecture

Microservices, event-driven, CQRS, and saga patterns.

## Microservices

### Principles
- Single responsibility per service
- Independent deployment
- Service-specific databases
- Inter-service communication via APIs

### When to Use
- Large, complex systems
- Different scaling needs per service
- Multiple teams working independently
- Technology diversity needed

### Challenges
- Service discovery
- Distributed transactions
- Network latency
- Data consistency
- Monitoring complexity

### Communication Patterns
- Synchronous: REST, gRPC
- Asynchronous: Message queues, event streaming
- Hybrid: REST for queries, events for updates

## Event-Driven Architecture

### Principles
- Services communicate via events
- Loose coupling
- Event sourcing for audit trails
- Event replay for recovery

### Patterns
- Event sourcing - Store events, not state
- CQRS - Separate read/write models
- Saga - Distributed transactions
- Event streaming - Kafka, RabbitMQ

### Benefits
- Scalability
- Resilience
- Flexibility
- Auditability

## CQRS (Command Query Responsibility Segregation)

### Principles
- Separate read and write models
- Optimize each independently
- Event sourcing for writes
- Denormalized read models

### When to Use
- High read/write ratio
- Complex queries
- Different scaling needs
- Event sourcing requirements

## Saga Pattern

### Distributed Transactions
- Long-running transactions across services
- Compensating actions for rollback
- Event-driven coordination

### Types
- Choreography - Services coordinate via events
- Orchestration - Central coordinator manages flow

### Example Flow
1. Order service creates order
2. Payment service processes payment
3. Inventory service reserves items
4. If any step fails, compensate previous steps

## Service Mesh

### Benefits
- Service discovery
- Load balancing
- Circuit breaking
- Observability
- Security (mTLS)

### Tools
- Istio
- Linkerd
- Consul Connect

## API Gateway

### Functions
- Request routing
- Authentication/authorization
- Rate limiting
- Request/response transformation
- Monitoring and logging

### Patterns
- Single entry point
- Backend for frontend (BFF)
- API composition
