# REST API Design Patterns

This document contains 30+ production-ready design patterns for building REST APIs that wrap graph databases. Each pattern includes request/response examples, best practices, and use cases.

---

## Table of Contents

1. [CRUD Operation Patterns](#crud-operation-patterns)
2. [Query Patterns](#query-patterns)
3. [Relationship Patterns](#relationship-patterns)
4. [Pagination & Filtering Patterns](#pagination--filtering-patterns)
5. [Error Handling Patterns](#error-handling-patterns)
6. [Authentication Patterns](#authentication-patterns)
7. [Response Format Patterns](#response-format-patterns)
8. [Advanced Patterns](#advanced-patterns)

---

## CRUD Operation Patterns

### Pattern 1: Create Resource

**Description:** Create a new resource in the graph

**Request:**
```http
POST /api/v1/nodes
Content-Type: application/json

{
  "label": "Person",
  "properties": {
    "name": "Alice",
    "email": "alice@example.com"
  }
}
```

**Response (201):**
```json
{
  "id": "n1",
  "label": "Person",
  "properties": {"name": "Alice", "email": "alice@example.com"},
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Use Case:** Creating new entities in the graph

### Pattern 2: Read Resource

**Description:** Retrieve a specific resource

**Request:**
```http
GET /api/v1/nodes/n1
```

**Response (200):**
```json
{
  "id": "n1",
  "label": "Person",
  "properties": {"name": "Alice", "email": "alice@example.com"},
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Use Case:** Getting entity details

### Pattern 3: Update Resource

**Description:** Update existing resource

**Request:**
```http
PUT /api/v1/nodes/n1
Content-Type: application/json

{
  "properties": {
    "email": "alice.new@example.com",
    "age": 31
  }
}
```

**Response (200):**
```json
{
  "id": "n1",
  "label": "Person",
  "properties": {"name": "Alice", "email": "alice.new@example.com", "age": 31},
  "updated_at": "2024-01-15T11:00:00Z"
}
```

**Use Case:** Modifying entity properties

### Pattern 4: Delete Resource

**Description:** Remove a resource

**Request:**
```http
DELETE /api/v1/nodes/n1
```

**Response (204 No Content)**

**Use Case:** Deleting entities

### Pattern 5: List Resources

**Description:** Get collection of resources

**Request:**
```http
GET /api/v1/nodes?limit=20&offset=0
```

**Response (200):**
```json
{
  "data": [
    {"id": "n1", "label": "Person", "properties": {"name": "Alice"}},
    {"id": "n2", "label": "Person", "properties": {"name": "Bob"}}
  ],
  "total": 100,
  "limit": 20,
  "offset": 0
}
```

**Use Case:** Listing all resources

### Pattern 6: Partial Update

**Description:** Update specific fields only

**Request:**
```http
PATCH /api/v1/nodes/n1
Content-Type: application/json

{
  "properties": {
    "age": 32
  }
}
```

**Response (200):**
```json
{
  "id": "n1",
  "properties": {"name": "Alice", "email": "alice@example.com", "age": 32}
}
```

**Use Case:** Partial updates without full object replacement

---

## Query Patterns

### Pattern 7: Simple Property Filter

**Description:** Filter by single property

**Request:**
```http
GET /api/v1/nodes?filter[name]=Alice
```

**Response:**
```json
{
  "data": [
    {"id": "n1", "name": "Alice"}
  ]
}
```

**Use Case:** Finding resources by property value

### Pattern 8: Range Filter

**Description:** Filter by value range

**Request:**
```http
GET /api/v1/nodes?filter[age][gte]=25&filter[age][lte]=35
```

**Response:**
```json
{
  "data": [
    {"id": "n1", "name": "Alice", "age": 30},
    {"id": "n2", "name": "Bob", "age": 28}
  ]
}
```

**Use Case:** Range-based filtering

### Pattern 9: Multiple Filters

**Description:** Combine multiple filter conditions

**Request:**
```http
GET /api/v1/nodes?filter[name]=Alice&filter[status]=active&filter[department]=eng
```

**Response:**
```json
{
  "data": [...]
}
```

**Use Case:** Complex filtering with multiple criteria

### Pattern 10: Text Search

**Description:** Full-text search across properties

**Request:**
```http
GET /api/v1/nodes/search?q=alice&fields=name,email&limit=10
```

**Response:**
```json
{
  "results": [
    {"id": "n1", "name": "Alice", "score": 1.0},
    {"id": "n5", "email": "alice.backup@example.com", "score": 0.8}
  ]
}
```

**Use Case:** Full-text search

### Pattern 11: Sorting

**Description:** Sort results by property

**Request:**
```http
GET /api/v1/nodes?sort=name
GET /api/v1/nodes?sort=-age
GET /api/v1/nodes?sort=name,age
```

**Response:**
```json
{
  "data": [...]
}
```

**Use Case:** Ordered result sets

### Pattern 12: Field Selection

**Description:** Return only specific fields

**Request:**
```http
GET /api/v1/nodes/n1?fields=name,email,age
```

**Response:**
```json
{
  "id": "n1",
  "name": "Alice",
  "email": "alice@example.com",
  "age": 30
}
```

**Use Case:** Bandwidth optimization

---

## Relationship Patterns

### Pattern 13: Create Relationship

**Description:** Create edge between nodes

**Request:**
```http
POST /api/v1/relationships
Content-Type: application/json

{
  "from_node_id": "n1",
  "to_node_id": "n2",
  "relationship_type": "KNOWS",
  "properties": {"since": "2020-01-15"}
}
```

**Response (201):**
```json
{
  "id": "r1",
  "from_node_id": "n1",
  "to_node_id": "n2",
  "relationship_type": "KNOWS",
  "properties": {"since": "2020-01-15"}
}
```

**Use Case:** Creating relationships

### Pattern 14: Get Related Resources

**Description:** Get nodes connected to a node

**Request:**
```http
GET /api/v1/nodes/n1/related?relationship_type=KNOWS
```

**Response:**
```json
{
  "related": [
    {"id": "n2", "label": "Person", "name": "Bob", "relationship": "KNOWS"}
  ]
}
```

**Use Case:** Finding connected nodes

### Pattern 15: Get Neighbors

**Description:** Get immediate neighbors of a node

**Request:**
```http
GET /api/v1/nodes/n1/neighbors?limit=20
```

**Response:**
```json
{
  "neighbors": [
    {"id": "n2", "label": "Person", "name": "Bob"},
    {"id": "n3", "label": "Person", "name": "Charlie"}
  ],
  "total": 150
}
```

**Use Case:** Social graphs, connected entities

### Pattern 16: Delete Relationship

**Description:** Remove edge between nodes

**Request:**
```http
DELETE /api/v1/relationships/r1
```

**Response (204 No Content)**

**Use Case:** Removing relationships

---

## Pagination & Filtering Patterns

### Pattern 17: Offset-Based Pagination

**Description:** Traditional pagination with offset

**Request:**
```http
GET /api/v1/nodes?limit=20&offset=40
```

**Response:**
```json
{
  "data": [...],
  "total": 500,
  "limit": 20,
  "offset": 40,
  "has_next": true,
  "has_prev": true
}
```

**Use Case:** Standard pagination

### Pattern 18: Cursor-Based Pagination

**Description:** Cursor pagination for large datasets

**Request:**
```http
GET /api/v1/nodes?limit=20&cursor=abc123def456
```

**Response:**
```json
{
  "data": [...],
  "next_cursor": "xyz789uvw012",
  "prev_cursor": "foo123bar456",
  "has_next": true
}
```

**Use Case:** Large dataset pagination

### Pattern 19: Limit Validation

**Description:** Enforce maximum limits

```python
@app.get("/nodes")
def list_nodes(limit: int = Query(20, le=100)):  # Max 100
    """Limit parameter capped at 100"""
    pass
```

**Use Case:** API rate limiting

### Pattern 20: Default Pagination

**Description:** Apply default pagination

```python
@app.get("/nodes")
def list_nodes(limit: int = Query(20), offset: int = Query(0)):
    """Default limit 20, offset 0"""
    pass
```

**Use Case:** Consistent pagination defaults

---

## Error Handling Patterns

### Pattern 21: Resource Not Found

**Request:**
```http
GET /api/v1/nodes/nonexistent
```

**Response (404):**
```json
{
  "error": "not_found",
  "message": "Node not found",
  "code": 404
}
```

**Use Case:** Missing resources

### Pattern 22: Validation Error

**Request:**
```http
POST /api/v1/nodes
{
  "label": "Person"
}
```

**Response (400):**
```json
{
  "error": "validation_error",
  "message": "Validation failed",
  "details": {
    "properties.name": "Name is required"
  }
}
```

**Use Case:** Input validation

### Pattern 23: Conflict Error

**Request:**
```http
POST /api/v1/nodes
{
  "id": "n1",
  "label": "Person"
}
```

**Response (409):**
```json
{
  "error": "conflict",
  "message": "Node already exists",
  "code": 409
}
```

**Use Case:** Duplicate resources

### Pattern 24: Server Error

**Response (500):**
```json
{
  "error": "internal_error",
  "message": "Internal server error",
  "request_id": "req-123456"
}
```

**Use Case:** Unexpected errors

### Pattern 25: Rate Limit Error

**Response (429):**
```json
{
  "error": "rate_limit_exceeded",
  "message": "Rate limit exceeded",
  "retry_after": 60
}
```

**Use Case:** Rate limiting

---

## Authentication Patterns

### Pattern 26: Bearer Token Authentication

**Request:**
```http
GET /api/v1/nodes
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

**Use Case:** JWT authentication

### Pattern 27: API Key Authentication

**Request:**
```http
GET /api/v1/nodes
X-API-Key: sk_live_4242424242424242
```

**Use Case:** API key-based access

### Pattern 28: Login Endpoint

**Request:**
```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "user",
  "password": "password"
}
```

**Response:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "expires_in": 3600
}
```

**Use Case:** Token generation

### Pattern 29: Role-Based Access Control

```python
@app.get("/admin/nodes")
@require_auth(roles=["admin"])
def admin_nodes():
    """Only admin users can access"""
    pass
```

**Use Case:** Permission-based access

---

## Response Format Patterns

### Pattern 30: Standard Success Response

```json
{
  "status": "success",
  "data": {...},
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Pattern 31: Envelope Response

```json
{
  "success": true,
  "data": {...},
  "meta": {
    "version": "1.0.0",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

### Pattern 32: Streaming Response

**Request:**
```http
GET /api/v1/nodes?stream=true
```

**Response:**
```
{"id": "n1", ...}
{"id": "n2", ...}
{"id": "n3", ...}
```

**Use Case:** Large result sets

---

## Advanced Patterns

### Pattern 33: Batch Operations

**Request:**
```http
POST /api/v1/batch
Content-Type: application/json

{
  "operations": [
    {"method": "POST", "path": "/nodes", "body": {...}},
    {"method": "POST", "path": "/relationships", "body": {...}}
  ]
}
```

**Response:**
```json
{
  "results": [
    {"status": 201, "body": {...}},
    {"status": 201, "body": {...}}
  ]
}
```

### Pattern 34: Async Operations

**Request:**
```http
POST /api/v1/async-query
Content-Type: application/json

{
  "query": "MATCH (n) RETURN n"
}
```

**Response (202):**
```json
{
  "task_id": "task-123456",
  "status": "processing",
  "status_url": "/api/v1/tasks/task-123456"
}
```

### Pattern 35: Webhooks

**Request:**
```http
POST /api/v1/webhooks
Content-Type: application/json

{
  "event": "node.created",
  "callback_url": "https://example.com/webhook",
  "active": true
}
```

---

## Summary

**30+ Patterns Covered:**
- ✅ 6 CRUD patterns
- ✅ 6 Query patterns
- ✅ 4 Relationship patterns
- ✅ 4 Pagination patterns
- ✅ 5 Error handling patterns
- ✅ 4 Authentication patterns
- ✅ 3 Response format patterns
- ✅ 3 Advanced patterns

Each pattern includes:
- Request/response examples
- HTTP status codes
- Error handling
- Use cases
- Best practices

---

**Last Updated:** April 12, 2026  
**REST API Version:** 1.1

