---
name: rest_api_wrapper_generator
description: Generate production-ready REST API endpoints to expose graph database operations, queries, and data management capabilities
category: integrations
tags:
  - knowledge-graph
  - rest-api
  - api-design
  - backend
  - graph-database
  - microservices
  - integration
  - fastapi
  - express
version: 1.0.0
author: kg-dev-skills
---

# REST API Wrapper Generator

## Purpose

This skill generates **production-ready REST API endpoints** that expose graph database operations and queries through a standardized HTTP interface.

It enables developers to:
- Expose graph database queries through REST endpoints
- Create APIs for node and relationship management
- Retrieve and traverse graph data via HTTP requests
- Integrate graph databases with web services and microservices
- Provide standardized interfaces for external applications

This provides a **standard HTTP interface** for graph-based systems, enabling seamless integration with modern web and mobile applications.

### Supported Databases
- Neo4j
- JanusGraph
- RDF Triple Stores (SPARQL endpoints)
- TigerGraph
- Any graph database with drivers

### Key Capabilities
- Auto-generate CRUD endpoints for graph nodes
- Auto-generate relationship management endpoints
- Create custom query execution endpoints
- Graph traversal and path-finding endpoints
- Batch operation endpoints
- Transaction support
- Built-in authentication and authorization
- Request validation and error handling
- API documentation generation
- Performance optimization features

---

## When To Use This Skill

Use this skill when:

- **Building Backend Services**: Creating REST APIs for graph-based applications
- **Exposing Graph Data**: Providing HTTP access to graph databases
- **Microservices Integration**: Connecting graph databases to microservices
- **Multi-Client Support**: Supporting web, mobile, and desktop applications
- **External Integration**: Enabling third-party systems to access graph data
- **API Development**: Rapidly generating API endpoints with validation

### Example Triggers

- "Generate REST endpoints for graph operations"
- "Create API for node and relationship management"
- "Build REST wrapper for Neo4j database"
- "Expose graph queries via HTTP endpoints"
- "Generate API with authentication and rate limiting"

---

## REST API Fundamentals

### HTTP Methods

| Method | Operation | Idempotent | Cacheable |
|--------|-----------|-----------|-----------|
| GET | Retrieve resources | ✓ | ✓ |
| POST | Create resources | ✗ | ✗ |
| PUT | Update resources | ✓ | ✗ |
| PATCH | Partial update | ✗ | ✗ |
| DELETE | Remove resources | ✓ | ✗ |
| HEAD | Like GET but no body | ✓ | ✓ |

### Status Codes

| Code | Meaning | Use Case |
|------|---------|----------|
| 200 | OK | Successful GET, PUT, PATCH |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid input |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 409 | Conflict | Resource conflict |
| 500 | Server Error | Internal error |
| 503 | Service Unavailable | Server maintenance |

### REST Conventions

```
GET    /api/v1/nodes                 - List all nodes
GET    /api/v1/nodes/{id}            - Get specific node
POST   /api/v1/nodes                 - Create new node
PUT    /api/v1/nodes/{id}            - Update node
DELETE /api/v1/nodes/{id}            - Delete node

GET    /api/v1/relationships         - List relationships
POST   /api/v1/relationships         - Create relationship
DELETE /api/v1/relationships/{id}    - Delete relationship

POST   /api/v1/query                 - Execute query
GET    /api/v1/nodes/{id}/neighbors  - Get connected nodes
```

---

## API Configuration

### Connection Configuration

```json
{
  "database_type": "neo4j",
  "database_url": "bolt://localhost:7687",
  "database_user": "neo4j",
  "database_password": "password",
  "connection_pool_size": 10
}
```

### API Configuration

```json
{
  "api_title": "Knowledge Graph API",
  "api_version": "1.0.0",
  "base_path": "/api/v1",
  "host": "0.0.0.0",
  "port": 8000,
  "enable_cors": true,
  "enable_authentication": true,
  "authentication_type": "jwt",
  "enable_rate_limiting": true,
  "rate_limit_requests": 1000,
  "rate_limit_window": 3600
}
```

---

## Core API Patterns

### Pattern 1: Node Endpoints

#### Retrieve All Nodes
```http
GET /api/v1/nodes?limit=20&offset=0
```

Response:
```json
{
  "nodes": [
    {"id": "n1", "label": "Person", "properties": {"name": "Alice"}},
    {"id": "n2", "label": "Person", "properties": {"name": "Bob"}}
  ],
  "total": 100,
  "limit": 20,
  "offset": 0
}
```

#### Retrieve Specific Node
```http
GET /api/v1/nodes/n1
```

Response:
```json
{
  "id": "n1",
  "label": "Person",
  "properties": {"name": "Alice", "age": 30},
  "created_at": "2024-01-15T10:30:00Z"
}
```

