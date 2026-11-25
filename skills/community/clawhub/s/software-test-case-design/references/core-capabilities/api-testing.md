# API Testing

> This document defines the specific test dimensions and strategy points for API testing. It complements the other test types.

---

## Contents

| Line | Section |
|------|------|
| 23 | 1. Functional Testing |
| 35 | 2. Status Code Verification |
| 52 | 3. Data Validation |
| 62 | 4. Authentication and Authorization |
| 71 | 5. Security Testing |
| 86 | 6. Error Handling |
| 96 | 7. Pagination and Sorting |
| 105 | 8. Search and Filtering |
| 114 | 9. Version Compatibility |

---

## 1. Functional Testing

| Test scenario | Test points |
|---------|---------|
| GET requests | Query single / list data normally; query with parameters; handling of empty / wrongly typed parameters |
| POST requests | Create resources normally; required field validation; field format validation; handling of duplicate creation |
| PUT/PATCH requests | Full update / partial update; updating a non-existent resource; handling of concurrent updates |
| DELETE requests | Normal deletion; deleting a non-existent resource; cascading deletion; soft deletion |
| Batch operations | Batch create / update / delete; handling of partial success; transaction rollback |

---

## 2. Status Code Verification

| Status code | Description |
|-------|------|
| 200 OK | Normal response |
| 201 Created | Created successfully |
| 204 No Content | Deleted successfully |
| 400 Bad Request | Parameter error |
| 401 Unauthorized | Not authenticated |
| 403 Forbidden | No permission |
| 404 Not Found | Resource not found |
| 409 Conflict | Resource conflict |
| 422 Unprocessable | Validation failed |
| 500 Internal Error | Server error |

---

## 3. Data Validation

| Test scenario | Test points |
|---------|---------|
| Field validation | Required fields, type, length, format, range |
| Business rules | Uniqueness constraints, foreign key constraints, state transition rules |
| Data consistency | Verify database writes; verify cache synchronization |

---

## 4. Authentication and Authorization

| Test scenario | Test points |
|---------|---------|
| Token authentication | Token generation, refresh, expiration, revocation |
| Access control | Role permissions, resource permissions, data permissions |

---

## 5. Security Testing

| Test scenario | Test points |
|---------|---------|
| Injection attacks | SQL injection (verify parameterized queries), NoSQL injection, command injection |
| Unauthorized access | Horizontal privilege escalation (IDOR, changing a resource ID to access others' data), vertical privilege escalation (a regular token accessing admin APIs) |
| Mass assignment | Add read-only fields (e.g., role, isAdmin, balance) to the request body and verify they are rejected |
| API rate limiting | Many requests in a short time (> 100 requests/second); verify 429 is returned |
| Sensitive data exposure | Whether the response returns password hashes, tokens, internal IPs, or other sensitive fields; whether error stacks expose framework versions |
| Security headers | X-Content-Type-Options, X-Frame-Options, CSP, HSTS, and other security response headers |
| JWT security | Unsigned token (alg=none), expired token, tampered payload, key brute-forcing |
| Parameter pollution | Duplicate parameters (?id=1&id=2), array injection (?id[]=1&id[]=2), HTTP Parameter Pollution |

---

## 6. Error Handling

| Test scenario | Test points |
|---------|---------|
| Error responses | Standardized error codes; clear error messages |
| Exception handling | Database exceptions, third-party service exceptions, network exceptions, timeout handling |
| Retry mechanism | Automatic retry; retry count limit; idempotency guarantee |

---

## 7. Pagination and Sorting

| Test scenario | Test points |
|---------|---------|
| Pagination | Page number parameter, page size, total count, out-of-range handling |
| Sorting | Single-field / multi-field sorting; sort direction; default sorting |

---

## 8. Search and Filtering

| Test scenario | Test points |
|---------|---------|
| Search | Exact search, fuzzy search, full-text search, multi-condition combinations |
| Filtering | Time range, status, category, custom filters |

---

## 9. Version Compatibility

| Test scenario | Test points |
|---------|---------|
| Multiple versions coexisting | Request and response structures of the old version (e.g., /v1) remain unchanged; new fields in the new version (e.g., /v2) do not affect old-version callers |
| Invalid version number | Requesting a non-existent version (e.g., /v99) returns 404 or a clear error message |
| Deprecated fields and APIs | Deprecated fields / APIs continue to be returned as agreed or give a deprecation notice; compatibility handling for old-version callers when a new required field is added |
