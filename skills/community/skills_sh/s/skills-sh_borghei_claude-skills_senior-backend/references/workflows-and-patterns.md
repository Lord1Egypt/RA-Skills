# Backend Workflows & Patterns

Read this when designing an API, optimizing a database, hardening security, or looking up common response/index patterns, troubleshooting, and the success bar.

## Backend Development Workflows

### API Design Workflow

Use when designing a new API or refactoring existing endpoints.

**Step 1: Define resources and operations**
```yaml
# openapi.yaml
openapi: 3.0.3
info:
  title: User Service API
  version: 1.0.0
paths:
  /users:
    get:
      summary: List users
      parameters:
        - name: limit
          in: query
          schema:
            type: integer
            default: 20
    post:
      summary: Create user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUser'
```

**Step 2: Generate route scaffolding**
```bash
python scripts/api_scaffolder.py openapi.yaml --framework express --output src/routes/
```

**Step 3: Implement business logic**
```typescript
// src/routes/users.ts (generated, then customized)
export const createUser = async (req: Request, res: Response) => {
  const { email, name } = req.body;

  // Add business logic
  const user = await userService.create({ email, name });

  res.status(201).json(user);
};
```

**Step 4: Add validation middleware**
```bash
# Validation is auto-generated from OpenAPI schema
# src/middleware/validators.ts includes:
# - Request body validation
# - Query parameter validation
# - Path parameter validation
```

**Step 5: Generate updated OpenAPI spec**
```bash
python scripts/api_scaffolder.py src/routes/ --generate-spec --output openapi.yaml
```

### Database Optimization Workflow

Use when queries are slow or database performance needs improvement.

**Step 1: Analyze current performance**
```bash
python scripts/database_migration_tool.py --connection $DATABASE_URL --analyze
```

**Step 2: Identify slow queries**
```sql
-- Check query execution plans
EXPLAIN ANALYZE SELECT * FROM orders
WHERE user_id = 123
ORDER BY created_at DESC
LIMIT 10;

-- Look for: Seq Scan (bad), Index Scan (good)
```

**Step 3: Generate index migrations**
```bash
python scripts/database_migration_tool.py --connection $DATABASE_URL \
  --suggest-indexes --output migrations/
```

**Step 4: Test migration (dry-run)**
```bash
python scripts/database_migration_tool.py --connection $DATABASE_URL \
  --migrate migrations/add_indexes.sql --dry-run
```

**Step 5: Apply and verify**
```bash
# Apply migration
python scripts/database_migration_tool.py --connection $DATABASE_URL \
  --migrate migrations/add_indexes.sql

# Verify improvement
python scripts/database_migration_tool.py --connection $DATABASE_URL --analyze
```

### Security Hardening Workflow

Use when preparing an API for production or after a security review.

**Step 1: Review authentication setup**
```typescript
// Verify JWT configuration
const jwtConfig = {
  secret: process.env.JWT_SECRET,  // Must be from env, never hardcoded
  expiresIn: '1h',                 // Short-lived tokens
  algorithm: 'RS256'               // Prefer asymmetric
};
```

**Step 2: Add rate limiting**
```typescript
import rateLimit from 'express-rate-limit';

const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15 minutes
  max: 100,                   // 100 requests per window
  standardHeaders: true,
  legacyHeaders: false,
});

app.use('/api/', apiLimiter);
```

**Step 3: Validate all inputs**
```typescript
import { z } from 'zod';

const CreateUserSchema = z.object({
  email: z.string().email().max(255),
  name: z.string().min(1).max(100),
  age: z.number().int().positive().optional()
});

// Use in route handler
const data = CreateUserSchema.parse(req.body);
```

**Step 4: Load test with attack patterns**
```bash
# Test rate limiting
python scripts/api_load_tester.py https://api.example.com/login \
  --concurrency 200 --duration 10 --expect-rate-limit

# Test input validation
python scripts/api_load_tester.py https://api.example.com/users \
  --method POST \
  --body '{"email": "not-an-email"}' \
  --expect-status 400
```

**Step 5: Review security headers**
```typescript
import helmet from 'helmet';

app.use(helmet({
  contentSecurityPolicy: true,
  crossOriginEmbedderPolicy: true,
  crossOriginOpenerPolicy: true,
  crossOriginResourcePolicy: true,
  hsts: { maxAge: 31536000, includeSubDomains: true },
}));
```

## Common Patterns Quick Reference

### REST API Response Format
```json
{
  "data": { "id": 1, "name": "John" },
  "meta": { "requestId": "abc-123" }
}
```

### Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "details": [{ "field": "email", "message": "must be valid email" }]
  },
  "meta": { "requestId": "abc-123" }
}
```

### HTTP Status Codes
| Code | Use Case |
|------|----------|
| 200 | Success (GET, PUT, PATCH) |
| 201 | Created (POST) |
| 204 | No Content (DELETE) |
| 400 | Validation error |
| 401 | Authentication required |
| 403 | Permission denied |
| 404 | Resource not found |
| 429 | Rate limit exceeded |
| 500 | Internal server error |

### Database Index Strategy
```sql
-- Single column (equality lookups)
CREATE INDEX idx_users_email ON users(email);

-- Composite (multi-column queries)
CREATE INDEX idx_orders_user_status ON orders(user_id, status);

-- Partial (filtered queries)
CREATE INDEX idx_orders_active ON orders(created_at) WHERE status = 'active';

-- Covering (avoid table lookup)
CREATE INDEX idx_users_email_name ON users(email) INCLUDE (name);
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `api_scaffolder.py` generates empty route files | OpenAPI spec missing `operationId` fields or paths use unsupported HTTP methods | Add `operationId` to each operation; verify methods are GET, POST, PUT, PATCH, or DELETE |
| `database_migration_tool.py` parses zero tables | SQL file uses non-standard DDL syntax or multi-line comments break regex parsing | Ensure `CREATE TABLE` statements end with `;` and remove block comments (`/* ... */`) before analysis |
| Load tester reports 100% failure rate | Target URL unreachable, SSL verification failing, or firewall blocking concurrent connections | Verify URL manually with `curl`; try `--no-verify-ssl` for self-signed certs; reduce `--concurrency` |
| Generated TypeScript types show `unknown` for all fields | OpenAPI schema uses `$ref` references to external files or missing `components/schemas` section | Inline referenced schemas or ensure all `$ref` targets exist within the same spec file |
| Migration diff reports "No changes" when changes exist | Column type differences are case-sensitive; `VARCHAR(255)` vs `varchar(255)` treated as different | Normalize casing in schema files; the parser converts types to uppercase internally |
| Load tester hangs after duration expires | Worker threads blocked on slow connections that exceed the default 30s timeout | Set `--timeout` lower than `--duration` (e.g., `--timeout 5 --duration 30`) to prevent thread starvation |
| Zod validators missing for nested objects | Deeply nested `$ref` chains not fully resolved by the scaffolder | Flatten nested schemas in the OpenAPI spec or manually extend the generated validators |

## Success Criteria

- **API p99 latency under 200ms** at production concurrency levels, verified by `api_load_tester.py`
- **Zero N+1 query patterns detected** in schema analysis via `database_migration_tool.py --analyze`
- **All foreign key columns indexed** with no "missing index" warnings from the migration tool
- **100% of generated routes include input validation** middleware (Zod schemas auto-generated from OpenAPI spec)
- **Success rate above 99.5%** during sustained load tests at target concurrency for 60+ seconds
- **Every migration paired with a rollback script** to enable zero-downtime deployment reversals
- **API response format consistency** across all endpoints following the standardized `data`/`error`/`meta` envelope pattern
