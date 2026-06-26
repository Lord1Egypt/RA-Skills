---
name: Go (Gin / Echo / Fiber)
detect:
  files: ["go.mod", "go.sum"]
  dependencies: ["gin-gonic/gin", "labstack/echo", "gofiber/fiber"]
  keywords: ["Go", "Golang", "Gin", "Echo", "Fiber"]
---

## attack-surface-http

**Go HTTP Handler Vulnerabilities:**
1. **No Built-in CSRF Protection:**
   - Go web frameworks do not include CSRF protection by default
   - Check if a CSRF middleware is installed (`gorilla/csrf`, `nosurf`, framework-specific)
   - If there is no CSRF middleware: all state-changing endpoints accepting cookies are vulnerable
2. **Input Binding Without Validation:**
   - Gin: Grep for `c.ShouldBindJSON`, `c.ShouldBind`, `c.Bind` — is the bound struct validated with `binding:"required"` tags?
   - Echo: Grep for `c.Bind`, `echo.Bind` — are struct tags enforcing constraints?
   - Fiber: Grep for `c.BodyParser`, `c.QueryParser` — is input validated after parsing?
   - Can an attacker send extra JSON fields that get bound to unexported or sensitive struct fields?
3. **SQL Injection via String Formatting:**
   - Grep for `fmt.Sprintf` used to construct SQL queries — this is the #1 Go SQL injection pattern
   - Check for raw query construction: `db.Raw(`, `db.Exec(` with string concatenation
   - Are parameterized queries used consistently? (`db.Where("id = ?", id)` vs `db.Where("id = " + id)`)
4. **Template Injection:**
   - If `html/template` is used: are templates constructed from user input? (`template.New("").Parse(userInput)`)
   - `text/template` does NOT escape HTML — is it used for HTML output?
5. **Path Traversal:**
   - Grep for `c.File`, `c.FileAttachment`, `http.ServeFile` — is the path user-controlled?
   - Is `filepath.Clean` or `filepath.Abs` used to sanitize paths? (these don't prevent traversal alone)
   - Check for `os.Open`, `os.ReadFile` with user-controlled paths

## attack-surface-authz

**Go Authorization Patterns:**
1. **Middleware Ordering:**
   - Gin uses `r.Use()` for middleware — is auth middleware applied before route groups that need it?
   - Are there route groups without auth middleware that should have it?
   - Can `c.Next()` be skipped to bypass downstream middleware?
2. **Context Value Auth:**
   - Is auth data stored in `c.Set()` / `c.Get()` (Gin) or `c.Set()` / `c.Get()` (Echo)?
   - Can the context value be forged or missing? Is there a check for its presence before use?
   - Is the user ID from context used directly in database queries without ownership verification?

## config-infrastructure

**Go Application Configuration:**
1. **TLS Configuration:**
   - Is the HTTP server running with TLS? (`http.ListenAndServeTLS` or framework equivalent)
   - If TLS is configured: is `MinVersion` set to `tls.VersionTLS12` or higher?
   - Are weak cipher suites disabled?
2. **Goroutine Leaks / Resource Exhaustion:**
   - Are HTTP request contexts used to cancel long-running goroutines? (`context.WithTimeout`, `context.WithCancel`)
   - Is there a maximum request body size configured? (Go's default is unlimited)
   - Are there goroutines spawned per-request without limits?
3. **Error Handling:**
   - Does the error response include stack traces or internal details? (Gin's `GinMode` should be `release` in production)
   - Are panics recovered? (Gin/Echo have recovery middleware — is it enabled?)
   - Do error messages contain file paths, query details, or configuration values?

## logic-dos

**Go-Specific DoS Vectors:**
1. **Unbounded Request Bodies:**
   - Is `http.MaxBytesReader` or framework equivalent configured? (Go accepts unlimited body by default)
   - Can an attacker send a multi-GB request body to exhaust memory?
2. **Goroutine Exhaustion:**
   - Are goroutines spawned per-request without a semaphore or pool?
   - Can an attacker trigger unbounded goroutine creation?
3. **JSON Decoding Bombs:**
   - `encoding/json` will decode deeply nested JSON — can this be used for CPU exhaustion?
   - Is `json.Decoder.DisallowUnknownFields()` used to reject unexpected input?

## dependency-audit

**Go-Specific Dependency Concerns:**
1. Run `govulncheck ./...` if available — checks dependencies against the Go vulnerability database
2. Check `go.mod` for `replace` directives pointing to local paths or forks (supply chain risk)
3. Are there `go.sum` integrity mismatches? (possible tampering)
4. Check for use of archived/unmaintained Go modules
