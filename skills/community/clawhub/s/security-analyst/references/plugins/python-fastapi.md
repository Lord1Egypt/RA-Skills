---
name: Python + FastAPI
detect:
  files: []
  dependencies: ["fastapi", "uvicorn"]
  keywords: ["FastAPI"]
---

## attack-surface-http

**Pydantic Model Validation Bypass:**
1. FastAPI uses Pydantic models for request validation — but validation can be bypassed:
   - Are there endpoints that accept `dict`, `Any`, or `Body(...)` without a Pydantic model? These skip validation
   - Are Pydantic models using `model_config = ConfigDict(extra="allow")`? This allows clients to send extra fields that pass validation
   - Are there `validator` or `field_validator` decorators that can be tricked? (e.g., regex validators with ReDoS patterns)
   - Is `orm_mode` / `from_attributes` used? Check that ORM objects don't expose sensitive fields when serialized

2. **Dependency Injection Auth Checks:**
   - FastAPI uses `Depends()` for auth — Grep for all dependency functions used for authentication
   - Are auth dependencies applied to all routes that need them? (easy to forget on a new endpoint)
   - Can auth dependencies be bypassed by passing the right parameters? (e.g., optional auth: `Depends(optional_auth)` where `None` is valid)
   - Are there endpoints with `dependencies=[Depends(auth)]` at the router level that have routes inadvertently excluded?

3. **File Upload Security:**
   - Grep for `UploadFile`, `File(...)` parameters
   - Are file uploads size-limited? (check for `UploadFile` without `max_size` or middleware-level limits)
   - Is the file content type validated server-side? (client-sent `content_type` is spoofable)
   - Are uploaded files written to a safe location? (path traversal via filename: `file.filename` comes from the client)
   - Are uploaded files scanned or validated before processing?

4. **Background Task Auth Context:**
   - Grep for `BackgroundTasks`, `background_tasks.add_task`
   - Do background tasks inherit the request's auth context? (they run after the response is sent — the auth state may be stale)
   - Can a background task perform privileged operations without re-verifying authorization?
   - Are background task failures handled? (no built-in retry or error handling)

5. **ASGI Middleware Ordering:**
   - Middleware in FastAPI/Starlette executes in reverse registration order (last registered = outermost = runs first)
   - Is auth middleware registered AFTER (so it runs BEFORE) other middleware?
   - Can CORS middleware response headers leak information before auth middleware rejects the request?

6. **Path Operation Quirks:**
   - FastAPI matches routes in order of declaration — can a less-restrictive route shadow a more-restrictive one?
   - Path parameters are strings by default — are they type-validated? (`/users/{user_id:int}` vs `/users/{user_id}`)
   - Are there routes with `response_model` that might expose sensitive fields from the ORM model?
   - Is `response_model_exclude` used correctly? (easier to accidentally include than to whitelist with `response_model_include`)

## config-infrastructure

**CORS Middleware:**
1. Read `CORSMiddleware` configuration:
   - Is `allow_origins=["*"]` used? (allows any origin)
   - Is `allow_credentials=True` combined with broad origins? (dangerous — enables cross-origin cookie access)
   - Are `allow_methods` and `allow_headers` restricted to what's needed?

**Server Configuration:**
2. Uvicorn/Gunicorn security:
   - Is `--reload` flag used in production? (auto-reloads on file changes — security risk if an attacker can write files)
   - Is the server binding to `0.0.0.0` or a specific interface?
   - Are Gunicorn workers configured with timeouts to prevent slow request DoS?
   - Is `--access-log` enabled for audit trailing?

3. **OpenAPI/Swagger UI Exposure:**
   - Is the auto-generated Swagger UI (`/docs`) and ReDoc (`/redoc`) accessible in production?
   - Is the OpenAPI schema (`/openapi.json`) exposing internal API structure?
   - Can these endpoints be disabled in production? (Grep for `docs_url=None`, `redoc_url=None`, `openapi_url=None`)

4. **Environment and Debug Settings:**
   - Is `debug=True` set in the FastAPI app constructor in production?
   - Are there custom exception handlers that return stack traces based on a debug flag?
   - Is `PYTHONDONTWRITEBYTECODE` set? (prevents `.pyc` file creation that could leak source in shared environments)
