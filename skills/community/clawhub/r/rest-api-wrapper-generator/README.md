# REST API Wrapper Generator

> Generate production-ready REST API endpoints to expose graph database operations and queries

## Directory Structure

```
rest-api-wrapper-generator/
├── README.md                      (This file - Quick reference)
├── SKILL.md                       (Skill definition with examples & best practices)
├── examples/
│   └── rest-api-examples.md       (5 complete production examples)
├── references/
│   └── rest-api-patterns.md       (30+ design patterns for REST APIs)
└── scripts/
    └── rest_api_generator.py      (Production-ready Python implementation)
```

## Quick Start

### Installation

```bash
pip install fastapi uvicorn pydantic
```

### Basic REST API Generation

```python
from rest_api_generator import APIGenerator, APIConfig, GraphDatabaseType

# Configure API
config = APIConfig(
    database_type=GraphDatabaseType.NEO4J,
    database_url="bolt://localhost:7687",
    api_title="Knowledge Graph API",
    api_version="1.0.0",
    enable_authentication=True
)

# Generate API
generator = APIGenerator(config)

# Create endpoints for node operations
generator.create_node_endpoint(
    path="/nodes",
    label="Person",
    properties=["name", "age", "email"]
)

# Create endpoints for relationship operations
generator.create_relationship_endpoint(
    path="/relationships",
    relationship_type="KNOWS",
    properties=["since"]
)

# Create endpoints for queries
generator.create_query_endpoint(
    path="/query",
    description="Execute custom queries"
)

# Start server
generator.start_server(host="0.0.0.0", port=8000)
```

## Features

✅ **Automatic REST Endpoint Generation**
- CRUD endpoints for nodes
- Relationship management endpoints
- Query execution endpoints
- Graph traversal endpoints

✅ **Multiple Database Support**
- Neo4j
- JanusGraph
- RDF Triple Stores
- TigerGraph

✅ **Request/Response Handling**
- Input validation using Pydantic
- Error handling and status codes
- JSON serialization
- Response formatting

✅ **Authentication & Authorization**
- JWT token support
- API key authentication
- Role-based access control
- Rate limiting

✅ **Documentation**
- Auto-generated Swagger/OpenAPI docs
- Endpoint documentation
- Example requests/responses
- Parameter descriptions

✅ **Advanced Features**
- Pagination for large result sets
- Filtering and sorting
- Batch operations
- Transaction support
- Caching support

## Key Concepts

### REST Principles
- RESTful architecture
- HTTP methods (GET, POST, PUT, DELETE)
- Proper status codes
- Resource-oriented design

### API Structure
- Base URL: `/api/v1`
- Resource paths: `/nodes`, `/relationships`, `/query`
- Resource IDs: `/nodes/{id}`
- Query parameters: `?limit=10&offset=20`

### HTTP Methods
- **GET** - Retrieve data (read-only)
- **POST** - Create new resources
- **PUT** - Update existing resources
- **DELETE** - Remove resources

### Request/Response Format
- JSON request bodies
- JSON response bodies
- Proper Content-Type headers
- Standard error responses

### Status Codes
- 200 OK - Success
- 201 Created - Resource created
- 400 Bad Request - Invalid input
- 401 Unauthorized - Authentication required
- 403 Forbidden - Permission denied
- 404 Not Found - Resource not found
- 500 Internal Server Error - Server error

## File Descriptions

| File | Purpose | Size |
|------|---------|------|
| README.md | Quick reference and getting started | This file |
| SKILL.md | Complete skill definition | 350+ lines |
| examples/rest-api-examples.md | 5 production API examples | 500+ lines |
| references/rest-api-patterns.md | 30+ REST API patterns | 450+ lines |
| scripts/rest_api_generator.py | Production Python implementation | 500+ lines |

## Common Use Cases

### 1. Knowledge Graph REST API
Expose Neo4j or other graph databases via REST endpoints

### 2. Microservices Integration
Expose graph operations to microservices architecture

### 3. Frontend Application Backend
Provide REST API for web/mobile frontends

### 4. Third-Party Integrations
Enable external systems to access graph data

### 5. Multi-Client Support
Support multiple client types (web, mobile, desktop)

## Integration Points

This skill integrates with:
- **Neo4j Integration** - Graph database querying
- **JanusGraph Connector** - Distributed graph access
- **RDF Triple Store Integration** - Semantic queries
- **Graph Query Optimization** - Performance tuning
- **GraphQL Graph Mapping** - GraphQL alternative
- **Authentication Systems** - API security
- **API Gateways** - Request routing

## Quick Examples

### Create a Node Endpoint
```python
generator.create_node_endpoint(
    path="/nodes",
    label="Person",
    properties=["name", "age", "email"],
    methods=["GET", "POST"]
)
```

### Create a Relationship Endpoint
```python
generator.create_relationship_endpoint(
    path="/relationships",
    relationship_type="KNOWS",
    properties=["since", "strength"],
    methods=["GET", "POST", "DELETE"]
)
```

### Create a Query Endpoint
```python
generator.create_query_endpoint(
    path="/query",
    description="Execute custom queries",
    requires_authentication=True
)
```

### Add Pagination
```python
generator.enable_pagination(
    default_limit=20,
    max_limit=100
)
```

### Add Filtering
```python
generator.enable_filtering(
    filterable_fields=["name", "age", "status"]
)
```

## Performance Tips

1. **Pagination** - Always paginate large result sets
2. **Filtering** - Provide filter endpoints to reduce data transfer
3. **Caching** - Cache frequently accessed resources
4. **Indexing** - Index frequently queried properties
5. **Rate Limiting** - Prevent abuse and overload
6. **Connection Pooling** - Reuse database connections
7. **Response Compression** - Compress large responses

## Security Best Practices

1. **Authentication** - Require authentication for sensitive endpoints
2. **Authorization** - Implement role-based access control
3. **Input Validation** - Validate all input data
4. **Rate Limiting** - Limit requests per user/IP
5. **HTTPS** - Use HTTPS in production
6. **CORS** - Configure CORS properly
7. **Logging** - Log all API access

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Database connection fails | Verify database URL and credentials |
| API not responding | Check server logs, verify port is open |
| Authentication fails | Verify JWT tokens or API keys |
| Slow responses | Add indexes, enable caching, check queries |
| CORS errors | Configure CORS settings properly |

## Related Documentation

- See **SKILL.md** for complete skill definition
- See **examples/rest-api-examples.md** for detailed examples
- See **references/rest-api-patterns.md** for design patterns
- See **scripts/rest_api_generator.py** for implementation details

## Next Steps

1. Review the SKILL.md for comprehensive documentation
2. Check examples/rest-api-examples.md for your use case
3. Look at references/rest-api-patterns.md for design patterns
4. Use scripts/rest_api_generator.py as reference implementation

---

**Status:** ✅ Production Ready | **Version:** 1.0.0 | **Last Updated:** April 12, 2026

