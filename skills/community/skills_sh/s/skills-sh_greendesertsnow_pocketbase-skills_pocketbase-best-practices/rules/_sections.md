# Section Definitions

This file defines the rule categories for PocketBase best practices. Rules are automatically assigned to sections based on their filename prefix.

---

## 1. Collection Design (coll)
**Impact:** CRITICAL
**Description:** Schema design, field types, relations, indexes, and collection type selection. Foundation for application architecture and long-term maintainability.

## 2. API Rules & Security (rules)
**Impact:** CRITICAL
**Description:** Access control rules, filter expressions, request context usage, and security patterns. Critical for protecting data and enforcing authorization.

## 3. Authentication (auth)
**Impact:** CRITICAL
**Description:** Password authentication, OAuth2 integration, token management, MFA setup, and auth collection configuration.

## 4. SDK Usage (sdk)
**Impact:** HIGH
**Description:** JavaScript SDK initialization, auth store patterns, error handling, request cancellation, and safe parameter binding.

## 5. Query Performance (query)
**Impact:** HIGH
**Description:** Pagination strategies, relation expansion, field selection, batch operations, and N+1 query prevention.

## 6. Realtime (realtime)
**Impact:** MEDIUM
**Description:** SSE subscriptions, event handling, connection management, and authentication with realtime.

## 7. File Handling (file)
**Impact:** MEDIUM
**Description:** File uploads, URL generation, thumbnail creation, and validation patterns.

## 8. Production & Deployment (deploy)
**Impact:** LOW-MEDIUM
**Description:** Backup strategies, configuration management, reverse proxy setup, and SQLite optimization.

## 9. Server-Side Extending (ext)
**Impact:** HIGH
**Description:** Extending PocketBase with Go or embedded JavaScript (JSVM) - event hooks, custom routes, transactions, cron jobs, filesystem, migrations, and safe server-side filter binding.
