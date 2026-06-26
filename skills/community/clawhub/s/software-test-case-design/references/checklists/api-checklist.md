# API Testing Checklist

> This checklist covers all dimensions of API testing for item-by-item self-review after API test case design.

---

## Table of Contents

| Line | Section |
|------|---------|
| 13 | 0. Test Case Executability Check |
| 20 | I. Functional Testing |
| 28 | II. Data Validation |
| 36 | III. Authentication & Authorization |
| 43 | IV. Error Handling |
| 50 | V. Pagination & Sorting |
| 56 | VI. Search & Filtering |
| 62 | VII. Version Management |
| 68 | VIII. API Documentation |

---

## 0. Test Case Executability Check (common to all test types)

- [ ] Do test steps provide concrete parameter values/request bodies/path values (rather than descriptive language)?
- [ ] Are there any unqualified descriptions such as "send a request with invalid parameters" or "input abnormal data"?
- [ ] Do request parameters specify concrete key=value pairs?
- [ ] For large data scenarios (e.g., oversized request bodies, extremely long string parameters), is descriptive language with explicit parameter specifications used?

---

## I. Functional Testing

- [ ] GET request returns normally
- [ ] POST creates resource successfully
- [ ] PUT/PATCH updates successfully
- [ ] DELETE deletes successfully
- [ ] Batch operations correct
- [ ] Status codes conform to specification
- [ ] Error responses are clear

---

## II. Data Validation

- [ ] Required field validation
- [ ] Field type validation
- [ ] Field format validation
- [ ] Field length validation
- [ ] Field range validation
- [ ] Uniqueness validation
- [ ] Business rule validation

---

## III. Authentication & Authorization

- [ ] Token authentication works correctly
- [ ] Unauthenticated access is rejected
- [ ] Unauthorized access is rejected
- [ ] Token expiry is handled
- [ ] Token refresh works correctly
- [ ] Permission isolation is correct

---

## IV. Error Handling

- [ ] Error codes follow specification
- [ ] Error messages are clear
- [ ] Exceptions are caught
- [ ] Logging is in place
- [ ] Retry mechanism exists
- [ ] Idempotency is guaranteed

---

## V. Pagination & Sorting

- [ ] Pagination parameters work correctly
- [ ] Total count is correct
- [ ] Sorting functionality works correctly
- [ ] Default sorting is reasonable

---

## VI. Search & Filtering

- [ ] Exact search works correctly
- [ ] Fuzzy search works correctly
- [ ] Multi-condition combination is correct
- [ ] Filtering functionality works correctly

---

## VII. Version Management

- [ ] Version control is correct
- [ ] Backward compatibility is maintained
- [ ] Version documentation is complete

---

## VIII. API Documentation

- [ ] Conforms to Swagger/OpenAPI specification
- [ ] Parameter descriptions are complete
- [ ] Examples are clear
- [ ] Error code documentation is provided
