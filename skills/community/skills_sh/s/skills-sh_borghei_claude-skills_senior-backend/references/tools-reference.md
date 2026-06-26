# Backend Tools Reference

Read this when running the API scaffolder, database migration tool, or load tester — full usage examples, flag tables, and sample output.

## Quick Start

```bash
# Generate API routes from OpenAPI spec
python scripts/api_scaffolder.py openapi.yaml --framework express --output src/routes/

# Analyze database schema and generate migrations
python scripts/database_migration_tool.py --connection postgres://localhost/mydb --analyze

# Load test an API endpoint
python scripts/api_load_tester.py https://api.example.com/users --concurrency 50 --duration 30
```

## Tools Overview

### 1. API Scaffolder

Generates API route handlers, middleware, and OpenAPI specifications from schema definitions.

**Input:** OpenAPI spec (YAML/JSON) or database schema
**Output:** Route handlers, validation middleware, TypeScript types

**Usage:**
```bash
# Generate Express routes from OpenAPI spec
python scripts/api_scaffolder.py openapi.yaml --framework express --output src/routes/

# Output:
# Generated 12 route handlers in src/routes/
# - GET /users (listUsers)
# - POST /users (createUser)
# - GET /users/{id} (getUser)
# - PUT /users/{id} (updateUser)
# - DELETE /users/{id} (deleteUser)
# ...
# Created validation middleware: src/middleware/validators.ts
# Created TypeScript types: src/types/api.ts

# Generate from database schema
python scripts/api_scaffolder.py --from-db postgres://localhost/mydb --output src/routes/

# Generate OpenAPI spec from existing routes
python scripts/api_scaffolder.py src/routes/ --generate-spec --output openapi.yaml
```

**Supported Frameworks:**
- Express.js (`--framework express`)
- Fastify (`--framework fastify`)
- Koa (`--framework koa`)

### 2. Database Migration Tool

Analyzes database schemas, detects changes, and generates migration files with rollback support.

**Input:** Database connection string or schema files
**Output:** Migration files, schema diff report, optimization suggestions

**Usage:**
```bash
# Analyze current schema and suggest optimizations
python scripts/database_migration_tool.py --connection postgres://localhost/mydb --analyze

# Output:
# === Database Analysis Report ===
# Tables: 24
# Total rows: 1,247,832
#
# MISSING INDEXES (5 found):
#   orders.user_id - 847ms avg query time, ADD INDEX recommended
#   products.category_id - 234ms avg query time, ADD INDEX recommended
#
# N+1 QUERY RISKS (3 found):
#   users -> orders relationship (no eager loading)
#
# SUGGESTED MIGRATIONS:
#   1. Add index on orders(user_id)
#   2. Add index on products(category_id)
#   3. Add composite index on order_items(order_id, product_id)

# Generate migration from schema diff
python scripts/database_migration_tool.py --connection postgres://localhost/mydb \
  --compare schema/v2.sql --output migrations/

# Output:
# Generated migration: migrations/20240115_add_user_indexes.sql
# Generated rollback: migrations/20240115_add_user_indexes_rollback.sql

# Dry-run a migration
python scripts/database_migration_tool.py --connection postgres://localhost/mydb \
  --migrate migrations/20240115_add_user_indexes.sql --dry-run
```

### 3. API Load Tester

Performs HTTP load testing with configurable concurrency, measuring latency percentiles and throughput.

**Input:** API endpoint URL and test configuration
**Output:** Performance report with latency distribution, error rates, throughput metrics

**Usage:**
```bash
# Basic load test
python scripts/api_load_tester.py https://api.example.com/users --concurrency 50 --duration 30

# Output:
# === Load Test Results ===
# Target: https://api.example.com/users
# Duration: 30s | Concurrency: 50
#
# THROUGHPUT:
#   Total requests: 15,247
#   Requests/sec: 508.2
#   Successful: 15,102 (99.0%)
#   Failed: 145 (1.0%)
#
# LATENCY (ms):
#   Min: 12
#   Avg: 89
#   P50: 67
#   P95: 198
#   P99: 423
#   Max: 1,247
#
# ERRORS:
#   Connection timeout: 89
#   HTTP 503: 56
#
# RECOMMENDATION: P99 latency (423ms) exceeds 200ms target.
# Consider: connection pooling, query optimization, or horizontal scaling.

# Test with custom headers and body
python scripts/api_load_tester.py https://api.example.com/orders \
  --method POST \
  --header "Authorization: Bearer token123" \
  --body '{"product_id": 1, "quantity": 2}' \
  --concurrency 100 \
  --duration 60

# Compare two endpoints
python scripts/api_load_tester.py https://api.example.com/v1/users https://api.example.com/v2/users \
  --compare --concurrency 50 --duration 30
```

## Common Commands

```bash
# API Development
python scripts/api_scaffolder.py openapi.yaml --framework express
python scripts/api_scaffolder.py src/routes/ --generate-spec

# Database Operations
python scripts/database_migration_tool.py --connection $DATABASE_URL --analyze
python scripts/database_migration_tool.py --connection $DATABASE_URL --migrate file.sql

# Performance Testing
python scripts/api_load_tester.py https://api.example.com/endpoint --concurrency 50
python scripts/api_load_tester.py https://api.example.com/endpoint --compare baseline.json
```

## Tool Reference

### api_scaffolder.py

**Purpose:** Generate Express.js/Fastify/Koa route handlers, Zod validators, and TypeScript types from an OpenAPI specification.

**Usage:**
```bash
python scripts/api_scaffolder.py <spec> [flags]
```

**Flags:**

