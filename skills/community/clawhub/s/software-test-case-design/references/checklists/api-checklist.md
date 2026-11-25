# API Testing Checklist

> This checklist corresponds to `references/core-capabilities/api-testing.md` and is used for item-by-item self-checking after designing API test cases.

---

## Contents

| Line | Section |
|------|------|
| 23 | 0. Test Case Executability Check |
| 34 | 1. Functional Testing |
| 45 | 2. Data Validation |
| 59 | 3. Authentication and Authorization |
| 71 | 4. Security Testing |
| 86 | 5. Error Handling |
| 97 | 6. Pagination and Sorting |
| 107 | 7. Search and Filtering |
| 117 | 8. Version Compatibility |

---

## 0. Test Case Executability Check (API testing)

- [ ] Do the test steps give concrete parameter values / request bodies / path values (instead of descriptive language)?
- [ ] Are there unacceptable descriptions such as "send a request with wrong parameters" or "enter abnormal data"?
- [ ] Do request parameters give concrete key=value values?
- [ ] Are setting request headers, setting the request body (or parameters), and sending the request separate steps?
- [ ] Do tokens, API keys, and other credentials use placeholders (e.g., `{{VALID_TOKEN}}`)?
- [ ] Do large data scenarios (e.g., very large request bodies, overly long string parameters) use descriptive language plus explicit parameters?

---

## 1. Functional Testing

- [ ] GET requests return normally (single item, list, query with parameters)
- [ ] POST creates resources successfully; duplicate creation is handled correctly
- [ ] PUT/PATCH full and partial updates succeed; updating a non-existent resource is handled correctly
- [ ] DELETE succeeds; deleting a non-existent resource is handled correctly
- [ ] Batch operations are correct; partial success is handled as agreed
- [ ] Status codes follow the conventions (200/201/204/400/401/403/404/409/422/500)

---

## 2. Data Validation

- [ ] Required field validation
- [ ] Field type validation
- [ ] Field format validation
- [ ] Field length validation
- [ ] Field range validation
- [ ] Uniqueness validation
- [ ] Business rule validation (foreign key constraints, state transition rules)
- [ ] Response field names, types, and required flags match the API document (Swagger / OpenAPI)
- [ ] Database and cache data after writes are consistent with the request

---

## 3. Authentication and Authorization

- [ ] Token authentication works
- [ ] Unauthenticated access is rejected (401)
- [ ] Access without permission is rejected (403)
- [ ] Token expiration handling
- [ ] Token refresh works
- [ ] Tokens cannot be used after revocation (logout)
- [ ] Role, resource, and data permissions are correctly isolated

---

## 4. Security Testing

- [ ] Injection attacks: SQL injection, NoSQL injection, and command injection parameters are handled correctly
- [ ] Horizontal privilege escalation: changing a resource ID to access others' data is rejected
- [ ] Vertical privilege escalation: a regular user token accessing admin APIs is rejected
- [ ] Mass assignment: read-only fields added to the request body (e.g., role, isAdmin, balance) have no effect or are rejected
- [ ] API rate limiting: 429 is returned after exceeding the rate limit threshold
- [ ] Sensitive data exposure: responses contain no password hashes, tokens, internal IPs, or other sensitive fields
- [ ] Error responses do not expose stacks, framework versions, or other internal information
- [ ] Security response headers (X-Content-Type-Options, X-Frame-Options, CSP, HSTS) are configured correctly
- [ ] JWT security: unsigned tokens (alg=none), expired tokens, and tampered payloads are all rejected
- [ ] Parameter pollution: duplicate parameters and array injection are handled as expected

---

## 5. Error Handling

- [ ] Standardized error codes
- [ ] Clear error messages
- [ ] Database exceptions, third-party service exceptions, network exceptions, and timeouts are handled correctly
- [ ] Logging
- [ ] Retry mechanism (retry count limit)
- [ ] Idempotency guarantee

---

## 6. Pagination and Sorting

- [ ] Pagination parameters work
- [ ] Total count is correct
- [ ] Out-of-range page number and page size are handled correctly (e.g., page=0, page beyond the total number of pages, pageSize above the limit)
- [ ] Sorting works (single / multiple fields, ascending / descending)
- [ ] Default sorting is reasonable

---

## 7. Search and Filtering

- [ ] Exact search works
- [ ] Fuzzy search works
- [ ] Multi-condition combinations are correct
- [ ] Filtering works (time range, status, category)
- [ ] An empty list (not an error) is returned when nothing matches

---

## 8. Version Compatibility

- [ ] When multiple versions coexist, the request and response structures of the old version (e.g., /v1) remain unchanged
- [ ] New fields in the new version do not affect old-version callers
- [ ] Requesting a non-existent version (e.g., /v99) returns 404 or a clear error message
- [ ] Deprecated fields / APIs continue to be returned as agreed or give a deprecation notice
