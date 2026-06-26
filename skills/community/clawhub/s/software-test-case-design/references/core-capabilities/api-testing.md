# API Testing

> This document defines specialized testing dimensions and strategy highlights for API testing. It is used complementarily with other test types.

---

## Table of Contents

| Line | Section |
|------|---------|
| 8 | I. Functional Testing |
| 24 | II. Status Code Verification |
| 38 | III. Data Validation |
| 46 | IV. Authentication & Authorization |
| 54 | V. Security Testing |
| 68 | VI. Error Handling |
| 78 | VII. Pagination & Sorting |
| 86 | VIII. Search & Filtering |

---

## I. Functional Testing

| Test Scenario | Test Highlights |
|---------|---------|
| GET Request | Normal single/list data query; query with parameters; handling of empty/incorrect parameter types |
| POST Request | Normal resource creation; required field validation; field format validation; duplicate creation handling |
| PUT/PATCH Request | Full update/partial update; updating non-existent resource; concurrent update handling |
| DELETE Request | Normal deletion; deleting non-existent resource; cascading deletion; soft deletion |
| Batch Operations | Batch create/update/delete; partial success handling; transaction rollback |

---

## II. Status Code Verification

| Status Code | Description |
|-------|------|
| 200 OK | Normal response |
| 201 Created | Creation successful |
| 204 No Content | Deletion successful |
| 400 Bad Request | Parameter error |
| 401 Unauthorized | Not authenticated |
| 403 Forbidden | No permission |
| 404 Not Found | Resource not found |
| 409 Conflict | Resource conflict |
| 422 Unprocessable | Validation failed |
| 500 Internal Error | Server error |

---

## III. Data Validation

| Test Scenario | Test Highlights |
|---------|---------|
| Field Validation | Required field, type, length, format, range validation |
| Business Rules | Uniqueness constraints, foreign key constraints, state transition rules |
| Data Consistency | Database write verification, cache synchronization verification |

---

## IV. Authentication & Authorization

| Test Scenario | Test Highlights |
|---------|---------|
| Token Authentication | Token generation, refresh, expiry, revocation |
| Permission Control | Role-based permission, resource permission, data permission verification |

---

## V. Security Testing

| Test Scenario | Test Highlights |
|---------|---------|
| Injection Attacks | SQL injection (parameterized query verification), NoSQL injection, command injection |
| Unauthorized Access | Horizontal privilege escalation (IDOR, modifying resource ID to access others' data), vertical privilege escalation (using normal Token to access admin APIs) |
| Mass Assignment | Adding read-only fields (e.g., role, isAdmin, balance) to the request body and verifying they are rejected |
| API Rate Limiting | Sending a large number of requests (>100/sec) in a short period and verifying whether 429 is returned |
| Sensitive Information Leakage | Whether responses return sensitive fields such as password hashes, Tokens, internal IPs; whether error stack traces expose framework versions |
| Security Header Check | Security response headers such as X-Content-Type-Options, X-Frame-Options, CSP, HSTS |
| JWT Security | Unsigned Token (alg=none), expired Token, tampered Payload, key brute-forcing |
| Parameter Pollution | Duplicate parameters (?id=1&id=2), array injection (?id[]=1&id[]=2), HTTP Parameter Pollution |

---

## VI. Error Handling

| Test Scenario | Test Highlights |
|---------|---------|
| Error Response | Error code specification; clear error messages |
| Exception Handling | Database exceptions, third-party service exceptions, network exceptions, timeout handling |
| Retry Mechanism | Automatic retry; retry count limit; idempotency guarantee |

---

## VII. Pagination & Sorting

| Test Scenario | Test Highlights |
|---------|---------|
| Pagination | Page number parameter, page size, total count, out-of-bounds handling |
| Sorting | Single-field/multi-field sorting; sort direction; default sorting |

---

## VIII. Search & Filtering

| Test Scenario | Test Highlights |
|---------|---------|
| Search | Exact search, fuzzy search, full-text search, multi-condition combination |
| Filtering | Time range, status, category, custom filtering |
