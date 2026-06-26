# API Design

REST, GraphQL, and gRPC patterns and best practices.

## REST APIs

### Principles
- Resource-based URLs
- HTTP methods (GET, POST, PUT, DELETE, PATCH)
- Stateless requests
- JSON responses

### Best Practices
- Use nouns for resources: `/users`, `/orders`
- Use HTTP status codes correctly
- Version APIs: `/v1/users`, `/v2/users`
- Pagination for collections
- Filtering, sorting, searching via query params

### Example Structure
```
GET    /api/v1/users            # List users
GET    /api/v1/users/:id        # Get user
POST   /api/v1/users            # Create user
PUT    /api/v1/users/:id        # Update user
DELETE /api/v1/users/:id        # Delete user
```

## GraphQL

### Principles
- Single endpoint
- Client-specified queries
- Strongly typed schema
- Introspection

### Best Practices
- Design schema first
- Use DataLoader for N+1 queries
- Implement query complexity limits
- Use subscriptions for real-time data
- Version via schema evolution

### Example Query
```graphql
query {
  user(id: "123") {
    name
    email
    orders {
      id
      total
    }
  }
}
```

## gRPC

### Principles
- Protocol Buffers for schema
- HTTP/2 transport
- Strong typing
- Streaming support

### Best Practices
- Define proto files first
- Use streaming for large datasets
- Implement proper error handling
- Use interceptors for cross-cutting concerns

### When to Use
- Internal microservices communication
- High-performance requirements
- Strong typing needed
- Streaming data

## API Versioning

### URL Versioning
```
/api/v1/users
/api/v2/users
```

### Header Versioning
```
Accept: application/vnd.api+json;version=1
```

### Best Practices
- Version from the start
- Maintain backward compatibility when possible
- Deprecate old versions with notice
- Document breaking changes

## Error Handling

### Standard Error Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": {
      "field": "email",
      "reason": "Invalid email format"
    }
  }
}
```

### HTTP Status Codes
- 200 OK - Success
- 201 Created - Resource created
- 400 Bad Request - Client error
- 401 Unauthorized - Authentication required
- 403 Forbidden - Authorization failed
- 404 Not Found - Resource not found
- 500 Internal Server Error - Server error

## Rate Limiting

- Implement rate limits to prevent abuse
- Use token bucket or sliding window algorithms
- Return appropriate headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`
- Provide clear error messages when limits exceeded

## Documentation

- Use OpenAPI/Swagger for REST APIs
- GraphQL schema serves as documentation
- Include examples for all endpoints
- Document authentication requirements
- Provide SDKs when possible