#### Create Node
```http
POST /api/v1/nodes
Content-Type: application/json

{
  "label": "Person",
  "properties": {
    "name": "Charlie",
    "age": 25,
    "email": "charlie@example.com"
  }
}
```

Response:
```json
{
  "id": "n3",
  "label": "Person",
  "properties": {"name": "Charlie", "age": 25, "email": "charlie@example.com"},
  "status": "created"
}
```

#### Update Node
```http
PUT /api/v1/nodes/n1
Content-Type: application/json

{
  "properties": {
    "age": 31
  }
}
```

#### Delete Node
```http
DELETE /api/v1/nodes/n1
```

Response:
```json
{
  "status": "deleted",
  "id": "n1"
}
```

### Pattern 2: Relationship Endpoints

#### Create Relationship
```http
POST /api/v1/relationships
Content-Type: application/json

{
  "from_node_id": "n1",
  "to_node_id": "n2",
  "relationship_type": "KNOWS",
  "properties": {
    "since": "2020-01-15"
  }
}
```

Response:
```json
{
  "id": "r1",
  "from_node_id": "n1",
  "to_node_id": "n2",
  "relationship_type": "KNOWS",
  "properties": {"since": "2020-01-15"},
  "status": "created"
}
```

#### Get Node Relationships
```http
GET /api/v1/nodes/n1/relationships
```

Response:
```json
{
  "relationships": [
    {
      "id": "r1",
      "from_node_id": "n1",
      "to_node_id": "n2",
      "relationship_type": "KNOWS"
    }
  ]
}
```

#### Get Node Neighbors
```http
GET /api/v1/nodes/n1/neighbors
```

Response:
```json
{
  "neighbors": [
    {"id": "n2", "label": "Person", "properties": {"name": "Bob"}}
  ]
}
```

### Pattern 3: Query Endpoints

#### Execute Custom Query
```http
POST /api/v1/query
Content-Type: application/json

{
  "query": "MATCH (n:Person) WHERE n.age > 25 RETURN n",
  "limit": 100
}
```

Response:
```json
{
  "results": [
    {"n": {"id": "n1", "label": "Person", "properties": {"name": "Alice", "age": 30}}}
  ],
  "execution_time_ms": 42
}
```

#### Graph Traversal
```http
POST /api/v1/traverse
Content-Type: application/json

{
  "start_node_id": "n1",
  "max_depth": 3,
  "relationship_types": ["KNOWS", "FRIEND_OF"]
}
```

#### Path Finding
```http
POST /api/v1/paths
Content-Type: application/json

{
  "from_node_id": "n1",
  "to_node_id": "n10",
  "max_hops": 5
}
```

---

## Request/Response Patterns

### Pagination

```http
GET /api/v1/nodes?limit=20&offset=40
```

Query Parameters:
- `limit` - Number of results (default: 20, max: 100)
- `offset` - Starting position (default: 0)

Response includes:
```json
{
  "data": [...],
  "total": 500,
  "limit": 20,
  "offset": 40
}
```

### Filtering

```http
GET /api/v1/nodes?filter[name]=Alice&filter[age]=30
GET /api/v1/nodes?filter[age][gt]=25
GET /api/v1/nodes?filter[status][in]=active,pending
```

### Sorting

```http
GET /api/v1/nodes?sort=name
GET /api/v1/nodes?sort=-age
GET /api/v1/nodes?sort=name,age
```

### Field Selection

```http
GET /api/v1/nodes/n1?fields=name,age,email
```

### Error Responses

```json
{
  "status": "error",
  "code": "INVALID_INPUT",
  "message": "Invalid node properties",
  "details": {
    "name": "Name is required",
    "age": "Age must be positive"
  }
}
```

---

## Authentication & Authorization

### JWT Authentication

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "user",
  "password": "password"
}
```

Response:
```json
{
  "token": "eyJhbGc...",
  "expires_in": 3600
}
```

Using token:
```http
GET /api/v1/nodes
Authorization: Bearer eyJhbGc...
```

### API Key Authentication

```http
GET /api/v1/nodes
X-API-Key: your-api-key-here
```

### Role-Based Access Control

```python
@api.get("/nodes/sensitive")
@require_auth(roles=["admin", "data_reader"])
def get_sensitive_nodes():
    pass
```

---

## Advanced Features

### Batch Operations

```http
POST /api/v1/batch
Content-Type: application/json

{
  "operations": [
    {"method": "POST", "path": "/nodes", "body": {...}},
    {"method": "POST", "path": "/relationships", "body": {...}},
    {"method": "PUT", "path": "/nodes/n1", "body": {...}}
  ]
}
```

Response:
```json
{
  "results": [
    {"status": 201, "body": {...}},
    {"status": 201, "body": {...}},
    {"status": 200, "body": {...}}
  ]
}
```

### Transactions

```http
POST /api/v1/transactions
Content-Type: application/json

{
  "operations": [...]
}
```

### Webhooks

```http
POST /api/v1/webhooks
Content-Type: application/json