| Flag | Short | Type | Default | Description |
|------|-------|------|---------|-------------|
| `spec` | | positional | *(required)* | Path to OpenAPI specification file (YAML or JSON) |
| `--output` | `-o` | string | `./generated` | Output directory for generated files |
| `--framework` | `-f` | choice | `express` | Target framework: `express`, `fastify`, or `koa` |
| `--types-only` | | flag | `false` | Generate only TypeScript type definitions, skip routes and validators |
| `--verbose` | `-v` | flag | `false` | Enable verbose output (shows spec title/version) |
| `--json` | | flag | `false` | Output results summary as JSON |

**Example:**
```bash
python scripts/api_scaffolder.py openapi.yaml --framework express --output src/routes/ --verbose
```
```
API Scaffolder - Express
Spec: openapi.yaml
Output: src/routes/
--------------------------------------------------
Loaded: User Service API v1.0.0
  Generated: src/routes/types.ts
  Generated: src/routes/validators.ts
  Generated: src/routes/users.routes.ts (5 handlers)
  Generated: src/routes/index.ts
--------------------------------------------------
Generated 5 route handlers
Generated 3 type definitions
Output: src/routes/
```

**Output Formats:** Human-readable console output by default. Add `--json` for machine-readable JSON with `status`, `generated_files`, `routes_count`, and `types_count` fields.

### database_migration_tool.py

**Purpose:** Analyze SQL schema files for issues, compare schemas to generate migrations with rollback scripts, and suggest missing indexes.

**Usage:**
```bash
python scripts/database_migration_tool.py <schema> [flags]
```

**Flags:**

| Flag | Short | Type | Default | Description |
|------|-------|------|---------|-------------|
| `schema` | | positional | *(required)* | Path to SQL schema file |
| `--analyze` | | flag | `false` | Analyze schema for issues and optimizations (default mode if no other mode specified) |
| `--compare` | | string | | Path to a second schema file to compare against and generate migration |
| `--suggest-indexes` | | flag | `false` | Generate index suggestions for foreign keys, filter columns, and timestamps |
| `--output` | `-o` | string | | Output directory for generated migration files |
| `--verbose` | `-v` | flag | `false` | Enable verbose output (shows parsed table count and info-level suggestions) |
| `--json` | | flag | `false` | Output results as JSON |

**Example:**
```bash
python scripts/database_migration_tool.py schema.sql --analyze --verbose
```
```
Database Migration Tool
Schema: schema.sql
--------------------------------------------------
Parsed 8 tables

Analysis Results:
  Tables: 8
  Errors: 1
  Warnings: 3
  Suggestions: 7

ERRORS:
  [audit_log] Table 'audit_log' has no primary key
    Suggestion: Add a primary key column (e.g., 'id SERIAL PRIMARY KEY')

WARNINGS:
  [orders] Foreign key column 'user_id' is not indexed
    Suggestion: CREATE INDEX idx_orders_user_id ON orders(user_id);
```

**Output Formats:** Human-readable console output by default. Add `--json` for structured JSON with `issues_detail` array containing severity, category, table, message, and suggestion for each finding. When using `--compare --output`, generates timestamped `_migration.sql` and `_migration_rollback.sql` files.

### api_load_tester.py

**Purpose:** Perform HTTP load testing with configurable concurrency, measuring latency percentiles (p50/p90/p95/p99), throughput, error rates, and optional endpoint comparison.

**Usage:**
```bash
python scripts/api_load_tester.py <urls...> [flags]
```

**Flags:**

| Flag | Short | Type | Default | Description |
|------|-------|------|---------|-------------|
| `urls` | | positional | *(required)* | One or more URLs to test |
| `--method` | `-m` | choice | `GET` | HTTP method: `GET`, `POST`, `PUT`, `PATCH`, or `DELETE` |
| `--body` | `-b` | string | | Request body as a JSON string |
| `--header` | `-H` | string (repeatable) | | HTTP header in `"Name: Value"` format; can be specified multiple times |
| `--concurrency` | `-c` | int | `10` | Number of concurrent request threads |
| `--duration` | `-d` | float | `10.0` | Test duration in seconds |
| `--timeout` | `-t` | float | `30.0` | Per-request timeout in seconds |
| `--compare` | | flag | `false` | Compare two endpoints side-by-side (requires two URLs) |
| `--no-verify-ssl` | | flag | `false` | Disable SSL certificate verification |
| `--verbose` | `-v` | flag | `false` | Enable verbose output (shows transfer bytes and throughput Mbps) |
| `--json` | | flag | `false` | Output results as JSON |
| `--output` | `-o` | string | | File path to write JSON results |

**Example:**
```bash
python scripts/api_load_tester.py https://api.example.com/users \
  --method GET \
  --header "Authorization: Bearer tok_abc123" \
  --concurrency 50 \
  --duration 30 \
  --verbose
```
```
============================================================
LOAD TEST RESULTS
============================================================

Target: https://api.example.com/users
Method: GET
Duration: 30.2s
Concurrency: 50

THROUGHPUT:
  Total requests: 14,832
  Requests/sec: 491.1
  Successful: 14,710 (99.2%)
  Failed: 122

LATENCY (ms):
  Min: 11.3
  Avg: 92.4
  P50: 71.2
  P90: 165.8
  P95: 201.3
  P99: 387.6
  Max: 1,102.5
  StdDev: 89.2

TRANSFER:
  Total bytes: 45,291,520
  Throughput: 12.01 Mbps

RECOMMENDATIONS:
  Warning: P99 latency (388ms) exceeds 500ms
    Consider: Connection pooling, query optimization, caching
  Performance looks good for this load level
============================================================
```

**Output Formats:** Human-readable console report by default with latency distribution and recommendations. Add `--json` for structured JSON output. Use `--output results.json` to write results to a file. When using `--compare` with two URLs, outputs a side-by-side metric comparison table.
