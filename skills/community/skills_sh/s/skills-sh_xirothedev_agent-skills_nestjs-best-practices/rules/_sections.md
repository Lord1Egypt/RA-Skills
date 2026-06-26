# Sections

This file defines all sections, their ordering, impact levels, and descriptions.
The section ID (in parentheses) is the filename prefix used to group rules.

---

## 1. Security (security)

**Impact:** CRITICAL
**Description:** Security vulnerabilities can lead to data breaches, unauthorized access, and service disruption. Always prioritize security in production.

## 2. Performance (performance)

**Impact:** HIGH
**Description:** Server performance directly affects user experience and infrastructure costs. Caching, compression, and lazy loading yield significant gains.

## 3. Architecture (architecture)

**Impact:** HIGH
**Description:** Proper module structure, separation of concerns, single responsibility, and naming conventions ensure maintainable and scalable applications.

## 4. Error Handling (error-handling)

**Impact:** HIGH
**Description:** Comprehensive error handling and structured logging enable debugging, monitoring, and graceful failure recovery in production environments.

## 5. Validation (validation)

**Impact:** CRITICAL
**Description:** Input validation prevents invalid data, reduces attack surface, and provides clear error messages to API consumers.

## 6. Database (database)

**Impact:** CRITICAL
**Description:** Parameterized queries prevent SQL injection. Efficient database queries and proper data handling prevent performance bottlenecks and security issues.

## 7. Authentication (auth)

**Impact:** CRITICAL
**Description:** Guards and authentication mechanisms ensure only authorized users can access protected resources and perform allowed actions.

## 8. API (api)

**Impact:** MEDIUM
**Description:** Well-designed APIs with consistent patterns, proper documentation (Swagger), and pagination improve developer experience and client integration.

## 9. Config (config)

**Impact:** CRITICAL
**Description:** Proper configuration management prevents secrets leakage, enables environment-specific settings, and simplifies deployment across environments.

## 10. Testing (testing)

**Impact:** MEDIUM
**Description:** Comprehensive test coverage ensures code quality, prevents regressions, and documents expected behavior through executable specifications.

## 11. Deployment (deployment)

**Impact:** MEDIUM
**Description:** Production readiness includes health checks, graceful shutdown, logging, monitoring, and scaling considerations.

## 12. Middleware (middleware)

**Impact:** MEDIUM
**Description:** Custom middleware for rate limiting, compression, and cross-cutting concerns improve application security and performance.

## 13. Advanced (advanced)

**Impact:** HIGH
**Description:** Advanced patterns like lazy loading, scheduled tasks, and event-driven architecture require careful implementation and deep understanding of NestJS internals.

## 14. Interceptors (interceptors)

**Impact:** MEDIUM
**Description:** Interceptors provide cross-cutting concerns like response transformation, logging, and caching for consistent behavior across routes.