{
  "event": "node.created",
  "callback_url": "https://example.com/webhook",
  "active": true
}
```

### Caching

```http
GET /api/v1/nodes
Cache-Control: max-age=3600
```

---

## Best Practices

### 1. API Design
✅ Use descriptive resource names  
✅ Follow RESTful conventions  
✅ Version your APIs  
✅ Use proper HTTP methods and status codes  
✅ Include pagination for large result sets  

### 2. Validation
✅ Validate all input data  
✅ Provide detailed error messages  
✅ Use schema validation  
✅ Implement type checking  
✅ Check authorization permissions  

### 3. Performance
✅ Implement pagination  
✅ Use caching appropriately  
✅ Create database indexes  
✅ Optimize queries  
✅ Use connection pooling  

### 4. Security
✅ Require authentication for sensitive endpoints  
✅ Implement rate limiting  
✅ Use HTTPS in production  
✅ Validate and sanitize input  
✅ Implement CORS properly  

### 5. Monitoring
✅ Log all API requests  
✅ Track error rates  
✅ Monitor response times  
✅ Alert on anomalies  
✅ Document API usage  

### 6. Documentation
✅ Generate API documentation  
✅ Include example requests/responses  
✅ Document error codes  
✅ Provide SDK/client libraries  
✅ Keep documentation up-to-date  

### 7. Versioning
✅ Version your API endpoints  
✅ Maintain backward compatibility  
✅ Deprecate endpoints gradually  
✅ Provide migration guides  
✅ Support multiple API versions  

### 8. Error Handling
✅ Use standard error formats  
✅ Include error codes  
✅ Provide context in errors  
✅ Log errors server-side  
✅ Don't expose sensitive info  

---

## Integration with Related Skills

### Neo4j Integration
- Expose Neo4j queries via REST
- Create node management APIs
- Implement relationship endpoints

### JanusGraph Connector
- Build REST wrapper for Gremlin queries
- Expose distributed graph operations
- Multi-graph management APIs

### RDF Triple Store Integration
- Create SPARQL query endpoints
- Expose RDF operations via REST
- Named graph management

### Graph Query Optimization
- Optimize API query performance
- Implement query result caching
- Monitor slow endpoints

### GraphQL Graph Mapping
- Provide REST alternative to GraphQL
- Support both REST and GraphQL APIs
- Convert between formats

---

## Libraries & Frameworks

### Python

| Library | Purpose |
|---------|---------|
| FastAPI | Modern REST framework |
| Flask | Lightweight framework |
| Django REST | Full-featured framework |
| Pydantic | Data validation |
| SQLAlchemy | Database ORM |

### JavaScript/Node.js

| Library | Purpose |
|---------|---------|
| Express | Minimal framework |
| Fastify | High-performance framework |
| Nest.js | Full-featured framework |
| Joi | Schema validation |

### Installation

```bash
# Python
pip install fastapi uvicorn pydantic

# Node.js
npm install express express-async-errors joi
```

---

## Expected Benefits

Using this skill enables:

✅ **Rapid API Development** - Auto-generate endpoints instead of manual coding  
✅ **Standardized Interface** - Consistent REST API across projects  
✅ **Easy Integration** - Connect graph databases to web/mobile apps  
✅ **Microservices Ready** - Built-in support for distributed architectures  
✅ **Built-in Security** - Authentication, authorization, rate limiting  
✅ **Developer Friendly** - Auto-generated documentation and SDKs  
✅ **Production Ready** - Error handling, logging, monitoring  
✅ **Performance Optimized** - Pagination, caching, query optimization  

---

## Quick Reference

### Generate Endpoints
```python
generator = APIGenerator(config)
generator.create_node_endpoint("/nodes")
generator.create_relationship_endpoint("/relationships")
generator.create_query_endpoint("/query")
```

### Add Authentication
```python
generator.enable_authentication(
    auth_type="jwt",
    secret_key="your-secret"
)
```

### Enable Caching
```python
generator.enable_caching(
    ttl=3600,
    cache_backend="redis"
)
```

### Start Server
```python
generator.start_server(
    host="0.0.0.0",
    port=8000,
    debug=False
)
```

---

## Related Skills

- **Neo4j Integration** - Graph query execution
- **JanusGraph Connector** - Distributed graph database
- **RDF Triple Store Integration** - SPARQL querying
- **Graph Query Optimization** - Query performance tuning
- **GraphQL Graph Mapping** - GraphQL alternative
- **Authentication Systems** - API security
- **API Gateways** - Request routing and management

---

## Resources

- [REST API Best Practices](https://restfulapi.net/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Express.js Guide](https://expressjs.com/)
- [HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
- [RESTful API Design](https://swagger.io/resources/articles/best-practices-in-api-design/)

---
 
**Version:** 1.0.0  
**Last Updated:** April 12, 2026
