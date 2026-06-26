# Pagination, Filtering, and Authentication

## Pagination Strategies

### Offset-Based (Simple)

```bash
GET /api/v1/users?page=2&per_page=20
```

**Pros:** Easy, supports "jump to page N"
**Cons:** Slow on large offsets, inconsistent with concurrent inserts

### Cursor-Based (Scalable)

```bash
GET /api/v1/users?cursor=eyJpZCI6MTIzfQ&limit=20
```

**Pros:** Consistent performance, stable with concurrent inserts
**Cons:** Cannot jump to arbitrary page

## Filtering, Sorting, and Search

### Filtering

```bash
# Simple equality
GET /api/v1/orders?status=active&customer_id=abc-123

# Comparison operators
GET /api/v1/products?price[gte]=10&price[lte]=100

# Multiple values
GET /api/v1/products?category=electronics,clothing
```

### Sorting

```bash
# Single field (- for descending)
GET /api/v1/products?sort=-created_at

# Multiple fields
GET /api/v1/products?sort=-featured,price,-created_at
```

### Full-Text Search

```bash
GET /api/v1/products?q=wireless+headphones
```

### Sparse Fieldsets

```bash
# Return only specified fields
GET /api/v1/users?fields=id,name,email
```

## Authentication and Authorization

### Token-Based Auth

```bash
GET /api/v1/users
Authorization: Bearer <your-api-token>
```

### Resource-Level Authorization

```typescript
app.get("/api/v1/orders/:id", async (req, res) => {
  const order = await Order.findById(req.params.id);
  if (!order) return res.status(404).json({ error: { code: "not_found" } });
  if (order.userId !== req.user.id) return res.status(403).json({ error: { code: "forbidden" } });
  return res.json({ data: order });
});
```

## Rate Limiting

### Response Headers

```bash
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640000000

# When exceeded
HTTP/1.1 429 Too Many Requests
Retry-After: 60
```

### Rate Limit Tiers

| Tier | Limit | Window |
|------|-------|--------|
| Anonymous | 30/min | Per IP |
| Authenticated | 100/min | Per user |
| Premium | 1000/min | Per API key |

## API Versioning Strategy

### URL Path Versioning (Recommended)

```bash
/api/v1/users
/api/v2/users
```

### Non-Breaking Changes (No Version Bump)

- Adding new fields to responses
- Adding new optional query parameters
- Adding new endpoints

### Breaking Changes (New Version)

- Removing or renaming fields
- Changing field types
- Changing URL structure
- Changing authentication method

### Deprecation Timeline

1. Announce deprecation (6 months notice)
2. Add `Sunset` header: `Sunset: Sat, 01 Jan 2026 00:00:00 GMT`
3. Return `410 Gone` after sunset date
